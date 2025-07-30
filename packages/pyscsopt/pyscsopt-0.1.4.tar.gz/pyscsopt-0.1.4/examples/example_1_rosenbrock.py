import numpy as np
import pyscsopt as scs
from pyscsopt.regularizers import PHuberSmootherL1L2
from pyscsopt.algorithms import ProxGradient, ProxLQNSCORE

import numpy as np

np.random.seed(1234)

def f(x):
    return 100 * (x[1] - x[0]**2)**2 + (1 - x[0])**2

x0 = np.array([0.0, -2.0])
lbda = 1e-8 # or set to zero to remove regularization entirely
reg_name = "l1" # see other examples for other regularization names
mu = 1.0
hmu = PHuberSmootherL1L2(mu)
problem = scs.Problem(x0, f, lbda)

# proximal gradient
method_pg = ProxGradient(use_prox=True, ss_type=1)
sol_pg = scs.iterate(method_pg, problem, reg_name, hmu, verbose=1, max_epoch=100)

# proximal LQNSCORE (L-BFGS-SCORE)
method_lqn = ProxLQNSCORE(use_prox=True, ss_type=2, m=10)
sol_lqn = scs.iterate(method_lqn, problem, reg_name, hmu, verbose=1, max_epoch=100)

# ### uncomment to print solutions
# print("=" * 50)
# print("ProxGradient:")
# print("Solution x:", sol_pg.x)
# print("=" * 50)
# print("ProxLQNSCORE:")
# print("Solution x:", sol_lqn.x)