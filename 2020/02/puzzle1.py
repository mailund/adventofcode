f = open('/Users/mailund/Projects/adventofcode/2020/02/input.txt')
data = f.readlines()

from collections import Counter

count = 0
for line in data:
    intv, let, x = line.split()
    let = let[0]
    a,b = map(int, intv.split('-'))
    if a <= Counter(x)[let] <= b:
        count += 1
print(f"Puzzle #1: {count}")

count = 0
for line in data:
    intv, let, x = line.split()
    let = let[0]
    a,b = map(int, intv.split('-'))
    a, b = a - 1, b - 1
    if (x[a] == let) ^ (x[b] == let):
        count += 1
print(f"Puzzle #2: {count}")
