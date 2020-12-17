
from itertools import product
_NEIGHBOUR_OFFSETS = (-1,0,1)
_NEIGHBOURS = [(i,j,k) for i,j,k in product(*([_NEIGHBOUR_OFFSETS]*3)) if (i,j,k) != (0,0,0)]

def expand_dim(val, dim):
    return (min(val, dim[0]), max(val+1,dim[1]))

class Map(object):
    def __init__(self):
        self.map = {}
        self.x_dim = (0,0)
        self.y_dim = (0,0)
        self.z_dim = (0,0)

    def read_init(self, init_map):
        for i,row in enumerate(init_map):
            for j,symb in enumerate(row):
                self[i,j,0] = symb
        return self

    def __setitem__(self, coord, value):
        # Only store the active coordinates
        if value != '#': return
        x, y, z = coord
        self.map[(x,y,z)] = value
        self.x_dim = expand_dim(x, self.x_dim)
        self.y_dim = expand_dim(y, self.y_dim)
        self.z_dim = expand_dim(z, self.z_dim)
    
    def __getitem__(self, coord):
        # Fake infinite space
        return self.map[coord] if coord in self.map else '.'

    def __len__(self):
        # The number of active locations in the map
        return len(self.map)

    def neighbours(self, x, y, z):
        # The number of active neighbours is the number of coordinates
        # we store in the neighbourhood.
        return sum( ((x+i,y+j,z+k) in self.map) for i,j,k in _NEIGHBOURS )


def rule(pos, no_occ):
    if pos == '#': return '#' if no_occ in [2,3] else '.'
    else:          return '#' if no_occ == 3 else '.'

def grow_dim(dim):
    return (dim[0] - 1, dim[1] + 1)

def next_map(old_map):
    new_map = Map()
    x0,x1 = grow_dim(old_map.x_dim)
    y0,y1 = grow_dim(old_map.y_dim)
    z0,z1 = grow_dim(old_map.z_dim)
    for x, y, z in product(range(x0,x1), range(y0,y1), range(z0,z1)):
        new_map[x,y,z] = rule(old_map[x,y,z], old_map.neighbours(x,y,z))
    return new_map

def evolve(m, n):
    for _ in range(n):
        m = next_map(m)
    return m


f = open('/Users/mailund/Projects/adventofcode/2020/17/input.txt')
init_map = f.read().split()
m = Map().read_init(init_map)
print(f"Puzzle #1: {len(evolve(m, 6))}")
