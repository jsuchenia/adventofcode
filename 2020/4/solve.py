#!/usr/local/bin/python3
# https://adventofcode.com/2020/day/4

FIELDS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]
MANDATORY = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

# Should be 140 - TBW!
class Passport:
    def __init__(self):
        self.fields = {}

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

        print("Passport valid = ", self.fields)
        return True

    def validByr(self):
        if 'byr' not in self.fields:
            return False

        byr = int(self.fields['byr'])
        if byr >= 1920 and byr <= 2002:
            print("Invalud BYR", byr)
            return True
        return False

    def validIyr(self):
        if 'iyr' not in self.fields:
            return False
        iyr = int(self.fields['iyr'])

        if iyr < 2010 or iyr > 2020:
            print("Invalud IYR", iyr)
            return False

        return True

    def validEyr(self):
        if 'eyr' not in self.fields:
            return False
        eyr = int(self.fields['eyr'])

        if eyr < 2020 or eyr > 2030:
            print("Invalid eyr ", eyr)
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
            if p >= 59 and p <= 76:
                return True
        elif suff == "cm":
            p = int(pref)
            if p >= 150 and p <= 193:
                return True

        print("Invalid HGT", hgt)
        return False

    def validHcl(self):
        VALID_CHARS = "0123456789abcdef"
        if 'hcl' not in self.fields:
            return False
        hcl = self.fields['hcl']
        if hcl[0] != '#':
            print("Invalud HCL, no hash", hcl)
            return False

        for c in hcl[1:]:
            if c not in VALID_CHARS:
                print("Invalid char in HCL", hcl)
                return False
        return True

    def validEcl(self):
        VALID_ECL = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
        if 'ecl' not in self.fields:
            return False
        ecl = self.fields['ecl']
        if ecl not in VALID_ECL:
            print("Invalid ECL", ecl)
            return False
        return True

    def validPid(self):
        VALID_PID_CHARS = "0123456789"
        if 'pid' not in self.fields:
            print("No PID in ", self.fields)
            return False
        pid = self.fields['pid']
        if len(pid) != 9:
            print("Invalid PID, wrong length", pid)
            return False
        for c in pid:
            if c not in VALID_PID_CHARS:
                print("Invalid char in PID", pid)
                return False

        return True


if __name__ == "__main__":
    lines = open("data").readlines()

    currentPassport = Passport()
    validPassports = 0
    invalidPassports = 0

    for l in lines:
        line = l.strip()
        if line == "":
            if currentPassport.isValid():
                validPassports += 1
            else:
                invalidPassports += 1
            currentPassport = Passport()
        else:
            for entry in line.split(" "):
                (key, value) = entry.split(":")
                currentPassport.addElement(key, value)

    if currentPassport.isValid():
        validPassports += 1
    else:
        invalidPassports += 1

    print("Valid passports =", validPassports)
    print("Invalid passports =", invalidPassports)
