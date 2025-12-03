from collections import deque
from itertools import pairwise, islice


def parse_input(filepath):
    with open(filepath, "r") as f:
        banks = f.read().splitlines()
    return banks


def max_joltage_bank(bank):
    digits = ["0", "0"]
    for tens, units in pairwise(bank):
        if tens > digits[0]:
            digits = [tens, units]
        elif units > digits[1]:
            digits[1] = units
    return int("".join(digits))


def nwise(iterable, n):
    iterable = iter(iterable)
    window = deque(islice(iterable, n - 1), maxlen=n)
    for value in iterable:
        window.append(value)
        yield tuple(window)


def max_joltage(bank, n):
    digits = ["0"] * n
    for possible_digits in nwise(bank, n):
        for idx, (digit, pdigit) in enumerate(zip(digits, possible_digits)):
            if pdigit > digit:
                digits[idx:] = possible_digits[idx:]
                break
    return int("".join(digits))


def part1(banks):
    return sum(max_joltage_bank(bank) for bank in banks)


def part2(banks):
    return sum(max_joltage(bank, 12) for bank in banks)


if __name__ == "__main__":
    banks = parse_input("input.txt")
    print(part1(banks))
    print(part2(banks))
