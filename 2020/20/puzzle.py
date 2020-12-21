
def keyflip(f, d):
    return { f(k): v for k,v in d.items() }
def ewflip(x):
    if x == 'E': return 'W'
    if x == 'W': return 'E'
    else:        return x
def nsflip(x):
    if x == 'N': return 'S'
    if x == 'S': return 'N'
    else:        return x

class Tile(object):
    def __init__(self, tile_id, pixels):
        self.tile_id = tile_id
        self.pixels = pixels
        self.connections = {}

    # Border edges, north, east, south, west
    @property
    def N(self): return self.pixels[0]
    @property
    def E(self): return ''.join(line[-1] for line in self.pixels)
    @property
    def S(self): return self.pixels[-1]
    @property
    def W(self): return ''.join(line[0] for line in self.pixels)
    @property
    def edges(self): return ( (e,getattr(self,e)) for e in "NESW" )

    def connect(self, ori, other):
        # In the general case, the same edge can match more than
        # one other tile. That makes the problem harder, but
        # here we check that it doesn't happen in our input
        assert ori not in self.connections
        self.connections[ori] = other

    def rot(self, a, b):
        x = "NESW"
        r = x.index(a) - x.index(b)
        if r < 0: r += 4

        for _ in range(r): # FIXME: be smarter, Thomas
            self.pixels = [ *zip(*self.pixels[::-1]) ]
        self.pixels = [ ''.join(x) for x in self.pixels ]

        self.connections = {
            x[(i + r) % 4]: self.connections[x[i]]
            for i in range(4) 
            if x[i] in self.connections
        }

    def flip_horizontal(self):
        self.connections = keyflip(ewflip, self.connections)
        self.pixels = [ x[::-1] for x in self.pixels ]

    def flip_vertical(self):
        self.connections = keyflip(nsflip, self.connections)
        self.pixels = self.pixels[::-1]

    def __str__(self):
        return "\n".join(
            [f"{self.tile_id}", *self.pixels]
        )
    def __repr__(self):
        return f"tile {self.tile_id}"

# Parse the tiles...
import re
def parse_tiles(fname):
    with open(fname) as f:
        tiles = []
        for tile in f.read().strip().split('\n\n'):
            tile = tile.split('\n')
            tile_id, = re.match(r"Tile (\d+):",tile[0]).groups()
            tiles.append(Tile(int(tile_id), tile[1:]))
        return tiles

# Connect the tiles...
def connect_tiles(tiles):
    def connect(x, y):
        for ori_x, edge_x in x.edges:
            for ori_y, edge_y in y.edges:
                if edge_x == edge_y or edge_x == edge_y[::-1]:
                    x.connect(ori_x, y)
                    y.connect(ori_y, x)

    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            connect(tiles[i], tiles[j])

    return tiles

# Puzzle #1: get the tiles with two (four with flip) neighbours
fname = '/Users/mailund/Projects/adventofcode/2020/20/input.txt'
import math
tiles = connect_tiles(parse_tiles(fname))
corners = [ tile for tile in tiles if len(tile.connections) == 2 ]
print(f"Puzzle #1: {math.prod(tile.tile_id for tile in corners )}")





# Assemble the tiles by building from the upper left corner
def fix_east(west, east):
    ori = [k for k,v in east.connections.items() if v == west][0]
    east.rot('W', ori)
    if west.E != east.W:
        east.flip_vertical()
    assert west.E == east.W
    if 'N' in east.connections:
        assert east.N == east.connections['N'].S

def fix_south(north, south):
    ori = [k for k,v in south.connections.items() if v == north][0]
    south.rot('N', ori)
    if north.S != south.N:
        south.flip_horizontal()
    assert north.S == south.N
    
def tile_row(x):
    res = []
    while 'E' in x.connections:
        res.append(x)
        x = x.connections['E']
        fix_east(res[-1], x)
    res.append(x)
    return res

def assemble_tiles(tiles):
    x = [ # get upper left tile to start from
        tile for tile in tiles 
        if set(tile.connections.keys()) == {'E','S'} 
    ][0]

    res = []
    row = tile_row(x)
    while 'S' in row[0].connections:
        res.append(row)
        x = row[0].connections['S']
        fix_south(row[0], x)
        row = tile_row(x)
    res.append(row)
    return res

assembly = assemble_tiles(tiles)


## Building image

def remove_borders(tiles):
    for tile in tiles:
        tile.pixels = [ row[1:-1] for row in tile.pixels[1:-1] ]

remove_borders(tiles)

def insert_tile(img, tile, x, y):
    k = len(tile.pixels)
    for i in range(k):
        for j in range(k):
            img[k*x+i][k*y+j] = tile.pixels[i][j]

def build_img(assembly):
    n, m, k = len(assembly), len(assembly[0]), len(assembly[0][0].pixels)
    img = [ [' '] * (m*k) for _ in range(n*k) ]
    for x in range(n):
        for y in range(m):
            insert_tile(img, assembly[x][y], x, y)
    return img

## Now scanning for monsters

MONSTER = \
"""                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """.split('\n')
MONSTER_OFFSETS = [
    (i,j) for i in range(len(MONSTER))
          for j in range(len(MONSTER[0]))
          if MONSTER[i][j] == '#'
]

def detect_monster(img, x, y):
    return all(
        img[x + i][y + j] == '#'
        for i,j in MONSTER_OFFSETS
    )
def draw_monster(img, x, y):
    for i,j in MONSTER_OFFSETS:
        img[x + i][y + j] = 'O'

def scan_for_monsters(img):
    found = False
    n, m = len(img), len(img[0])
    nn, mm = len(MONSTER), len(MONSTER[0])
    for x in range(n - nn):
        for y in range(m - mm):
            if detect_monster(img, x, y):
                found = True
                draw_monster(img, x, y)
    return found

# Try rotations until we find something or have rotated all the way
img = build_img(assembly)

def rotate_img(img):
    return [ *map(list, zip(*img[::-1])) ]

def print_img(img):
    print('\n'.join( ''.join(row) for row in img ))

for _ in range(4):
    if scan_for_monsters(img):
        break
    img = rotate_img(img)

# It was enough with rotations for me, but potentially
# you would need flips as well...
print(f"Puzzle #2: {sum(row.count('#') for row in img)}")
