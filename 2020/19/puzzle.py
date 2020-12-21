
import re
def parse_rules(rules):
    terminals = []
    nonterminals = []
    for rule in rules.split('\n'):
        m = re.match(r'(\d+): "(.)', rule)
        if m:
            i, char = m.groups()
            terminals.append((int(i), char))
        else:
            i, seqs = rule.split(':')
            seq_rules = []
            for seq in seqs.split('|'):
                seq_rules.append(list(map(int, seq.split())))
            nonterminals.append((i,seq_rules))
    return terminals, nonterminals

def increasing_intervals(min_length, max_length):
    """Generates increasingly large intervals, starting
    with min_length and going up to max_length."""
    for l in range(min_length, max_length + 1):
        for i in range(max_length + 1 - l):
            yield i, i + l

def partition(i, j, k):
    """Generates tuples that split the interval (i,j) into
    k partitions."""
    assert k >= 2
    if k == 2:
        yield from ((x,) for x in range(i+1, j-1))
    else:
        for l in range(i+1, j-1):
            yield from (((l,) + x) for x in partition(l, j, k - 1))



import numpy as np
def matches(test, RULES):
    term, nonterm = RULES
    dims = (len(term)+len(nonterm), len(test) + 1, len(test) + 1)
    matches = np.ndarray(dims, dtype = bool)

    for i in range(len(test)):
        for rule,x in term:
            matches[rule,i,i+1] = test[i] == x

    for i, j in increasing_intervals(2, len(test)):
        for rule, subrules in nonterm:
            
    
    return False

f = open('/Users/mailund/Projects/adventofcode/2020/19/input.txt')
rules, tests = f.read().split('\n\n')
RULES = parse_rules(rules)
tests = tests.split('\n')
print(f"Puzzle #1: {sum( matches(test, RULES) for test in tests )}")

