from itertools import product

A = {1,2}
B = {'X','Y'}

cartesian_product = list(product(A,B))

# 打印结果
print(f"A × B = {cartesian_product}")