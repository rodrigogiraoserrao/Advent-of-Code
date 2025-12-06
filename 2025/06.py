"""🎄 Solution for Day 6 of Advent of Code 2025 🎄

Usage:

uv run adventofcode run 06.py
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
    grand_total = 0
    op_col_idx = 0
    while op_col_idx < len(ops):
        op = sum if ops[op_col_idx] == "+" else prod
        operands = []
        col_idx = op_col_idx
        while col_idx < len(ops):
            operand = ""
            for line in numbers:
                if line[col_idx] != " ":
                    operand += line[col_idx]

            if operand:
                operands.append(int(operand))
                col_idx += 1

            if not operand or col_idx == len(ops):
                print(op, operands)
                grand_total += op(operands)
                op_col_idx = col_idx + 1
                break

    return grand_total
