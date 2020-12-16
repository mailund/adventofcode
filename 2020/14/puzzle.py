import re
f = open('/Users/mailund/Projects/adventofcode/2020/14/small-input.txt')
program = f.readlines()

class Mask(object):
    def __init__(self, mask):
        self.zero_mask, self.one_mask = ~0, 0
        for i,b in mask:
            if b == '1': self.one_mask |= (1 << i)
            else:        self.zero_mask &= ~(1 << i)
    def __call__(self, val):
        return (val & self.zero_mask) | self.one_mask

def run_prog_1(program):
    mask = Mask(())
    mem = {}
    for inst in program:
        if inst.startswith('mask'):
            parsed_mask = [(i,b) for i,b in enumerate(reversed(inst.split()[-1])) if b != 'X']
            mask = Mask(parsed_mask)
        else:
            addr, val = map(int, re.match(r"mem\[(\d*)\] = (\d*)", inst).groups())
            mem[addr] = mask(val)
    return mem

print(f"Puzzle #1: {sum(run_prog_1(program).values())}")

# damned it, I will brute force this shit...
def powerset(x):
    res = []
    for i in range(2**len(x)):
        s = [] # the set
        for j, b in enumerate(reversed(bin(i))):
            if b == '1': s.append(x[j])
        # the complement
        c = [j for j in x if j not in s]
        # and the masks...
        ones, zeros = 0, ~0
        for j in s: ones |= (1 << j)
        for j in c: zeros &= ~(1 << j)
        res.append((ones,zeros))
    return res

class Mask(object):
    def __init__(self, mask):
        self.one_mask = 0
        self.floating = []
        for i,b in enumerate(reversed(mask)):
            if b == '1': self.one_mask |= (1 << i)
            if b == 'X': self.floating.append(i)
        self.masks = [
            (self.one_mask | one_mask, zero_mask)
            for one_mask, zero_mask in powerset(self.floating)
        ]
       
    def __call__(self, addr):
        for one_mask, zero_mask in self.masks:
            yield (addr | one_mask) & zero_mask

def run_prog_2(program):
    mask = Mask(())
    mem = {}
    for inst in program:
        if inst.startswith('mask'):
            mask = Mask(inst.split()[-1])
        else:
            addr, val = map(int, re.match(r"mem\[(\d*)\] = (\d*)", inst).groups())
            for masked_addr in mask(addr):
                mem[masked_addr] = val
    return mem

print(f"Puzzle #2: {sum(run_prog_2(program).values())}")


def run_prog_2_(program):
    mem = {}
    for inst in program:
        if inst.startswith('mask'):
            mask = inst.split()[-1]
        else:
            addr, val = map(int, re.match(r"mem\[(\d*)\] = (\d*)", inst).groups())
            addr = bin(addr).zfill(36)
            masked_addr = ''.join(m if m in 'X1' else b for m,b in zip(mask, addr))
            mem[masked_addr] = val * 2**masked_addr.count('X')
    return mem

print(f"Puzzle #2: {sum(run_prog_2_(program).values())}")


masks = [inst.split()[-1] for inst in program if inst.startswith('mask')]


def transpose(x):
    return [[y[j] for y in x] for j in range(len(x[0]))]
print([*map(set, transpose(masks))])
