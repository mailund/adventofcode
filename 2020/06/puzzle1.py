from functools import reduce
from operator import or_, and_
import string

def solve_puzzle(infile, set_update, set_init):
    return sum(len(ans) for ans in
        (reduce(
           lambda answers, ans: set_update(answers, set(ans)),
           group.split(),
           set_init
         ) for group in infile.read().split('\n\n')
        ))

def puzzle1(infile):
    return solve_puzzle(infile, or_, set())
def puzzle2(infile):
    return solve_puzzle(infile, and_, set(string.ascii_lowercase))

print('Puzzle #1:', puzzle1(open('test.txt')))
print('Puzzle #2:', puzzle2(open('test.txt')))
