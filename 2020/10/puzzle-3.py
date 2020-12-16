
f = open('/Users/mailund/Projects/adventofcode/2020/10/test.txt')
adapters = list(sorted(map(int, f.read().split())))
charges = [0, *adapters, 3 + adapters[-1]]

# Puzzle 1
from collections import Counter
cnt = Counter(charges[i] - charges[i-1] for i in range(1,len(charges)))
print('Puzzle #1:', cnt[1] * cnt[3])

# Puzzle 2
def count_paths(charges):
    tbl = {0: 1}
    for w in charges[1:]:
        tbl[w] = sum(tbl.setdefault(v, 0) for v in range(w-3,w))
    return tbl[w]
print(f'Puzzle #2: {count_paths(charges)}')

def neighbours(w):
    return range(max(0, w - 3), w)
def count_paths(charges):
    tbl = [1] + [0] * charges[-1]
    for w in charges[1:]:
        tbl[w] = sum(tbl[v] for v in neighbours(w))
    return tbl[w]
print(f'Puzzle #2: {count_paths(charges)}')