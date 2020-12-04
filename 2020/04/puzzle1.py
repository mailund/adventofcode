import sys

valid1 = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'}
valid2 = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}

def valid_passport(fields):
    return fields == valid1 or fields == valid2
    #return len(fields) == 8 or \
    #       len(fields) == 7 and 'cid' not in fields

passport_fields = set()
no_valid = 0
for line in (line.strip() for line in sys.stdin):
    if not line:
        if valid_passport(passport_fields):
            no_valid += 1
        passport_fields = set()
        continue

    for key, val in (x.split(':') for x in line.split()):
        passport_fields.add(key)

if valid_passport(passport_fields):
    no_valid += 1
print(no_valid)
