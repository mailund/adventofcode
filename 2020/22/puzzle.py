f = open('/Users/mailund/Projects/adventofcode/2020/22/input.txt')

def parse_player(player):
    return tuple(map(int, player.strip().split('\n')[1:]))
player1, player2 = map(parse_player, f.read().split('\n\n'))

def play(p1, p2):
    while p1 and p2:
        if p1[0] > p2[0]:
            p1 += (p1[0],p2[0])
        else:
            p2 += (p2[0],p1[0])
        p1, p2 = p1[1:], p2[1:]
    return p1 if p1 else p2

winner = play(player1, player2)
result = sum((i+1)*x for i,x in enumerate(reversed(winner)))
print(f"Puzzle #1: {result}")

def play(p1, p2, s1, s2):
    while p1 and p2:
        if p1 in s1 or p2 in s2:
            return 1, p1
        s1.add(p1)
        s2.add(p2)

        card1,card2 = p1[0],p2[0]
        p1, p2 = p1[1:], p2[1:]

        winner = None
        if card1 > len(p1) or card2 > len(p2):
            winner = 1 if card1 > card2 else 2
        else:
            winner,_ = play(p1[:card1], p2[:card2], set(), set())

        if winner == 1:    
            p1 += (card1,card2)
        else:
            p2 += (card2,card1)
        
    return (1,p1) if p1 else (2,p2)

_, winner = play(player1, player2, set(), set())
result = sum((i+1)*x for i,x in enumerate(reversed(winner)))
print(f"Puzzle #2: {result}")

        
