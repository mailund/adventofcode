f = open('/Users/mailund/Projects/adventofcode/2020/13/input.txt')
depart = int(f.readline())
busses = [int(bus) for bus in f.read().strip().split(',') if bus != 'x']

# Puzzle #1: Get the earliest bus after departure...
waiting = sorted((b - depart % b, b) for b in busses)
w, b = waiting[0]
print(f"Puzzle #1: {b * w}")

# Puzzle #2: We want a number x such that b - x mod b == offset
#            (with a special case for offset 0, where x mod b = 0).
# Looks like we have to solve the chinese remainder...

f = open('/Users/mailund/Projects/adventofcode/2020/13/input.txt')
depart = int(f.readline())
busses = [(offset, int(bus))
            for offset, bus in enumerate(f.read().strip().split(','))
            if bus != 'x']

from sympy.ntheory.modular import crt 
n = [b for o,b in busses]
a = [(b - o) for o,b in busses]
x, N = crt(n, a)
print(f"Puzzle #2: {x}")

