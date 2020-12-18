
f = open('/Users/mailund/Projects/adventofcode/2020/18/input.txt')
expressions = [expr.replace(" ","") for expr in f.read().strip().split('\n')]

from operator import add, mul
op_tbl = {'+': add, '*': mul}

def eval_stack(stack, precedence):
    rhs = stack.pop()
    while stack:
        if precedence_table[stack[-1]] > precedence:
            break
        op = stack.pop()
        lhs = stack.pop()
        rhs = op_tbl[op](lhs,rhs)
    stack.append(rhs)

def eval_expr(expr):
    stack = []
    # The numbers are single digits, so we can
    # look at individual characters--no lexer needed
    for tok in expr:
        if tok == '(':
            stack.append(tok)
        elif tok in '+*':
            eval_stack(stack, precedence_table[tok])
            stack.append(tok)
        elif tok == ')':
            eval_stack(stack, precedence_table[')'])
            stack.pop(-2) # get rid of '('
        else:
            stack.append(int(tok))

    # End of expression
    eval_stack(stack, 1234) # 1234 is just max precedence
    return stack[-1]

precedence_table = { '+': 0, '*': 0, ')': 2, '(': 3 }
print(f"Puzzle #1: {sum( eval_expr(expr) for expr in expressions )}")
precedence_table = { '+': 0, '*': 1, ')': 2, '(': 3 }
print(f"Puzzle #2: {sum( eval_expr(expr) for expr in expressions )}")
