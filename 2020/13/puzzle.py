f = open('/Users/mailund/Projects/adventofcode/2020/13/input.txt')

depart = int(f.readline())
busses = [(offset, int(bus))
            for offset, bus in enumerate(f.read().strip().split(','))
            if bus != 'x']

# Puzzle #1: Get the earliest bus after departure...
waiting = sorted([(b - depart % b, b) for _,b in busses if b is not None])
w, b = waiting[0]
print(f"Puzzle #1: {b * w}")

# Puzzle #2: We want a number x such that b - x mod b == offset
#            (with a special case for offset 0, where x mod b = 0).
# Looks like we have to solve the chinese remainder...
from math import prod
def crt(n, a):
    res, N = 0, prod(n)
    for n_i, a_i in zip(n, a):
        N_i = N // n_i
        res += a_i * pow(N_i, -1, mod = n_i) * N_i
    return res % N
 
print(f"Puzzle #2: {crt([b for o,b in busses], [(b - o) for o,b in busses])}")

from sympy.ntheory.modular import crt 
print(f"Puzzle #2: {crt([b for o,b in busses], [(b - o) for o,b in busses])[0]}")