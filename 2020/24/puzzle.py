f = open('/Users/mailund/Projects/adventofcode/2020/24/input.txt')
tiles = f.read().strip().split()

def identify_tile(x):
    i, tile = 0, 0 + 0j
    while i < len(x):
        ew_step = 2
        if x[i] == 'n':
            tile += 1j
            i += 1
            ew_step = 1
        elif x[i] == 's':
            tile -= 1j
            i += 1
            ew_step = 1

        if x[i] == 'e':
            tile += ew_step
            i += 1
        else:
            assert x[i] == 'w'
            tile -= ew_step
            i += 1

    return tile

def collect_black(tiles):
    black_tiles = set()
    for x in tiles:
        tile = identify_tile(x)
        if tile in black_tiles:
            black_tiles.remove(tile)
        else:
            black_tiles.add(tile)
    return black_tiles

print(f"Puzzle #1: {len(collect_black(tiles))}")


NEIGHBOURS = [ 1+1j, 2, 1-1j, -1-1j, -2, -1+1j ]
class Floor(object):
    def __init__(self, tiles = ()):
        self.blacks = collect_black(tiles)

    def black_neighbours(self, tile):
        return sum( (tile + n) in self.blacks for n in NEIGHBOURS )

    def __iter__(self):
        for tile in self.blacks:
            yield 'B', tile, self.black_neighbours(tile)
            for n in NEIGHBOURS:
                if tile + n not in self.blacks:
                    yield 'W', tile + n, self.black_neighbours(tile + n)

    def next_floor(self):
        floor = Floor()
        for col, coord, black_n in self:
            if col == 'W' and black_n == 2:
                floor.blacks.add(coord)
            elif col == 'B' and 1 <= black_n <= 2:
                floor.blacks.add(coord)
        return floor

    def __len__(self): return len(self.blacks)

floor = Floor(tiles)
def evolve(tiles, days):
    floor = Floor(tiles)
    for _ in range(days):
        floor = floor.next_floor()
    return floor

print(f"Puzzle #2: {len(evolve(tiles, 100))}")
