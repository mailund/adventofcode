f = open('/Users/mailund/Projects/adventofcode/2020/06/test.txt')
groups = f.read().split('\n\n')

res = 0
for group in groups:
    unique = set()
    for answer in group.split():
        unique.update(answer)
    res += len(unique)
print(f'Puzzle #1: {res}')

res = sum( len(set(''.join(group.split()))) for group in groups )
print(f'Puzzle #1: {res}')

from functools import reduce
from operator import or_, and_
import string

def solve_puzzle(groups, set_update, set_init):
    return sum(len(ans) for ans in
        (reduce(
           lambda answers, ans: set_update(answers, set(ans)),
           group.split(),
           set_init
         ) for group in groups)
        )

def puzzle1(infile):
    return solve_puzzle(groups, or_, set())
def puzzle2(infile):
    return solve_puzzle(groups, and_, set(string.ascii_lowercase))

print(f'Puzzle #1: {puzzle1(groups)}')
print(f'Puzzle #2: {puzzle2(groups)}')

print('--' * 5, 'take II', '-' * 20)

def solve_puzzle(groups, set_update):
    x = list(reduce(set_update, map(set, group.split()))
             for group in groups)
    print(x)
    return sum(map(len, x))


def puzzle1(infile):
    return solve_puzzle(infile, or_)
def puzzle2(infile):
    return solve_puzzle(infile, and_)

print(f'Puzzle #1: {puzzle1(groups)}')
print(f'Puzzle #2: {puzzle2(groups)}')

print('--' * 5, 'take III', '-' * 20)

def puzzle(f):
    return lambda groups: sum(
        len(f(*map(set, group.split())))
        for group in groups
    )
puzzle1 = puzzle(set.union)
puzzle2 = puzzle(set.intersection)
print(f'Puzzle #1: {puzzle1(groups)}')
print(f'Puzzle #2: {puzzle2(groups)}')
