
f = open('/Users/mailund/Projects/adventofcode/2020/01/input.txt')
x = list(map(int, f.read().split()))

def brute_force(x):
    for i in range(len(x)):
        for j in range(i):
            if x[i] + x[j] == 2020:
                return x[i] * x[j]
print(f"Puzzle #1: {brute_force(x)}")

def hash_trick(x):
    s = { 2020 - y for y in x }
    for y in x:
        if y in s:
            return y * (2020 - y)
print(f"Puzzle #1: {hash_trick(x)}")

import sys ; sys.exit()

def brute_force(x):
    for i in range(len(x)):
        for j in range(i):
            for k in range(j):
                if x[i] + x[j] + x[k] == 2020:
                    return x[i] * x[j] * x[k]
print(f"Puzzle #2: {brute_force(x)}")