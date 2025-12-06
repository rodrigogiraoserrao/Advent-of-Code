"""🎄 Solution for Day 6 of Advent of Code 2025 🎄

Usage:

uv run adventofcode run 06_transposed.py
"""

from math import prod

inp = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """
part1_asserts = [
    (inp, 4277556),
]
part2_asserts = [
    (inp, 3263827),
]


def part1(inp: str) -> str | int | None:
    problems = zip(*map(str.split, inp.splitlines()))
    grand_total = 0
    for prob in problems:
        op = sum if prob[-1] == "+" else prod
        grand_total += op(map(int, prob[:-1]))
    return grand_total


def part2(inp: str) -> str | int | None:
    *numbers, ops = inp.splitlines()
    transposed = zip(*numbers)

    grand_total = 0
    for op in ops.split():
        operands = []
        for chars in transposed:
            num = "".join(chars).strip()
            if not num:
                break
            operands.append(int(num))
        func = sum if op == "+" else prod
        grand_total += func(operands)
    return grand_total
