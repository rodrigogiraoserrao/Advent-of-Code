"""🎄 Solution for Day 12 of Advent of Code 2025 🎄

Usage:

uv run adventofcode run 12.py
"""

INP = """\
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""
part1_asserts = [
    (INP, 2),
]
part2_asserts = [
    (INP, None),
]


from collections import Counter
from functools import cache
from itertools import product


type Point = tuple[int, int]
type Piece = frozenset[Point]


_ROTATE: dict[Point, Point] = {
    (0, 0): (2, 0),
    (1, 0): (2, 1),
    (2, 0): (2, 2),
    (0, 1): (1, 0),
    (1, 1): (1, 1),
    (2, 1): (1, 2),
    (0, 2): (0, 0),
    (1, 2): (0, 1),
    (2, 2): (0, 2),
}


def rotate(base_piece: Piece, n: int) -> Piece:
    """Rotates a piece 90 degrees clockwise."""
    if not n:
        return base_piece
    return rotate(frozenset(_ROTATE[p] for p in base_piece), n - 1)


def rotations(base_piece: Piece) -> set[Piece]:
    """Returns a set with the unique rotations of a piece."""
    return set(rotate(base_piece, n) for n in range(4))


def flip_horizontal(base_piece: Piece) -> Piece:
    """Flip a piece along the horizontal axis y=1."""
    return frozenset((x, 2 - y) for x, y in base_piece)


def flip_vertical(base_piece: Piece) -> Piece:
    """Flip a piece along the vertical axis x=1."""
    return frozenset((2 - x, y) for x, y in base_piece)


def print_piece(piece: Piece) -> None:
    """Prints a piece."""
    for y in range(max(y for _, y in piece) + 1):
        for x in range(max(x for x, _ in piece) + 1):
            print("#" if (x, y) in piece else " ", end="")
        print()


@cache
def translate(piece: Piece, point: Point) -> Piece:
    """Translates a piece by a given offset."""
    dx, dy = point
    return frozenset((x + dx, y + dy) for x, y in piece)


def place(
    width: int, height: int, counts: Counter[int], pieces: list[set[Piece]]
) -> bool:
    region: set[Point] = set(product(range(width), range(height)))

    def _place(region: set[Point], counts: Counter[int], last_used_row: int, last_used_column: int) -> bool:
        if counts.total() == 0:
            return True

        for y in range(last_used_row + 3):
            for x in range(last_used_column + 3):
                if (x, y) not in region:
                    continue
                for piece, c in counts.items():
                    if not c:
                        continue
                    counts[piece] -= 1
                    for variant in pieces[piece]:
                        translated = translate(variant, (x, y))
                        if not translated <= region:
                            continue
                        new_region = region - translated
                        bottom = max(y for _, y in translated)
                        right = max(x for x, _ in translated)
                        can_place = _place(
                            new_region,
                            counts,
                            max(bottom, last_used_row),
                            max(right, last_used_column),
                        )
                        if can_place:
                            return True
                    counts[piece] += 1

        return False

    return _place(region, counts, -1, -1)


def part1(inp: str) -> str | int | None:
    *blocks, problems_str = inp.split("\n\n")

    piece_areas: list[int] = []
    pieces: list[set[Piece]] = []  # Stores each piece and its variants.
    for block in blocks:
        base_piece: Piece = frozenset(
            (x, y)
            for y, line in enumerate(block.splitlines()[1:])
            for x, char in enumerate(line)
            if char == "#"
        )
        variants: set[Piece] = (
            rotations(base_piece)
            | rotations(flip_horizontal(base_piece))
            | rotations(flip_vertical(base_piece))
        )
        piece_areas.append(len(base_piece))
        pieces.append(variants)

    problems: list[tuple[int, int, Counter[int]]] = []
    for line in problems_str.splitlines():
        dims, nums = line.split(": ")
        counter: Counter[int] = Counter(
            {idx: int(num) for idx, num in enumerate(nums.split())}
        )
        width, height = map(int, dims.split("x"))
        problems.append((width, height, counter))

    done = 0
    impossible = 0
    have_to_solve: list[tuple[int, int, Counter[int]]] = []
    for width, height, counter in problems:
        if (width // 3) * (height // 3) >= counter.total():
            # print("Solved.")
            done += 1
        elif width * height < sum(
            count * piece_areas[piece] for piece, count in counter.items()
        ):
            impossible += 1
            # print("Impossible.")
        else:
            have_to_solve.append((width, height, counter))
    print(f"Done: {done}, impossible: {impossible}, to solve: {len(have_to_solve)}.")

    can_solve = 0
    for width, height, counter in have_to_solve:
        print(width, height, counter)
        can_solve += place(width, height, counter, pieces)

    return done + can_solve


def part2(inp: str) -> str | int | None:
    return None
