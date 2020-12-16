
# took about 10 min get the brute force solution implemented...
# Takes 10 secs to run. So good enough.
# Looks like Van Eck Sequence, so there probably isn't
# any simple solution

def solve(input, n):
    spoken = { n:(i+1) for i, n in enumerate(input[:-1]) }
    last = input[-1] # misnomer, since it is the current...
    for i in range(len(input), n):
        # we insert 'last' *after* we check if we
        # had spoken it before. That is the only
        # tricky part to this solution...
        curr = 0 if last not in spoken else i - spoken[last]
        spoken[last] = i ; i += 1 ; last = curr
    return last

input = [2,0,6,12,1,3]
print(f"Puzzle #1: {solve(input, 2020)}")
print(f"Puzzle #1: {solve(input, 30_000_000)}")
