#f = open('/Users/mailund/Projects/adventofcode/2020/23/input.txt')

inp = "137826495" # puzzle input
inp = "389125467" # test data
cups = list(map(int, inp))
min_cup = min(cups)
max_cup = max(cups)
n = len(cups)

def next_three(i):
    return [ (i+k) % n for k in range(1,4) ]

# Brute force with small list manipulations...
def round(cups, i):
    current_cup = cups[i]
    removed = [cups[i] for i in next_three(i)]
    remaining = [c for c in cups if c not in removed]
    
    destination = current_cup - 1
    while destination not in remaining:
        destination -= 1
        if destination < min_cup:
            destination = max_cup
    
    j = remaining.index(destination)
    remaining[j+1:j+1] = removed
    return remaining, (remaining.index(current_cup) + 1) % n

def play(cups, rounds):
    i = 0
    for _ in range(rounds):
        cups, i = round(cups, i)
    return cups

def rotation(cups, start):
    i = cups.index(start)
    return ''.join(str(cups[ (i+j+1) % n ]) for j in range(n))[:-1]

print(f"Puzzle #1: {rotation(play(cups[:], 100), 1)}")


