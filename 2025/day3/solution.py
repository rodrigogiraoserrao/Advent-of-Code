from itertools import pairwise  # Python 3.10+

from collections import deque
from itertools import islice

def parse_input(filepath):
    with open(filepath, "r") as f:
        banks = f.read().splitlines()
    return banks


def max_voltage(bank, n):
    best_digits = ["0"] * n

    for candidate_digits in nwise(bank, n):
        for data in enumerate(zip(best_digits, candidate_digits)):
            idx, (best_digit, candidate_digit) = data

            if best_digit < candidate_digit:
                best_digits[idx:] = candidate_digits[idx:]

    return int("".join(best_digits))


def part1(banks):
    return sum(max_voltage(bank, 2) for bank in banks)


def nwise(iterable, n):
    iterable = iter(iterable)
    window = deque(islice(iterable, n - 1), maxlen=n)
    for value in iterable:
        window.append(value)
        yield tuple(window)


def part2(banks):
    return sum(max_voltage(bank, 12) for bank in banks)

if __name__ == "__main__":
    banks = parse_input("input.txt")
    print(part1(banks))
    print(part2(banks))