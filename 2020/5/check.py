#!/usr/local/bin/python3

def getRowNumber(ticket):
    row = ticket[0:7]
    binRow = ''.join(['0' if c == "F" else '1' for c in row])
    return int(binRow, 2)


def getColumnNumber(ticket):
    row = ticket[7:10]
    binRow = ''.join(['0' if c == "L" else '1' for c in row])
    return int(binRow, 2)


if __name__ == "__main__":
    lines = open("data.txt", "r").readlines()

    TEST_TICKET = "FBFBBFFRLR"
    assert getRowNumber(TEST_TICKET) == 44
    assert getColumnNumber(TEST_TICKET) == 5

    foundTickets = [False] * (128 * 8)

    for entry in lines:
        row = getRowNumber(entry)
        column = getColumnNumber(entry)

        foundTickets[row * 8 + column] = True

    foundSeats = [i for i, x in enumerate(foundTickets) if x]
    leftSeats = [i for i, x in enumerate(foundTickets) if not x]

    print("Last reserved seat ", foundSeats[-1])
    assert foundSeats[-1] == 906

    for seat in range(foundSeats[0], foundSeats[-1]):
        if not foundTickets[seat]:
            print("Found seat", seat)
            assert seat == 519
            break
