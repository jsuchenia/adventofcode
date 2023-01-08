#!/usr/local/bin/python3
# https://adventofcode.com/2020/day/4

MANDATORY = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}

class Passport:
    def __init__(self):
        self.fields = {}

    def mandatoryFields(self):
        return len(MANDATORY.difference(frozenset(self.fields.keys()))) == 0

    def addElement(self, key, value):
        self.fields[key] = value

    def isValid(self):
        if not self.validByr():
            return False
        if not self.validIyr():
            return False
        if not self.validEyr():
            return False
        if not self.validHgt():
            return False
        if not self.validHcl():
            return False
        if not self.validEcl():
            return False
        if not self.validPid():
            return False

        return True

    def validByr(self):
        if 'byr' not in self.fields:
            return False

        byr = int(self.fields['byr'])
        if 1920 <= byr <= 2002:
            return True
        return False

    def validIyr(self):
        if 'iyr' not in self.fields:
            return False
        iyr = int(self.fields['iyr'])

        if iyr < 2010 or iyr > 2020:
            return False

        return True

    def validEyr(self):
        if 'eyr' not in self.fields:
            return False
        eyr = int(self.fields['eyr'])

        if eyr < 2020 or eyr > 2030:
            return False

        return True

    def validHgt(self):
        if 'hgt' not in self.fields:
            return False
        hgt = self.fields['hgt']
        suff = hgt[-2:]
        pref = hgt[:-2]

        if suff == "in":
            p = int(pref)
            if 59 <= p <= 76:
                return True
        elif suff == "cm":
            p = int(pref)
            if 150 <= p <= 193:
                return True

        return False

    def validHcl(self):
        VALID_CHARS = "0123456789abcdef"
        if 'hcl' not in self.fields:
            return False
        hcl = self.fields['hcl']
        if hcl[0] != '#':
            return False

        for c in hcl[1:]:
            if c not in VALID_CHARS:
                return False
        return True

    def validEcl(self):
        VALID_ECL = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
        if 'ecl' not in self.fields:
            return False
        ecl = self.fields['ecl']
        if ecl not in VALID_ECL:
            return False
        return True

    def validPid(self):
        VALID_PID_CHARS = "0123456789"
        if 'pid' not in self.fields:
            return False
        pid = self.fields['pid']
        if len(pid) != 9:
            return False
        for c in pid:
            if c not in VALID_PID_CHARS:
                return False

        return True

def check(filename):
    lines = open(filename).read().splitlines()

    passports = []
    currentPassport = Passport()

    for line in lines:
        if line == "":
            passports.append(currentPassport)
            currentPassport = Passport()
        else:
            for entry in line.split(" "):
                (key, value) = entry.split(":")
                currentPassport.addElement(key, value)
    passports.append(currentPassport)

    validPassports = [passport.isValid() for passport in passports].count(True)
    invalidPassports = [passport.isValid() for passport in passports].count(False)
    filledPassports = [passport.mandatoryFields() for passport in passports].count(True)

    print(f"{filledPassports=} {validPassports=} {invalidPassports=}")
    return filledPassports, validPassports

def test_passport_example():
    assert check("example.txt") == (2, 2)

def test_passport_data():
    assert check("data.txt") == (222, 140)
