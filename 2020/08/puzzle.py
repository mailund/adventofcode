import sys
prog = [tuple(f(x) for f,x in zip((str,int), inst.split()))
        for inst in sys.stdin.readlines()]

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
        if state.instp in visited: return ('Abort:', state.acc_)
        visited.add(state.instp)
        op, operand = prog[state.instp]
        ops[op](operand)
    return ('Success:', state.acc_)

print(run_prog(prog))

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

for alt_prog in alternative_progs(prog):
    res, acc = run_prog(alt_prog)
    if res == 'Success:':
        print(acc)
        break

