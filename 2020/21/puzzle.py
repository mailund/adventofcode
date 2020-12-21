f = open('/Users/mailund/Projects/adventofcode/2020/21/input.txt')

class IngredientsList(object):
    def __init__(self, foods, allergens):
        self.foods = foods
        self.allergens = allergens

class Food(object):
    def __init__(self, name):
        self.name = name
        self.may_contain = set()

    def add_allergens(self, allergens):
        self.may_contain.update(allergens)

class Allergen(object):
    def __init__(self, name):
        self.name = name
        self.might_be_in = None
    def add_foods(self, foods):
        if self.might_be_in is None:
            self.might_be_in = set(foods)
        else:
            self.might_be_in &= set(foods)
        
class Graph(object):
    def __init__(self):
        self.foods = {}
        self.allergens = {}
    def food(self, name):
        if name not in self.foods:
            self.foods[name] = Food(name)
        return self.foods[name]
    def allergen(self, name):
        if name not in self.allergens:
            self.allergens[name] = Allergen(name)
        return self.allergens[name]

GRAPH = Graph()
LIST = []

import re
for line in f:
    foods, allergens = re.match(r"([^\(]+) \(contains (.*)\)", line).groups()
    foods = foods.split()
    allergens = [a.strip() for a in allergens.strip().split(',')]

    for food in foods:
        GRAPH.food(food).add_allergens(GRAPH.allergen(a) for a in allergens)
    for allergen in allergens:
        GRAPH.allergen(allergen).add_foods(GRAPH.food(f) for f in foods)

    LIST.append(IngredientsList([GRAPH.food(food) for food in foods],
                                [GRAPH.allergen(a) for a in allergens]))


## PUZZLE #1 --------------------------------------------------------------
contains_allergens = set.union( *(a.might_be_in for a in GRAPH.allergens.values()) )
foods = set(GRAPH.foods.values())
no_allergens = foods - contains_allergens
count = sum((food in lst.foods) for food in no_allergens for lst in LIST)
print(f"Puzzle #1: {count}" )
    
def elimination(allergens):
    pairings = []
    while True:
        singletons = [
            a for a in allergens if len(a.might_be_in) == 1
        ]
        allergens = [
            a for a in allergens if len(a.might_be_in) > 1
        ]
        pairings.extend(singletons)

        if len(allergens) == 0:
            return pairings
        
        for s in singletons:
            food, = s.might_be_in
            for r in allergens:
                if food in r.might_be_in:
                    r.might_be_in.remove(food)

def danger_list(pairings):
    lst = sorted([
        (a.name,list(a.might_be_in)[0].name)
        for a  in pairings
    ])
    return ','.join(f for a,f in lst)

pairings = elimination(GRAPH.allergens.values())
cannonical_list = danger_list(pairings)
print(f"Puzzle #2: {cannonical_list}")

 