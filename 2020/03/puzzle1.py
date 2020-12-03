import sys

tree_map = sys.stdin.read().split('\n')[:-1] # except last line...
n, m = len(tree_map), len(tree_map[0])

def count_trees(right, down):
    i, j = 0, 0
    count = 0
    while i < n:
        if tree_map[i][j] == '#':
            count += 1
        i += down
        j = (j + right) % m
    return count

paths = [(1,1), (3,1), (5,1), (7,1), (1,2)]
counts = [count_trees(*p) for p in paths]

import math
print(math.prod(counts))
