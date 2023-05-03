"""
Testing for revealing factors for Max-kAND

By Noah Singer <ngsinger@cs.cmu.edu>, May 2023
"""

from lp import primal_lp

def unif_partition(l):
    return tuple(i/l for i in range(l+1))

def pl_rounding(t, x_th):
    return tuple(1 if x > x_th else 1/2*(1+x/x_th) for x in t[1:])

def test_pl(k, l, x_th, y_th=1.0):
    print("~"*80)
    print("Testing piecewise linear rounding, k={}, l={}, x_th={}".format(k, l, x_th))
    t = unif_partition(l)
    p = pl_rounding(t, x_th)
    print("Result: {}".format(primal_lp(k, l, t, p)))

def superobl_p(k):
    if k%2==0:
        return 1/2 + 1/(2*(k+1))
    else:
        return 1/2 + 1/(2*k)

def superobl_alpha(k):
    if k%2==0:
        return 2**(-(k - 1))*(1 - 1/(k + 1)**2)**(k/2)
    else:
        return 2**(-(k - 1))*(1 - 1/k**2)**((k - 1)/2)

def test_superobl(k, delta=0.01, eps=0.001):
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
    for k in range(2,11):
        test_superobl(k)