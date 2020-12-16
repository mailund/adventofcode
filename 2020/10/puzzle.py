
f = open('/Users/mailund/Projects/adventofcode/2020/10/input.txt')
adapters = list(sorted(map(int, f.read().split())))
charges = [0, *adapters, 3 + adapters[-1]]

# Puzzle 1
from collections import Counter
cnt = Counter(charges[i] - charges[i-1] for i in range(1,len(charges)))
print('Puzzle #1:', cnt[1] * cnt[3])

# Puzzle 2
def count_paths(charges):
    dynprog = [None] * len(charges)
    dynprog[len(charges) - 1] = 1   # basis is one, you have to include the device
    for i in range(len(charges) - 2, -1, -1):
        # For each adaptor, check how many paths you get for each
        # valid choice of the next adaptor.
        cnt = 0
        for j in range(i+1,len(charges)):
            if charges[j] - charges[i] > 3: break
            cnt += dynprog[j]
        dynprog[i] = cnt
    return dynprog[0]
print(f'Puzzle #2: {count_paths(charges)}')

