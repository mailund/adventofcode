
class Ship(object):
    def __init__(self):
        self.wp  = 10 + 1j
        self.pos =  0 + 0j

    @property
    def manhattan_dist(self):
        return abs(self.pos.real) + abs(self.pos.imag)

    # Ops...
    def N(self, amount): self.wp += amount*1j
    def S(self, amount): self.wp -= amount*1j
    def E(self, amount): self.wp += amount
    def W(self, amount): self.wp -= amount
    def L(self, angle):  self.wp *= 1j ** (angle // 90)
    def R(self, angle):  self.wp *= 1j ** (-angle // 90)
    def F(self, amount): self.pos += amount * self.wp

ship = Ship()
dispatcher = {op: getattr(ship, op) for op in "NSEWLRF"}

f = open('/Users/mailund/Projects/adventofcode/2020/12/input.txt')
for op in [line.strip() for line in f]:
    dispatcher[op[0]](int(op[1:]))
print(f"Puzzle #2: {round(ship.manhattan_dist)}")


