
trans_table = str.maketrans({'F': '0', 'B': '1', 'L': '0', 'R': '1'})
def decode(x):
    return int(x.translate(trans_table), base = 2)

f = open('/Users/mailund/Projects/adventofcode/2020/05/input.txt')
x = [decode(x.strip()) for x in f]
print(f"Puzzle #1: {max(x)}")

occ_seats = set(x)
all_seats = { *range(min(x),max(x)+1) }
print(f"Puzzle #2: {(all_seats - occ_seats)}")
