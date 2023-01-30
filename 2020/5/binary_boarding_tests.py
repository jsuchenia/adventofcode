#!/usr/local/bin/python3
# https://adventofcode.com/2020/day/5

def get_row_number(ticket):
    row = ticket[0:7]
    binRow = ''.join(['0' if c == "F" else '1' for c in row])
    return int(binRow, 2)

def get_colum_number(ticket):
    row = ticket[7:10]
    binRow = ''.join(['0' if c == "L" else '1' for c in row])
    return int(binRow, 2)

def test_example_ticket():
    test_ticket = "FBFBBFFRLR"

    assert get_row_number(test_ticket) == 44
    assert get_colum_number(test_ticket) == 5

def check_seats(filename):
    lines = open(filename, "r").readlines()

    found_tickets = [False] * (128 * 8)

    for entry in lines:
        row = get_row_number(entry)
        column = get_colum_number(entry)

        found_tickets[row * 8 + column] = True

    found_seats = [i for i, x in enumerate(found_tickets) if x]

    print("Last reserved seat ", found_seats[-1])
    assert found_seats[-1] == 906

    for seat in range(found_seats[0], found_seats[-1]):
        if not found_tickets[seat]:
            return found_seats[-1], seat

def test_data():
    assert check_seats("data.txt") == (906, 519)
