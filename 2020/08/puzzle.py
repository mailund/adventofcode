with open('/Users/mailund/Projects/adventofcode/2020/08/input.txt') as f:
    prog = [tuple(cast(x) for cast,x in zip((str,int), inst.split()))
            for inst in f.readlines()]

class State(object):
    def __init__(self):
        self.instp = 0 # instruction pointer
        self.acc_ = 0  # accumulator
    def nop(self, operand):
        self.instp += 1
    def acc(self, operand):
        self.acc_ += operand
        self.instp += 1
    def jmp(self, operand):
        self.instp += operand

def run_prog(prog):
    visited = set()
    state = State()
    ops = {op: getattr(state,op) for op in dir(State) if not op.startswith('__')}
    while state.instp < len(prog):
        if state.instp in visited: return state.acc_
        visited.add(state.instp)
        op, operand = prog[state.instp]
        ops[op](operand)

print(f"Puzzle #1: {run_prog(prog)}")


def run_prog(prog):
    visited = set()
    state = State()
    ops = {op: getattr(state,op) for op in dir(State) if not op.startswith('__')}
    while state.instp < len(prog):
        if state.instp in visited: return ('Abort', state.acc_)
        visited.add(state.instp)
        op, operand = prog[state.instp]
        ops[op](operand)
    return ('Success', state.acc_)

def alternative_progs(prog):
    for i, (op, operand) in enumerate(prog):
        if op == 'nop':
            prog[i] = ('jmp', operand)
            yield prog
            prog[i] = ('nop', operand)
        if op == 'jmp':
            prog[i] = ('nop', operand)
            yield prog
            prog[i] = ('jmp', operand)

for alt_prog in alternative_progs(prog[:]):
    res, acc = run_prog(alt_prog)
    if res == 'Success':
        print(f"Puzzle #2: {acc}")
        break

# hack for non-local return
class CallCC(Exception):
    def __init__(self, resval):
        self.resval = resval

def callcc(f, *args):
    try:
        f(*args)
    except CallCC as x:
         return x.resval

def locate_index(prog, seen, i, j):
    if i == len(prog): raise CallCC(j)
    if i in seen: return

    seen.add(i)
    op, operand = prog[i]
    if op == 'acc':
        locate_index(prog, seen, i+1, j)
    elif op == 'nop':
        locate_index(prog, seen, i + 1, j)
        # switch to jmp
        if j is None:
            locate_index(prog, seen, i + operand, i)
    else: # op is jmp
        locate_index(prog, seen, i + operand, j)
        # switch to nop
        if j is None:
            locate_index(prog, seen, i + 1, i)
    seen.remove(i)

def change_index(prog):
    idx = callcc(locate_index, prog, set(), 0, None)
    op, operand = prog[idx]
    if op == 'nop': prog[idx] = 'jmp', operand
    else:           prog[idx] = 'nop', operand

change_index(prog)
print(f"Puzzle #2: {run_prog(prog)}")
