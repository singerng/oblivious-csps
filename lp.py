"""
Factor-revealing LP for oblivious algorithms for Max-kAND

By Noah Singer <ngsinger@cs.cmu.edu>, May 2023
"""

import numpy as np
import cvxpy as cp

from pattern import enum_patterns

def ivl_bound(t, sgn, i):
    if i >= (1-sgn)//2:
        return t[i-1+(1+sgn)//2]
    else:
        return -t[-i-1+(1-sgn)//2]

def primal_lp(k, l, t, p, solver=cp.GLPK, verbose=False):
    assert len(t) == l+1
    assert len(p) == l

    print("="*40)
    print("Setting up LP!")

    n = 0
    patterns = {}
    for pattern in enum_patterns(k, l):
        patterns[n] = pattern
        n += 1
    W = cp.Variable(n)

    prob_vector = np.array([patterns[j].prob(p) for j in range(n)])
    objective = prob_vector.T @ W

    nonneg_constraints = W >= 0

    pos_vector = np.array([int(patterns[j].is_positive()) for j in range(n)])
    opt_constraint = pos_vector.T @ W == 1

    bias_constraints = []

    for i in range(-l,l+1):
        pos_i_vector = np.array([patterns[j][+1, i] for j in range(n)])
        neg_i_vector = np.array([patterns[j][-1, i] for j in range(n)])

        total_weight = (pos_i_vector+neg_i_vector).T @ W
        bias_weight = (pos_i_vector-neg_i_vector).T @ W

        bias_constraints.append(ivl_bound(t, -1, i) * total_weight <= bias_weight)
        bias_constraints.append(bias_weight <= ivl_bound(t, +1, i) * total_weight)

    constraints = [nonneg_constraints, opt_constraint] + bias_constraints

    print("Solving LP with {} variables and {} constraints".format(n, len(constraints)))
    print("="*40)
    return cp.Problem(cp.Minimize(objective), constraints).solve(solver=solver, verbose=verbose)

