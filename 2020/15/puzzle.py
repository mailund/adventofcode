
# took about 10 min get the brute force solution...
# it would take a lot longer to be smart.

def solve(input, n):
    spoken = { n:(i+1) for i, n in enumerate(input[:-1]) }
    last = input[-1] # misnomer, since it is the current...
    for i in range(len(input), n):
        # we insert 'last' *after* we check if we
        # had spoken it before. That is the only
        # tricky part to this solution...
        next = 0 if last not in spoken else i - spoken[last]
        spoken[last] = i ; i += 1 ; last = next
    return last

input = [2,0,6,12,1,3]
print(f"Puzzle #1: {solve(input, 2020)}")
print(f"Puzzle #1: {solve(input, 30000000)}")
