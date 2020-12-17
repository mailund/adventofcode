f = open('/Users/mailund/Projects/adventofcode/2020/17/input.txt')
init_map = f.read().split()

class Map(object):
    def __init__(self):
        self.map = {}
        self.x_dim = (0,0)
        self.y_dim = (0,0)
        self.z_dim = (0,0)
        self.w_dim = (0,0)

    def read_init(self, init_map):
        for i,row in enumerate(init_map):
            for j,symb in enumerate(row):
                self[i,j,0,0] = symb
        return self

    def __setitem__(self, coord, value):
        x, y, z, w = coord
        self.map[(x,y,z,w)] = value
        self.x_dim = (min(x,self.x_dim[0]), max(x+1,self.x_dim[1]))
        self.y_dim = (min(x,self.y_dim[0]), max(y+1,self.y_dim[1]))
        self.z_dim = (min(x,self.z_dim[0]), max(z+1,self.z_dim[1]))
        self.w_dim = (min(x,self.w_dim[0]), max(z+1,self.w_dim[1]))
    
    def __getitem__(self, coord):
        if coord in self.map: return self.map[coord]
        else: return '.'

    def __contains__(self, coord):
        return coord in self.map
        
    def __str__(self):
        res = []
        for w in range(*self.w_dim):
            for z in range(*self.z_dim):
                res.append(f"z = {z}, w = {w}")
                for x in range(*self.x_dim):
                    res.append(''.join(self.map[(x,y,z)] for y in range(*self.y_dim)))
                res.append('\n')
            res.append('\n')
        return '\n'.join(res)

    _NEIGHBOURS = [(i,j,k,l) for i in (-1,0,1) for j in (-1,0,1) for k in (-1,0,1) for l in (-1,0,1) if (i,j,k,l) != (0,0,0,0)]
    def neighbours(self, x, y, z, w):
        return [ self[(x+i,y+j,z+k,w+l)] for i,j,k,l in self._NEIGHBOURS ]
    def occupied_neighhbours(self, x, y, z,w):
        return self.neighbours(x,y,z,w).count('#')

    def next_map(self, rule):
        x0,x1 = self.x_dim ; x0 -= 1 ; x1 += 1
        y0,y1 = self.y_dim ; y0 -= 1 ; y1 += 1
        z0,z1 = self.z_dim ; z0 -= 1 ; z1 += 1
        w0,w1 = self.w_dim ; w0 -= 1 ; w1 += 1
        new_map = Map()
        for x in range(x0,x1):
            for y in range(y0, y1):
                for z in range(z0, z1):
                    for w in range(w0, w1):
                        new_map[x,y,z,w] = rule(self[x,y,z,w], 
                                                self.occupied_neighhbours(x,y,z,w))
        return new_map


m = Map().read_init(init_map)

def rule(pos, no_occ):
    if pos == '#':
        if no_occ in [2,3]: return '#'
        else:               return '.'
    else:
        if no_occ == 3:     return '#'
        else:               return '.'

def evolve(m, n, rule):
    for _ in range(n):
        m = m.next_map(rule)
    return m

print(list(evolve(m, 6, rule).map.values()).count('#'))


