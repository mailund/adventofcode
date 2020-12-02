import sys

count = 0
for line in sys.stdin:
    intv, let, x = line.split()
    let = let[0]
    a,b = map(int, intv.split('-'))
    a, b = a - 1, b - 1
    if (x[a] == let) ^ (x[b] == let):
        count += 1
print(count)
