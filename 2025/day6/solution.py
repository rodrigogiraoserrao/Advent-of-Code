from itertools import groupby
from math import prod
from operator import is_not_none  # Python 3.14
# Functional version of checking `obj is not None`

def parse_input_part1(filepath):
    with open(filepath, "r") as f:
        *operands, operators_line = f

    operands = [
        map(int, row.split())
        for row in operands
    ]
    operands = zip(*operands)

    operators = [
        sum if op_char == "+" else prod
        for op_char in operators_line.split()
    ]

    return operands, operators


def part1(operands, operators):
    return sum(
        op(row)
        for row, op in zip(operands, operators)
    )


def parse_input_part2(filepath):
    with open(filepath, "r") as f:
        *operand_chars, operator_line = f

    # Transpose all the characters.
    operand_chars = zip(*operand_chars)

    operands = [
        int(string) if (string := "".join(tup).strip()) else None
        for tup in operand_chars
    ]

    # At this point, operands is [9643, 5775, None, 7, 93, ...]
    # I want to turn this into an iterable of iterables with integers
    # [9643, 5775, None, 7, 93, ...] -> [[9643, 5775], [7, 93, ...], ...]
    grouped_operands = []
    for key, group in groupby(operands, key=is_not_none):
        if key:
            grouped_operands.append(list(group))

    operators = [
        sum if op_char == "+" else prod
        for op_char in operator_line.split()
    ]

    return grouped_operands, operators


part2 = part1


if __name__ == "__main__":
    operands, operators = parse_input_part1("input.txt")
    print(part1(operands, operators))

    operands, operators = parse_input_part2("input.txt")
    print(part2(operands, operators))