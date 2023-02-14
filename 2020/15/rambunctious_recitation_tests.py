# https://adventofcode.com/2020/day/15

def playgame(startingnumbers, rounds=10):
    last_time = -1
    map = {}

    for i in range(rounds):
        if i < len(startingnumbers):
            number = startingnumbers[i]
        elif last_time >= 0:
            number = i - last_time - 1
        else:
            number = 0

        if number in map:
            last_time = map[number]
        else:
            last_time = -1
        map[number] = i
    print("Result> for {} after {} is {}".format(startingnumbers, rounds, number))
    return number

def test_number_spoken_example_1():
    assert playgame([0, 3, 6], rounds=10) == 0

def test_number_spoken_example_2():
    assert playgame([2, 1, 3], rounds=2020) == 10

def test_number_spoken_example_3():
    assert playgame([1, 3, 2], rounds=2020) == 1

def test_number_spoken_example_4():
    assert playgame([1, 2, 3], rounds=2020) == 27

def test_number_spoken_example_5():
    assert playgame([2, 3, 1], rounds=2020) == 78

def test_number_spoken_example_6():
    assert playgame([3, 2, 1], rounds=2020) == 438

def test_number_spoken_example_7():
    assert playgame([3, 1, 2], rounds=2020) == 1836

def test_number_spoken_data():
    assert playgame([1, 20, 11, 6, 12, 0], rounds=2020) == 1085

def test_number_spoken_manyrounds_example():
    assert playgame([0, 3, 6], rounds=30000000) == 175594

def test_number_spoken_manyrounds_data():
    assert playgame([1, 20, 11, 6, 12, 0], rounds=30000000) == 10652
