import sys, re

bags_table = {}
for line in open('/Users/mailund/Projects/adventofcode/2020/07/input.txt'):
    bag, subbags = line.strip().split(" bags contain ")
    bags_table[bag] = []
    if subbags == "no other bags.": continue
    for sbag in [bag.strip() for bag in subbags.split(',')]:
        no, bagtype = re.match(r"(\d+) (.+) bag.*", sbag).groups()
        bags_table[bag].append((bagtype,int(no)))

from functools import cache

## Puzzle 1
@cache
def explore1(bag):
    if bag == 'shiny gold': return True
    return any(explore1(sbag) for sbag,_ in bags_table[bag])
print(f"Puzzle #1: {sum(explore1(bag) for bag in bags_table) - 1}") # -1 for the gold bag

## Puzzle 2
@cache
def explore2(bag):
    return 1 + sum(n * explore2(sbag) for sbag,n in bags_table[bag])
print(f"Puzzle #2: {explore2('shiny gold') - 1}") # -1 for the gold bag itself

