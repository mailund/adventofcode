import sys

valid1 = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid'}
valid2 = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}

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

valid_hair_chars = {'a','b','c','d','e','f','0','1','2','3','4','5','6','7','8','9'}
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

def valid_passport(fields):
    keys = set(fields)
    if keys != valid1 and keys != valid2: return False
    for key, val in fields.items():
        if not validators[key](val):
            return False
    return True

passport_fields = {}
no_valid = 0
for line in (line.strip() for line in sys.stdin):
    if not line:
        if valid_passport(passport_fields):
            no_valid += 1
        passport_fields = {}
        continue

    for key, val in (x.split(':') for x in line.split()):
        passport_fields[key] = val

if valid_passport(passport_fields):
    no_valid += 1
print(no_valid)
