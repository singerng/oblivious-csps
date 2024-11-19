"""
Output superoblivious ratios for Max-kAND, k=2..12, and PL sigmoid ratios
for k=2,3,4,5 which exceed the superoblivious ratios.

By Noah Singer <ngsinger@cs.cmu.edu>, May 2023
"""

# 
# PL sigmoid ratios should exceed

from examples import pl_sigmoid_ratio, superobl_ratio

# output superoblivious ratios vs. perturbed superoblivious ratios
for k in range(2, 12):
    superobl_ratio(k)

# output ratios from piecewise linear rounding vectors
pl_sigmoid_ratio(2, 200, 0.5, 1.0) # 0.4844
pl_sigmoid_ratio(3, 30, 0.7, 1.0)  # 0.2417
pl_sigmoid_ratio(4, 11, 0.8, 0.8)  # 0.1188
pl_sigmoid_ratio(5, 7, 0.95, 0.8)  # 0.0589
