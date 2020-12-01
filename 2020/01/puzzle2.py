
import sys

# brute force solution...
def brute_force(x):
    for i in range(len(x)):
        for j in range(i):
            for k in range(j):
                if x[i] + x[j] + x[k] == 2020:
                    return x[i] * x[j] * x[k]
    assert False, "Shouldn't reach here"

x = list(map(int, sys.stdin.read().split()))
print(brute_force(x))
