"""🎄 Solution for Day 3 of Advent of Code 2025 🎄

Usage:

uv run adventofcode run 03.py
"""

inp = """987654321111111
811111111111119
234234234234278
818181911112111"""
part1_asserts = [
    (inp, 357),
]
part2_asserts = [
    (inp, 3121910778619),
]

from itertools import pairwise  # Python 3.10+

from collections import deque
from itertools import islice


def max_voltage(bank, n):
    best_digits = ["0"] * n

    for candidate_digits in nwise(bank, n):
        for data in enumerate(zip(best_digits, candidate_digits)):
            idx, (best_digit, candidate_digit) = data

            if best_digit < candidate_digit:
                best_digits[idx:] = candidate_digits[idx:]

    return int("".join(best_digits))


def part1(inp):
    banks = inp.splitlines()
    return sum(max_voltage(bank, 2) for bank in banks)


def nwise(iterable, n):
    iterable = iter(iterable)
    window = deque(islice(iterable, n - 1), maxlen=n)
    for value in iterable:
        window.append(value)
        yield tuple(window)


def part2(inp):
    banks = inp.splitlines()
    return sum(max_voltage(bank, 12) for bank in banks)
