#!/usr/bin/env python
"""
Testing for revealing factors for Max-kAND.
Uses 

By Noah Singer <ngsinger@cs.cmu.edu>, May 2023
"""

from lp import primal_lp, build_pattern_dict

def unif_partition(l):
    """
    Generate a uniform bias partition (i.e., a partition of [0,1]
    into equally spaced intervals).
    """
    return list(i/l for i in range(l+1))

def piecewise_partition(l, x_th):
    """
    Generate a piecewise bias partition with a threshold at x_th.
    """
    return list(i/(l-1) * x_th for i in range(l)) + [1,]

def midpoint_rounding(t, f):
    """
    Discretizes a continuous selection function `f`. Given a bias partition `t`,
    returns a rounding vector `p` such that the rounding of the i-th interval
    is the midpoint of the selection function over that interval.
    """
    values = list(map(f, t))
    return tuple((values[i]+values[i+1])/2 for i in range(len(t)-1))

def pl_sigmoid(x_th, y_th=1.0):
    """
    A piecewise linear (PL) sigmoid function: Interpolates between 1/2 and
    y_th over biases in [0,x_th], then between y_th and 1 over biases in [x_th,1].
    """
    def wrapper(x):
        assert -10e-10<=x<=1+10e-10
        if x <= x_th:
            return 0.5 + (y_th-0.5)*x/x_th
        else:
            return y_th + (1-y_th)*(x-x_th)/(1-x_th)
    return wrapper

def pl_sigmoid_ratio(k, l, x_th, y_th=1.0, patterns=None, log=True):
    """
    Test PL sigmoid rounding as in the previous function.
    """
    if log:
        print("~"*80)
        print("Testing PL sigmoid rounding, k={}, l={}, x_th={}, y_th={}".format(k, l, x_th, y_th))
    
    t = piecewise_partition(l, x_th)
    f = pl_sigmoid(x_th, y_th)
    p = midpoint_rounding(t, f)
    factor = primal_lp(k, l, t, p, patterns=patterns, log=log)

    if log:
        print("Result: {}".format(factor))
    return factor

def test_pl_many(k, l, th_list, log=True):
    """
    Test many different parameter settings for PL sigmoid rounding,
    reusing the pattern dictionary to save time.
    """
    patterns = build_pattern_dict(k, l, log=log)
    best_factor = 0
    for x_th, y_th in th_list:
        try:
            factor = pl_sigmoid_ratio(k, l, x_th, y_th, patterns=patterns, log=log)
            if factor > best_factor:
                if log:
                    print("New best factor {} @ (x_th,y_th) = ({},{})".format(factor, x_th, y_th))
                best_factor = factor
        except:
            print("An error occured while solving the LP")
    if log:
        print("Final best factor {}".format(best_factor))
    return best_factor

def grid_th_list(k, l, x_th_b, y_th_b, x_ticks, y_ticks):
    """
    Generate a grid to search over for parameters of PL sigmoid rounding. 
    """
    x_th_l,x_th_u = x_th_b
    y_th_l,y_th_u = y_th_b

    return [(x_th_l + (x_th_u-x_th_l)*i/max(1,x_ticks-1),
        y_th_l + (y_th_u-y_th_l)*j/(max(1,y_ticks-1)))
        for i in range(x_ticks) for j in range(y_ticks)]

def test_pl_grid(k, l, x_th_b, y_th_b, x_ticks, y_ticks):
    """
    Do a grid search for the best parameters for PL sigmoid rounding.
    """
    grid = grid_th_list(k, l, x_th_b, y_th_b, x_ticks, y_ticks)
    test_pl_many(k, l, grid)

def superobl_p(k):
    """
    Calculate the rounding probability used by the optimal superoblivious algorithm.
    """
    if k%2==0:
        return 1/2 + 1/(2*(k+1))
    else:
        return 1/2 + 1/(2*k)

def superobl_alpha(k):
    """
    Calculate the ratio achieved by the optimal superoblivious algorithm.
    """
    if k%2==0:
        return 2**(-(k - 1))*(1 - 1/(k + 1)**2)**(k/2)
    else:
        return 2**(-(k - 1))*(1 - 1/k**2)**((k - 1)/2)

def superobl_ratio(k, delta=0.01, eps=0.001):
    """
    Test a small perturbation of the optimal superoblivious algorithm.
    """
    print("~"*80)
    print("Testing superoblivious rounding, k={}, l={}".format(k, 1))
    t0 = (0,1)
    td = (delta,1)
    p0 = (superobl_p(k),)
    pe = (superobl_p(k)+eps,)
    print("Predicted superoblivious ratio: {}".format(superobl_alpha(k)))
    print("Computed superoblivious ratio: {}".format(primal_lp(k, 1, t0, p0)))
    print("Computed perturbed ratio: {}".format(primal_lp(k, 1, td, pe)))
