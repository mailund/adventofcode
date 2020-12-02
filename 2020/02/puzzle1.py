import sys

def count_char(x, c):
    count = 0
    for y in x:
        if y == c:
            count += 1
    return count

count = 0
for line in sys.stdin:
    intv, let, x = line.split()
    let = let[0]
    a,b = map(int, intv.split('-'))
    if a <= count_char(x, let) <= b:
        count += 1
print(count)
