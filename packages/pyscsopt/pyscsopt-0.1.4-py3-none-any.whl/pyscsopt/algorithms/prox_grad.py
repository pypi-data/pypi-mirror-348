import numpy as np
import jax
import jax.numpy as jnp
from pyscsopt.utils.utils import linesearch
import pyscsopt.prox.prox_operators as prox_ops

class ProxGradient:
    def __init__(self, ss_type=1, use_prox=True, name="prox-grad", label="Prox-Grad"):
        self.ss_type = ss_type
        self.use_prox = use_prox
        self.name = name
        self.label = label

    def init(self, x):
        return self

    def step(self, model, reg_name, hmu, As, x, x_prev, ys, Cmat, iter):
        # handle regularization parameter
        lam = model.lam[0] if hasattr(model.lam, '__len__') and len(model.lam) > 1 else model.lam
        lam_gr = lam * hmu.grad(Cmat, x)
        Hr_diag = hmu.hess(Cmat, x)
        is_generic = (model.A is None or model.y is None)
        if is_generic:
            obj = lambda x_: model.f(x_) + model.get_reg(x_, reg_name)
            if hasattr(model, 'grad_fx') and model.grad_fx is not None:
                grad_f = lambda x_: model.grad_fx(x_) + lam_gr
            else:
                grad_f = lambda x_: jnp.array(jax.grad(lambda z: model.f(z))(x_)) + lam_gr
        else:
            obj = lambda x_: model.f(As, ys, x_) + model.get_reg(x_, reg_name)
            if hasattr(model, 'grad_fx') and model.grad_fx is not None:
                grad_f = lambda x_: model.grad_fx(As, ys, x_) + lam_gr
            else:
                grad_f = lambda x_: jnp.array(jax.grad(lambda z: model.f(As, ys, z))(x_)) + lam_gr
        grad = grad_f(x)
        d = -grad
        # step size selection
        if self.ss_type == 1 and getattr(model, 'L', None) is not None:
            step_size = 1.0 / model.L
        elif self.ss_type == 1 and getattr(model, 'L', None) is None:
            step_size = linesearch(x, d, obj, grad_f)
        elif self.ss_type == 2:
            # lam_gr_prev = lam * hmu.grad(Cmat, x_prev)
            grad_prev = grad_f(x_prev)
            delta = x - x_prev
            gamma = grad - grad_prev
            L_val = np.dot(gamma, gamma)/np.dot(delta, gamma) if np.dot(delta, gamma) != 0 else 1.0
            step_size = 1.0 if iter == 1 else L_val
        elif self.ss_type == 3:
            step_size = linesearch(x, d, obj, grad_f)
        else:
            step_size = 1.0 / model.L
        if self.use_prox:
            x_new = prox_ops.invoke_prox(model, reg_name, x + step_size * d, np.ones_like(Hr_diag), lam, step_size)
        else:
            x_new = x + step_size * d
        grad_norm = np.linalg.norm(grad)
        return x_new, grad_norm
