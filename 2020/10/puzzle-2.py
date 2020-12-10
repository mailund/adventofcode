
f = open('/Users/mailund/Projects/adventofcode/2020/10/input.txt')
adapters = list(sorted(map(int, f.read().split())))
charges = [0, *adapters, 3 + adapters[-1]]

# Puzzle 1
from collections import Counter
cnt = Counter(charges[i] - charges[i-1] for i in range(1,len(charges)))
print('Puzzle #1:', cnt[1] * cnt[3])

# Puzzle 2
difs = ''.join([str(charges[i] - charges[i-1]) for i in range(1,len(charges))]).split('3')
print('Puzzle #2:', 2**difs.count('11') * 4**difs.count('111') * 7**difs.count('1111'))
