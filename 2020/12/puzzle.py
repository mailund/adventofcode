from math import cos, sin, pi
class Position(object):
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.angle = 0.0 # facing east

    @property
    def manhattan_dist(self):
        return abs(self.x) + abs(self.y)

    # Ops...
    def N(self, amount): self.y += amount
    def S(self, amount): self.y -= amount
    def E(self, amount): self.x += amount
    def W(self, amount): self.x -= amount
    def L(self, angle):  self.angle += pi * angle / 180.0 # use radiants
    def R(self, angle):  self.L(-angle) # subtraction, because we turn right...
    def F(self, amount):
        self.x += amount * cos(self.angle)
        self.y += amount * sin(self.angle)

pos = Position()
dispatcher = {op: getattr(pos, op) for op in "NSEWLRF"}

f = open('/Users/mailund/Projects/adventofcode/2020/12/input.txt')
for op in [line.strip() for line in f]:
    dispatcher[op[0]](int(op[1:]))
print(f"Puzzle #1: {int(pos.manhattan_dist)}")


