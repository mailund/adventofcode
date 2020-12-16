from functools import cache
from itertools import takewhile

f = open('/Users/mailund/Projects/adventofcode/2020/10/test.txt')
adapters = list(sorted(map(int, f.read().split())))
charges = [0, *adapters, 3 + adapters[-1]]

# Puzzle 1
#from collections import Counter
#cnt = Counter(charges[i] - charges[i-1] for i in range(1,len(charges)))
#print('Puzzle #1:', cnt[1] * cnt[3])

# Puzzle 2
def count_paths(charges):
    def neighbours(v):
        return takewhile(lambda w: charges[w] - charges[v] <= 3,
                         range(v + 1, len(charges)))

    count = [None] * len(charges)
    count[len(charges) - 1] = 1
    for v in range(len(charges) - 2, -1, -1):
        count[v] = sum(count[w] for w in neighbours(v))

    return count[0]
print(f'Puzzle #2: {count_paths(charges)}')

def count_paths(charges):
    def neighbours(v):
        return takewhile(lambda w: charges[w] - charges[v] <= 3,
                         range(v + 1, len(charges)))
    @cache
    def count(v):
        if v == len(charges) - 1: return 1
        return sum(count(w) for w in neighbours(v))
    return count(0)
print(f'Puzzle #2: {count_paths(charges)}')
