def print_map(x):
    print('\n'.join(''.join(x[i][j] for j in range(len(x[0]))) for i in range(len(x))))
    print()


## Puzzle #1:
f = open('/Users/mailund/Projects/adventofcode/2020/11/input.txt')
x = [line.strip() for line in f.readlines()]

def local_map(x, i, j):
    seat = x[i][j]
    adjecant = [ x[i+k][j+l] for l in [-1,0,1] if 0 <= j+l < len(x[0])
                             for k in [-1,0,1] if 0 <= i+k < len(x)
                             if (l,k) != (0,0) ]
    return seat, adjecant

def update_seat(x, i, j):
    seat, adj = local_map(x, i, j)
    if seat == 'L' and '#' not in adj:      return '#'
    if seat == '#' and adj.count('#') >= 4: return 'L'
    else:                                   return x[i][j]

def update_map(x):
    return [[update_seat(x, i, j) for j in range(len(x[0]))] for i in range(len(x))]
    
def evolve(x, last_x = None):
    return x if x == last_x else evolve(update_map(x), x)

print(f"Puzzle #1: {sum(row.count('#') for row in evolve(x))}")



## Puzzle #2: Updates to update_seat is all it takes...
def search(x, i,j, di, dj):
    """Find the first seat in direction (dx,dy)."""
    i += di ; j += dj
    while 0 <= i < len(x) and 0 <= j < len(x[0]):
        if x[i][j] in '#L': return x[i][j]
        i += di ; j += dj

def closest_seats(x, i, j):
    return [ search(x, i, j, di, dj) for dj in [-1,0,1] 
                                     for di in [-1,0,1] if (di,dj) != (0,0) ]

def update_seat(x, i, j):
    seat, adj = x[i][j], closest_seats(x, i, j)
    if seat == 'L' and '#' not in adj:      return '#'
    if seat == '#' and adj.count('#') >= 5: return 'L'
    else:                                   return x[i][j]

print(f"Puzzle #2: {sum(row.count('#') for row in evolve(x))}")
