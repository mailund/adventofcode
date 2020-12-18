
# -- Parsing the input ---------------------------------------
f = open('/Users/mailund/Projects/adventofcode/2020/16/input.txt')
rules_description, ticket, nearby = f.read().strip().split('\n\n')

# Parsing rules...
class Range(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def check(self, val):
        return self.a <= val <= self.b
    def __repr__(self):
        return f"Range({self.a}, {self.b})"

class Rule(object):
    def __init__(self, name, ranges):
        self.name = name
        self.ranges = ranges
    def check(self, val):
        return any(r.check(val) for r in self.ranges)
    def __repr__(self):
        return f"Rule({self.name},{self.ranges})"

rules = []
for line in rules_description.split('\n'):
    rule, ranges = line.split(':')
    rules.append(
        Rule(rule.strip(), [
             Range(*map(int, x.strip().split('-'))) for x in ranges.split('or')
    ]))

# Parsing my ticket
def parse_ticket(ticket):
    return list(map(int, ticket.split(',')))
my_ticket = parse_ticket(ticket.split('\n')[1])

# Parsing nearby tickets
nearby_tickets = []
for ticket in nearby.split('\n')[1:]:
    nearby_tickets.append(parse_ticket(ticket))



# -- Puzzle #1 -------------------------------------------------------
def ticket_scanning_error(tickets, rules):
    return sum(sum(field for field in ticket
                   if not any(r.check(field) for r in rules))
               for ticket in tickets)

print(f"Puzzle #1: {ticket_scanning_error(nearby_tickets, rules)}")

# -- Puzzle #2 -------------------------------------------------------
# Get the valid tickets to work with...
def check_ticket(ticket):
    return all(
        any(r.check(field) for r in rules)
        for field in ticket
    )
valid_tickets = [ *filter(check_ticket, nearby_tickets) ]

# Get the rules that each field can satisfy...
def infer_rules(tickets):
    # I want the fields, rather than the tickets, so transform...
    fields = [[ticket[j] for ticket in valid_tickets]
              for j in range(len(valid_tickets[0]))]

    # For each field, identify the candidate rules
    def candidate_rules(field):
        return { r.name for r in rules if r.check(field) }
    def satisfying_rules(fields):
        return set.intersection( *map(candidate_rules, fields) )
    field_rules = [ *enumerate(map(satisfying_rules, fields)) ]
    
    # Now start eliminating...
    field_rules.sort(key = lambda x: len(x[1]))
    for i in range(len(field_rules)):
        r, = field_rules[i][1]
        for j in range(i + 1, len(field_rules)):
            field_rules[j][1].remove(r)
    field_rules.sort() # get them back in order...

    return [ name for _,(name,) in field_rules ]

rule_names = infer_rules(valid_tickets)
print(rule_names)
indices = [i for i,r in enumerate(rule_names) if r.startswith("departure")]

from math import prod
print(f"Puzzle #2: {prod(my_ticket[i] for i in indices)}")

import heapq

# Get the rules that each field can satisfy...
def infer_rules(tickets):
    # I want the fields, rather than the tickets, so transform...
    fields = [[ticket[j] for ticket in valid_tickets]
              for j in range(len(valid_tickets[0]))]

    # For each field, identify the candidate rules
    def candidate_rules(field):
        return { r.name for r in rules if r.check(field) }
    def satisfying_rules(fields):
        return set.intersection( *map(candidate_rules, fields) )
    field_rules = [ *enumerate(map(satisfying_rules, fields)) ]

    assigned_rules = []
    while field_rules:
        singletons =  [ (i,r) for i,r in field_rules if len(r) == 1 ]
        field_rules = [ (i,r) for i,r in field_rules if len(r) > 1  ]
        assigned_rules.extend(singletons)        
        removed = set.union( *[r for i,r in singletons] )
        for _,s in field_rules:
            s -= removed

    assigned_rules.sort()
    return [ name for _,(name,) in assigned_rules ]

rule_names = infer_rules(valid_tickets)
indices = [i for i,r in enumerate(rule_names) if r.startswith("departure")]

from math import prod
print(f"Puzzle #2: {prod(my_ticket[i] for i in indices)}")