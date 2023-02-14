from collections import defaultdict

def doTask(data, firstPhase=True):
    rules, myticket, otherTickets = data.split("\n\n")

    validNumbers = defaultdict(set)
    ALL_FIELDS = []

    result = 0
    for rule in rules.splitlines():
        field, frange = rule.split(":")
        ALL_FIELDS.append(field)

        for frule in frange.split(" or "):
            start, stop = frule.strip().split('-')
            start = int(start)
            stop = int(stop)

            for x in range(start, stop + 1):
                validNumbers[x].add(field)

    fieldtitles = []
    for i in range(len(ALL_FIELDS)):
        fieldtitles.append(set(ALL_FIELDS))

    for ticket in otherTickets.splitlines()[1:]:
        invalidTicket = False
        ticketNumbers = [int(x) for x in ticket.split(",")]
        for val in ticketNumbers:
            if val not in validNumbers.keys():
                result += val
                invalidTicket = True
                break

        if invalidTicket or firstPhase:
            continue

        # Checking mappings
        for pos, val in enumerate(ticketNumbers):
            fieldtitles[pos].intersection_update(validNumbers[val])

    if firstPhase:
        print("EX1 result: ", result)
        return result

    # Normalize data.txt
    toBeValidated = set(ALL_FIELDS)
    while len(toBeValidated) > 0:
        for pos, values in enumerate(fieldtitles):
            if len(values) == 1:
                value = values.copy().pop()
                if value in toBeValidated:
                    for othherpos, otherValues in enumerate(fieldtitles):
                        if pos != othherpos:
                            otherValues.difference_update(values)
                    toBeValidated.remove(value)

    positions = [pos for pos, fields in enumerate(fieldtitles) if fields.pop().startswith("departure")]
    myticketnumbers = [int(x) for x in myticket.splitlines()[1].split(',')]

    result = 1
    for pos in positions:
        result *= myticketnumbers[pos]

    print("Ex2 result", result)
    return result

def test_error_rate_test():
    test = open("test.txt", "r").read()
    assert doTask(test) == 71

def test_error_rate_data():
    data = open("data.txt", "r").read()
    assert doTask(data) == 21956

def test_departure_multiplication_test():
    test = open("test.txt", "r").read()
    assert doTask(test, firstPhase=False) == 1

def test_deprarture_multiplication_data():
    data = open("data.txt", "r").read()
    assert doTask(data, firstPhase=False) == 3709435214239
