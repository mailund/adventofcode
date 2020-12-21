
class CharRule(object):
    def __init__(self, char):
        self.char = char

class SeqRule(object):
    def __init__(self, seq):
        self.seq = list(map(int, seq))

class OrRule(object):
    def __init__(self, seq_rules):
        self.seq_rules = seq_rules

import re
def parse_rules(rules):
    RULES = {}
    for rule in rules.split('\n'):
        m = re.match(r'(\d+): "(.)', rule)
        if m:
            i, char = m.groups()
            RULES[int(i)] = CharRule(char)
        else:
            i, seqs = rule.split(':')
            seq_rules = []
            for seq in seqs.split('|'):
                seq_rules.append(SeqRule(seq.split()))
            RULES[int(i)] = OrRule(seq_rules)
    return RULES

def matches(test, RULES):
    if len(test) == 0: return False

    # Dynamic programming table
    TBL = [
        [[False] * len(test) for _ in range(len(test))]
        for _ in range(len(RULES))
    ]

    # Make the characters match the character rules
    base = { x:[] for x in "ab" }
    for k,v in RULES.items():
        if isinstance(v, CharRule):
            base[v.char].append(k)

    for i,x in enumerate(test):
        for rule in base[x]:
            print(len(TBL), len(TBL[0]), len(TBL[0][0]))
            print(i, 1, repr(rule), len(test), len(RULES))
            TBL[rule][i][1] = True

    for n in range(len(test)):
        assert False, "I might look at it later... I'm too tired of AoC right now"
    
    return False

f = open('/Users/mailund/Projects/adventofcode/2020/19/test.txt')
rules, tests = f.read().split('\n\n')
RULES = parse_rules(rules)
print(RULES)
tests = tests.split('\n')
print(f"Puzzle #1: {sum( matches(test, RULES) for test in tests )}")

RULES['8']  = OrRule([SeqRule(['42']),SeqRule(['42','8'])])
RULES['11'] = OrRule([SeqRule(['42', '31']),SeqRule(['42','11', '31'])])
print(f"Puzzle #2: {sum( matches(test, RULES) for test in tests )}")


