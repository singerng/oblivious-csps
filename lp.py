"""
Factor-revealing LP for oblivious algorithms for Max-kAND.

By Noah Singer <ngsinger@cs.cmu.edu>, May 2023
"""

import numpy as np
import cvxpy as cp

from pattern import enum_patterns

def ivl_bound(t, sgn, i):
    """
    Calculate the upper (sgn=+1) or lower (sgn=-1) bound of the i-th interval
    in bias partition t.
    """
    if i >= (1-sgn)//2:
        return t[i-1+(1+sgn)//2]
    else:
        return -t[-i-1+(1-sgn)//2]

def build_pattern_dict(k, l):
    """
    Build a dictionary mapping 'patterns' to nonnegative integers, to
    use as indexes into vector of LP variables.
    """
    print("Building pattern dictionary for k={}, l={}".format(k, l))
    n = 0
    patterns = {}
    for pattern in enum_patterns(k, l):
        patterns[n] = pattern
        n += 1
    return patterns

def primal_lp(k, l, t, p, solver=cp.GLPK, verbose=False, patterns=None):
    """
    Construct and solve the primal factor-revealing LP for the Max-kAND
    oblivious algorithm with L=2*l+1 bias classes, bias partition t,
    rounding vector p.
    """
    assert len(t) == l+1
    assert len(p) == l

    print("="*40)

    if not patterns: # pattern dictionary can be cached
        patterns = build_pattern_dict(k, l)
    n = len(patterns)
    W = cp.Variable(n)

    # objective is expected weight of satisfied clauses
    prob_vector = np.array([patterns[j].prob(p) for j in range(n)])
    objective = prob_vector.T @ W

    # all patterns have nonnegative weight
    nonneg_constraints = W >= 0

    # weight on positive patterns is 1
    pos_vector = np.array([int(patterns[j].is_positive()) for j in range(n)])
    opt_constraint = pos_vector.T @ W == 1

    # bias constraints (see paper)
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
    factor = cp.Problem(cp.Minimize(objective), constraints).solve(solver=solver, verbose=verbose)
    print("="*40)
    return factor
