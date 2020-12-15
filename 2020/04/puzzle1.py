
def valid_passport(fields):
    return fields == {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'} \
        or fields == {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'}

f = open('/Users/mailund/Projects/adventofcode/2020/04/input.txt')
passports = f.read().split('\n\n')
no_valid = sum(valid_passport({ field.split(':')[0] 
                                for field in passport.split() })
               for passport in passports)
print(f"Puzzle #1: {no_valid}")
