#!/usr/local/bin/python3
# https://adventofcode.com/2020/day/2
def validEntry(entry):
    (rules, password) = entry.strip().split(":")

    rules = rules.strip()
    password = password.strip()

    letter = rules[-1]

    print("Rules = ", rules)
    print("Password = ", password)
    print("letter = ", letter)
    (lmin,lmax) = rules[:-1].split("-")

    lmin = int(lmin)
    lmax = int(lmax)

    print("Lmin ", lmin)
    print("Lmax ", lmax)

    # lcount = password.count(letter)
    # print("Counter ", lcount)
    # if lcount >= lmin and lcount <= lmax:
    #     return True
    # else:
    #     return False

    l1 = password[lmin-1]
    l2 = password[lmax-1]

    if l1 == l2:
        return False

    if l1 == letter or l2 == letter:
        return True
    else:
        return False
if __name__ == "__main__":
    entries = open("data", "r").readlines()

    validEntries = 0
    for entry in entries:
        if validEntry(entry):
            validEntries += 1

    print("Valid entries = ", validEntries)