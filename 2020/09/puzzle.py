f = open('/Users/mailund/Projects/adventofcode/2020/09/input.txt')
x = list(map(int, f.read().split()))
p = 25

# Just brute force the first task... it is too simple to bother
# with being smart...
def check_sum(x,res):
    for i in range(len(x)):
        for j in range(i):
            if x[i] + x[j] == res:
                return True
    return False
for i in range(p, len(x)):
    if not check_sum(x[i-p:i], x[i]):
        print(i, x[i])
        break

# invalid: 466456641
invalid = 466456641

def acc_sum(x):
    y = [0] + x
    for i in range(1,len(x)):
        y[i] += y[i - 1]
    return y

def weakness(x):
    acc = acc_sum(x)
    for int_len in range(len(acc), 0, -1):
        for int_start in range(len(acc) - int_len):
            if acc[int_start + int_len] - acc[int_start] == invalid:
                start = int_start
                end = int_start + int_len
                intv = x[start:end]
                return min(intv) + max(intv)

print(weakness(x))