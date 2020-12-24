

# These are given from the puzzle by now...
min_cup = 1
max_cup = 1_000_000


def play(starting_cups):
    # Zero-index instead
    starting_cups = [x - 1 for x in starting_cups]
    cups = starting_cups + list(range(max(starting_cups) + 1, max_cup))
    
    LINK_MAP = { starting_cups[i]: i for i in range(len(starting_cups)) }
    def cup_idx(i): return LINK_MAP[i] if i in LINK_MAP else i
    
    next_links = cups[1:] + [cups[0]]
    def next_cup(cup):
        return next_links[cup_idx(cup)]
    def set_next(cup, n):
        next_links[cup_idx(cup)] = n
    
    # starting cup
    cup = cups[0]

    # Now play the game...
    for i in range(10_000_000):
        if i % 1_000_000 == 0:
            print(i)
        
        a = next_cup(cup)
        b = next_cup(a)
        c = next_cup(b)

        dest = cup
        while dest in [cup, a, b, c]:
            dest -= 1
            if dest < 0: dest = max_cup - 1

        set_next(cup, next_cup(c)) # cup's next is past the three
        set_next(c, next_cup(dest))
        set_next(dest, a)
        
        cup = next_cup(cup)

    return (1 + next_cup(0)) * (1 + next_cup(next_cup(0)))

inp = "137826495" # puzzle input
inp = "389125467" # test data
cups = list(map(int, inp))
print(f"Puzzle #2: {play(cups)}")

