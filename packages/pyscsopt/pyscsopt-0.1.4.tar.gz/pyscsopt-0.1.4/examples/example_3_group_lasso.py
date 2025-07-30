import numpy as np
import jax.numpy as jnp
import pyscsopt as scs
from pyscsopt.algorithms import ProxGradient, ProxLQNSCORE, ProxGGNSCORE
from pyscsopt.regularizers import PHuberSmootherGL
from pyscsopt.utils import make_group_lasso_problem

np.random.seed(42)

# generate synthetic group lasso regression data using utility
m = 300
n = 100
grpsize = 10
p_active = 0.1  # 10% of groups/features active
A, y, x_true, x0, groups, ind, P = make_group_lasso_problem(
    m=m, n=n, grpsize=grpsize, p_active=p_active, noise_std=0.1, seed=42, group_weights=1.0, use_const_grpsize=True, corr=0.5)

# obj
# define the obj this way ONLY for ProxGGNSCORE (that is, allow for a precomputed yhat, in which case we don't need to provide all the gradient functions below)
def f(A, y, x, yhat=None):
    m = y.shape[0]
    if yhat is None:
        yhat = out_fn(A, x)
    return 0.5 * jnp.sum((yhat - y) ** 2)/m

# strictly OPTIONAL for all methods
def grad_fx(A, y, x):
    m = y.shape[0]
    return (A.T @ (A @ x - y))/m

# the following functions are used ONLY by ProxGGNSCORE (ONLY out_fn is required, others are optional as in other methods provided f is defined as above)
def out_fn(A, x):
    return A @ x

def jac_yx(A, y, yhat, x):
    return A

def grad_fy(A, y, yhat):
    m = y.shape[0]
    return (yhat - y)/m

def hess_fy(A, y, yhat):
    m = y.shape[0]
    return np.eye(len(yhat))/m

# regularization parameters
lam1 = 1e-7  # l1
lam2 = 0.1   # group lasso
lam = [lam1, lam2]
mu = 0.1

x0 = np.random.randn(n)
reg_name = "gl"

# problem = scs.Problem(x0=x0, f=f, lam=lam, A=A, y=y, P=P, out_fn=out_fn, grad_fx=grad_fx, jac_yx=jac_yx, grad_fy=grad_fy, hess_fy=hess_fy)

# the following works fine (gradients are computed internally using jax)
problem = scs.Problem(x0=x0, f=f, lam=lam, A=A, y=y, P=P, out_fn=out_fn)

hmu = PHuberSmootherGL(mu, lam, P) # group lasso smoother takes also lam and P as input

method_pg = ProxGradient(use_prox=True, ss_type=1)
sol_pg = scs.iterate(method_pg, problem, reg_name, hmu, verbose=1, max_epoch=100)

method_lqn = ProxLQNSCORE(use_prox=True, ss_type=2, m=10)
sol_lqn = scs.iterate(method_lqn, problem, reg_name, hmu, verbose=1, max_epoch=100)

method_ggn = ProxGGNSCORE(use_prox=True, ss_type=2)
sol_ggn = scs.iterate(method_ggn, problem, reg_name, hmu, verbose=1, max_epoch=100)

# ### uncomment to print solutions
# print("=" * 50)
# print("True Solution (x_true):")
# print("x_true:", x_true)
# print("=" * 50)
# print("ProxGradient (Sparse Group Lasso):")
# print("Solution x:", sol_pg.x)
# print("=" * 50)
# print("ProxLQNSCORE (Sparse Group Lasso):")
# print("Solution x:", sol_lqn.x)
# print("=" * 50)
# print("ProxGGNSCORE (Sparse Group Lasso):")
# print("Solution x:", sol_ggn.x)
