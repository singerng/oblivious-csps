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
    return tuple(i/l for i in range(l+1))

def pl_rounding(t, x_th, y_th):
    """
    Generate a rounding vector for bias partition t using a piecewise
    linear function: Interpolate between 1/2 and y_th over biases in [0,x_th],
    then between y_th and 1 over biases in [x_th,1].
    """
    def pl(x):
        if x <= x_th:
            return 0.5 + (y_th-0.5)*x/x_th
        else:
            return y_th + (1-y_th)*(x-x_th)/(1-x_th)
    return tuple(map(pl, t[1:]))

def test_pl(k, l, x_th, y_th=1.0, patterns=None):
    """
    Test piecewise linear rounding as in the previous function.
    """
    print("~"*80)
    print("Testing piecewise linear rounding, k={}, l={}, x_th={}, y_th={}".format(k, l, x_th, y_th))
    t = unif_partition(l)
    p = pl_rounding(t, x_th, y_th)
    factor = primal_lp(k, l, t, p, patterns=patterns)
    print("Result: {}".format(factor))
    return factor

def test_pl_many(k, l, th_list):
    """
    Test many different parameter settings for piecewise linear rounding,
    reusing the pattern dictionary to save time.
    """
    patterns = build_pattern_dict(k, l)
    best_factor = 0
    for x_th, y_th in th_list:
        try:
            factor = test_pl(k, l, x_th, y_th, patterns=patterns)
            if factor > best_factor:
                print("New best factor {} @ (x_th,y_th) = ({},{})".format(factor, x_th, y_th))
                best_factor = factor
        except:
            print("An error occured while solving the LP")
    print("Final best factor {}".format(best_factor))

def grid_th_list(k, l, x_th_b, y_th_b, x_ticks, y_ticks):
    """
    Generate a grid to search over for parameters of piecewise linear rounding. 
    """
    x_th_l,x_th_u = x_th_b
    y_th_l,y_th_u = y_th_b

    return [(x_th_l + (x_th_u-x_th_l)*i/max(1,x_ticks-1),
        y_th_l + (y_th_u-y_th_l)*j/(max(1,y_ticks-1)))
        for i in range(x_ticks) for j in range(y_ticks)]

def test_pl_grid(k, l, x_th_b, y_th_b, x_ticks, y_ticks):
    """
    Do a grid search for the best parameters for piecewise linear rounding.
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

def test_superobl(k, delta=0.01, eps=0.001):
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

if __name__ == "__main__":
    # output superoblivious ratios vs. perturbed superoblivious ratios
    for k in range(2, 12):
        test_superobl(k)

    # output ratios from piecewise linear rounding vectors
    test_pl(2, 200, 0.5, 1.0) # 0.4844
    test_pl(3, 30, 0.7, 1.0) # 0.2417
    test_pl(4, 11, 0.8, 0.8) # 0.1188
    test_pl(5, 7, 0.95, 0.8) # 0.0589
