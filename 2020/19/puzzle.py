
class CharRule(object):
    def __init__(self, char):
        self.char = char
    def check(self, x, i):
        if i < len(x) and x[i] == self.char:
            yield i + 1

class SeqRule(object):
    def __init__(self, seq):
        self.seq = seq
    def check(self, x, i, r = 0):
        if r == len(self.seq):
            yield i
        else:
            for j in RULES[self.seq[r]].check(x, i):
                yield from self.check(x, j, r + 1)

class OrRule(object):
    def __init__(self, seq_rules):
        self.seq_rules = seq_rules
    def check(self, x, i):
        for rule in self.seq_rules:
            yield from rule.check(x, i)

import re
def parse_rules(rules):
    RULES = {}
    for rule in rules.split('\n'):
        m = re.match(r'(\d+): "(.)', rule)
        if m:
            i, char = m.groups()
            RULES[i] = CharRule(char)
        else:
            i, seqs = rule.split(':')
            seq_rules = []
            for seq in seqs.split('|'):
                seq_rules.append(SeqRule(seq.split()))
            RULES[i] = OrRule(seq_rules)
    return RULES

def matches(test, RULES):
    for i in RULES['0'].check(test, 0):
        if i == len(test): return True
    return False

f = open('/Users/mailund/Projects/adventofcode/2020/19/input.txt')
rules, tests = f.read().split('\n\n')
RULES = parse_rules(rules)
tests = tests.split('\n')
print(f"Puzzle #2: {sum( matches(test, RULES) for test in tests )}")

RULES['8']  = OrRule([SeqRule(['42']),SeqRule(['42','8'])])
RULES['11'] = OrRule([SeqRule(['42', '31']),SeqRule(['42','11', '31'])])
print(f"Puzzle #2: {sum( matches(test, RULES) for test in tests )}")


