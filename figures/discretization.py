# Code to output curves of approximation ratios given increasing discretizations

from lp import primal_lp
from examples import pl_sigmoid_ratio
k = 2

# for x_th in [149/309, 1/2]:
#     print("x_th = {}".format(x_th))
#     for l in list(range(6, 102, 5)):
#         factor = pl_sigmoid_ratio(k, l, x_th, log=False)
#         print("({},{})".format(l, factor))
#     print("~"*80)

for x_th in [1/2]:
    print("x_th = {}".format(x_th))
    for l in list(range(191, 202, 10)):
        factor = pl_sigmoid_ratio(k, l, x_th, log=True)
        print("({},{})".format(l, factor))
    print("~"*80)
