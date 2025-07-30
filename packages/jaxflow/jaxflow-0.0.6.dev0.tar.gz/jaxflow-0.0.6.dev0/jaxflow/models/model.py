import math
from typing import Optional, Tuple

import jax
import jax.numpy as jnp
from jax import value_and_grad, jit, vmap, pmap
from tqdm import tqdm
from sklearn.model_selection import train_test_split
import optax

from jaxflow.layers.layer import Layer


class Model(Layer):
    """High‑performance JAXFlow *Model* with

    * explicit `add()` API
    * pure‑functional training loop (Optax)
    * automatic JIT / vmap / pmap fusion
    * optional `validation_split` handled by *scikit‑learn*
    * `evaluate(..., params=…)` so you can test *any* parameter tree
    """

    # ---------------------------------------------------------------------
    # Construction & layer management
    # ---------------------------------------------------------------------

    def __init__(self, name: Optional[str] = None, trainable: bool = True):
        super().__init__(name=name, trainable=trainable)
        self.layers: list[Layer] = []  # user‑registered layers in order
        # training state handles (filled during compile)
        self.optimizer = None
        self.loss_fn = None
        self.metrics = []
        self.multi_device = False
        self._opt_state = None
        self._accum_grads = None
        self._ema_params = None
        self._step = None

    # -- user facing -------------------------------------------------------

    def add(self, layer: Layer):
        if not isinstance(layer, Layer):
            raise ValueError("add() expects a Layer instance")
        self.layers.append(layer)

    # -- internal helpers --------------------------------------------------

    def _get_all_sub_layers(self):
        explicit = list(self.layers)
        inherited = super()._get_all_sub_layers()
        return explicit + [l for l in inherited if l not in explicit]

    # ---------------------------------------------------------------------
    # Building & fused forward
    # ---------------------------------------------------------------------

    def build(self, input_shape):
        dummy = list(input_shape)
        if not dummy or dummy[0] in (None, 0):
            dummy[0] = 1
        x = jnp.zeros(dummy, dtype=jnp.float32)
        subs = self._get_all_sub_layers()
        for L in subs:
            if not L.built:
                L.build(x.shape)
                L.built, L.built_shape = True, (None,) + x.shape[1:]
            x = L(x, training=False)
        self.built, self.built_shape = True, input_shape

        # Python‑loop forward; JIT w/ static training flag
        def _forward(inp, training: bool):
            out = inp
            for L in subs:
                out = L(out, training=training)
            return out

        self._forward_fn = jit(_forward, static_argnums=(1,))

    # public call ----------------------------------------------------------
    def call(self, inputs, training: bool = False):
        if not self.built:
            self.build(inputs.shape)
        return self._forward_fn(inputs, training)

    # functional forward (pure) -------------------------------------------
    def functional_call(self, inputs, params, training: bool = False):
        out = inputs
        for i, L in enumerate(self._get_all_sub_layers()):
            out = L.functional_call(out, params[f"layer_{i}"], training=training)
        return out

    # ---------------------------------------------------------------------
    # Parameter helpers
    # ---------------------------------------------------------------------

    def get_params(self):
        return {
            f"layer_{i}": {n: v.value for n, v in L._params.items()}
            for i, L in enumerate(self._get_all_sub_layers())
        }

    def set_params(self, params):
        for i, L in enumerate(self._get_all_sub_layers()):
            for n, v in L._params.items():
                v.assign(params[f"layer_{i}"][n])

    # ---------------------------------------------------------------------
    # Compilation (optimizer + jit kernels)
    # ---------------------------------------------------------------------

    def compile(self, optimizer, loss_fn, *, metrics=None, multi_device=False):
        if not self.built:
            raise RuntimeError("Call build() (or run data through the model) before compile().")
        self.optimizer = optimizer
        self.loss_fn = loss_fn
        self.metrics = metrics or []
        self.multi_device = multi_device

        # vectorised forward (batch axis 0)
        self._batched_forward = vmap(self._forward_fn, in_axes=(0, None))
        if multi_device:
            self._parallel_forward = pmap(self._batched_forward, in_axes=(0, None))
        else:
            self._parallel_forward = self._batched_forward

        params = self.get_params()
        self._opt_state, self._accum_grads, self._ema_params, self._step = optimizer.init(params)

        self._train_step = jit(self._make_train_step())
        self._eval_step = jit(self._make_eval_step())

    # ---------------------------------------------------------------------
    # Data splitting helper
    # ---------------------------------------------------------------------

    @staticmethod
    def _split_data(X, Y, val_split: float):
        X_train, X_val, Y_train, Y_val = train_test_split(
            X, Y, test_size=val_split, shuffle=True
        )
        return X_train, Y_train,X_val, Y_val

    # ---------------------------------------------------------------------
    # JIT‑compiled step factories
    # ---------------------------------------------------------------------

    def _make_train_step(self):
        def step(params, opt_state, accum, ema, count, xb, yb):
            def loss_fn(p):
                preds = self.functional_call(xb, p, training=True)
                return self.loss_fn(yb, preds)
            loss, grads = value_and_grad(loss_fn)(params)
            params, opt_state, accum, ema, count, _ = self.optimizer.update(
                params, grads, opt_state, accum, ema, count)
            return params, opt_state, accum, ema, count, loss
        return step

    def _make_eval_step(self):
        def step(params, xb, yb):
            preds = self.functional_call(xb, params, training=False)
            return self.loss_fn(yb, preds)
        return step

    # ---------------------------------------------------------------------
    # Fit / evaluate / predict
    # ---------------------------------------------------------------------

    def fit(
        self,
        X,
        Y,
        *,
        epochs: int,
        batch_size: int = 32,
        validation_data: Optional[Tuple] = None,
        validation_split: Optional[float] = None,
        verbose: int = 1,
    ):
        if validation_split is not None:
            if validation_data is not None:
                raise ValueError("Pass either validation_data or validation_split, not both.")
            if not (0.0 < validation_split < 1.0):
                raise ValueError("validation_split must be in (0,1)")
            X, Y,X_val, Y_val = self._split_data(X, Y, validation_split)
            validation_data = (X_val, Y_val)

        params = self.get_params()
        opt_state, accum, ema, step = (
            self._opt_state, self._accum_grads, self._ema_params, self._step
        )

        n_samples = X.shape[0]
        steps_per_epoch = max(1, math.ceil(n_samples / batch_size))

        history = {"loss": []}
        if validation_data is not None:
            history["val_loss"] = []

        for epoch in range(1, epochs + 1):
            if verbose:
                print(f"Epoch {epoch}/{epochs}")
            running = 0.0
            bar = tqdm(total=steps_per_epoch, desc="Training", unit="batch",
                        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}] • {postfix}") if verbose else None
            for step_idx in range(steps_per_epoch):
                start = step_idx * batch_size
                end = min(start + batch_size, n_samples)
                xb, yb = X[start:end], Y[start:end]
                params, opt_state, accum, ema, step, loss_val = self._train_step(
                    params, opt_state, accum, ema, step, xb, yb)
                running += float(loss_val)
                if verbose:
                    bar.update(1)
                    bar.set_postfix({"loss": f"{running/(step_idx+1):.4f}"})
            if verbose:
                bar.close()
            avg_loss = running / steps_per_epoch
            history["loss"].append(avg_loss)

            # --- Validation (uses fresh params, no mutation) -------------
            if validation_data is not None:
                Xv, Yv = validation_data
                val_loss = self.evaluate(Xv, Yv, batch_size=batch_size, verbose=0, params=params)
                history["val_loss"].append(val_loss)
                if verbose:
                    print(f"loss: {avg_loss:.4f} — val_loss: {val_loss:.4f}")

        # after final epoch push trained weights into layers
        self.set_params(params)
        self._opt_state, self._accum_grads, self._ema_params, self._step = opt_state, accum, ema, step
        return history

    def evaluate(
        self,
        X,
        Y,
        *,
        batch_size: int = 32,
        verbose: int = 0,
        params: Optional[dict] = None,
    ) -> float:
        """Compute loss on a dataset. If *params* is provided, evaluate that
        parameter tree; otherwise use the model's internal buffers."""
        if params is None:
            params = self.get_params()

        n = X.shape[0]
        steps = max(1, math.ceil(n / batch_size))
        total = 0.0

        bar = tqdm(total=steps, desc="Evaluating", unit="batch",
                    bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}] • {postfix}") if verbose else None
        for i in range(steps):
            xb = X[i * batch_size:(i + 1) * batch_size]
            yb = Y[i * batch_size:(i + 1) * batch_size]
            total += float(self._eval_step(params, xb, yb))
            if verbose:
                bar.update(1); bar.set_postfix({"loss": f"{total/(i+1):.4f}"})
        if verbose:
            bar.close()
        return total / steps

    # ---------------------------------------------------------------------
    # Prediction wrappers
    # ---------------------------------------------------------------------

    def predict(self, X):
        if not hasattr(self, "_batched_forward"):
            # not compiled yet – fall back to per-example call()
            return vmap(lambda x: self.call(x, training=False))(X)
        return  self.call(X, training=False)

    
    def predict_pmap(self, Xs):
        if not self.multi_device:
            raise RuntimeError("Compile with multi_device=True")
        devices = jax.local_devices()
        params = self.get_params()
        pr = jax.device_put_replicated(params, devices)
        return pmap(self._batched_forward, in_axes=(0, None))(Xs, False)

    def summary(self):
        print(f"Model '{self.name}' summary:")
        for i, L in enumerate(self._get_all_sub_layers()):
            print(f"  Layer {i}: {L}")

    def __repr__(self):
        return f"<Model {self.name}, built={self.built}, layers={len(self._get_all_sub_layers())}>"