f = open('/Users/mailund/Projects/adventofcode/2020/09/input.txt')
x = list(map(int, f.read().split()))
p = 25

# Just brute force the first task... it is too simple to bother
# with being smart...
from itertools import dropwhile
def find_invalid(x, p):
    def valid(i): # solution from day 01
        prev, curr = x[i-p:i], x[i]
        z = { *((curr - y) for y in prev) }
        return any(y in prev for y in z)

    i = next(dropwhile(valid, range(p, len(x))))
    return x[i]

invalid = find_invalid(x, p)
print(f"Puzzle #1: {invalid}")


def cumsum(x):
    y = x[:]
    for i in range(1,len(x)):
        y[i] += y[i - 1]
    return y

from numpy import cumsum
#print(cumsum(x)[-10:])
#print(numpy.cumsum(x)[-10:])

def weakness(x):
    cs = [0, *cumsum(x)]
    for int_len in range(len(cs), 0, -1):
        for int_start in range(len(cs) - int_len):
            if cs[int_start + int_len] - cs[int_start] == invalid:
                start = int_start
                end = int_start + int_len
                intv = x[start:end]
                return min(intv) + max(intv)

print(f"Puzzle #2: {weakness(x)}")