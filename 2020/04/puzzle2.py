import sys

def year_validator(year, x, y):
    year = int(year)
    return x <= year <= y

def height_validator(height):
    if height.endswith("in"):
        height = int(height[:-2])
        return 59 <= height <= 76
    elif height.endswith("cm"):
        height = int(height[:-2])
        return 150 <= height <= 193
    else:
        return False

valid_hair_chars = { *'abcdef0123456789' }
def hair_colour_validator(hair):
    if hair[0] != '#': return False
    hair = hair[1:]
    if len(hair) != 6: return False
    for x in hair:
        if x not in valid_hair_chars:
            return False
    return True

valid_eye_colour = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}
def eye_colour_validator(eyes):
    return eyes in valid_eye_colour

def pid_validator(pid):
    if len(pid) != 9: return 0
    try:
        int(pid)
        return True
    except:
        return False

validators = {
    'byr': lambda year: year_validator(year, 1920, 2002),
    'iyr': lambda year: year_validator(year, 2010, 2020),
    'eyr': lambda year: year_validator(year, 2020, 2030),
    'hgt': height_validator,
    'hcl': hair_colour_validator,
    'ecl': eye_colour_validator,
    'pid': pid_validator,
    'cid': lambda x: True
}

valid1 = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'}
valid2 = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
def valid_passport(fields):
    keys = set(fields)
    if keys != valid1 and keys != valid2: return False
    for key, val in fields.items():
        if not validators[key](val):
            return False
    return True

f = open('/Users/mailund/Projects/adventofcode/2020/04/input.txt')
passports = f.read().split('\n\n')
no_valid = sum(valid_passport(dict(field.split(':') for field in passport.split()))
               for passport in passports)
print(f"Puzzle #2: {no_valid}")
