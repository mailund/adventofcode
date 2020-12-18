
from itertools import product
_NEIGHBOUR_OFFSETS = (-1,0,1)
_NEIGHBOURS = [(i,j,k) for i,j,k in product(*([_NEIGHBOUR_OFFSETS]*3)) if (i,j,k) != (0,0,0)]

def expand_dim(val, dim):
    return (min(val, dim[0]), max(val+1,dim[1]))

class Map(object):
    def __init__(self):
        self.active = set()
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
        self.active.add(coord)
        self.x_dim = expand_dim(coord[0], self.x_dim)
        self.y_dim = expand_dim(coord[1], self.y_dim)
        self.z_dim = expand_dim(coord[2], self.z_dim)
    
    def __getitem__(self, coord):
        # Fake infinite space
        return '#' if coord in self.active else '.'

    def __len__(self):
        # The number of active locations in the map
        return len(self.active)

    def neighbours(self, x, y, z):
        # The number of active neighbours is the number of coordinates
        # we store in the neighbourhood.
        return sum( ((x+i,y+j,z+k) in self.active) for i,j,k in _NEIGHBOURS )


def rule(pos, no_occ):
    if pos == '#': return '#' if no_occ in [2,3] else '.'
    else:          return '#' if no_occ == 3 else '.'

def grow_dim(dim):
    return (dim[0] - 1, dim[1] + 1)

def next_map(old_map):
    new_map = Map()
    for ax,ay,az in old_map.active:
        for x,y,z in ((ax+i,ay+j,az+k) for i,j,k in _NEIGHBOURS):
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
