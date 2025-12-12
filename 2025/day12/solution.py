from collections import Counter
from functools import cache
from itertools import product

_ROTATE = {
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


def rotate(piece, n):
    for _ in range(n):
        piece = frozenset(_ROTATE[cell] for cell in piece)
    return piece


def rotations(piece):
    return set(
        rotate(piece, n)
        for n in range(4)
    )


def flip_horizontal(piece):
    """Flip a piece along the horizontal axis y=1."""
    return frozenset((x, 2 - y) for x, y in piece)


def flip_vertical(piece):
    """Flip a piece along the vertical axis x=1."""
    return frozenset((2 - x, y) for x, y in piece)


def print_piece(piece):
    for y in range(3):
        for x in range(3):
            print("#" if (x, y) in piece else " ", end="")
        print()


def parse_input(filepath):
    with open(filepath, "r") as f:
        *blocks, problems_str = f.read().split("\n\n")

    pieces = []
    for block in blocks:
        piece = frozenset(
            (x, y)
            for y, line in enumerate(block.splitlines()[1:])
            for x, char in enumerate(line)
            if char == "#"
        )
        variations = (
            rotations(piece)
            | rotations(flip_horizontal(piece))
            | rotations(flip_vertical(piece))
        )
        pieces.append((len(piece), variations))

        for variation in variations:
            print_piece(variation)
            print()
        print("-" * 20)

    problems = []
    for problem_line in problems_str.splitlines():
        dims, counts_str = problem_line.split(": ")
        width, height = map(int, dims.split("x"))
        counter = Counter(dict(enumerate(map(int, counts_str.split()))))  # Anže approved ✅
        problems.append((width, height, counter))


    return pieces, problems


@cache
def translate(piece, offset):
    dx, dy = offset
    return frozenset((x + dx, y + dy) for x, y in piece)


def place(pieces, width, height, counter):
    region = set(product(range(width), range(height)))

    def _place(region, counter, last_row_used, last_col_used):
        """Checks whether a certain placement is possible."""
        if counter.total() == 0:
            return True

        for y in range(last_row_used + 3):
            for x in range(last_col_used + 3):
                if (x, y) not in region:
                    continue

                for piece_idx, c in counter.items():
                    if not c:
                        continue

                    counter[piece_idx] -= 1
                    for piece_variant in pieces[piece_idx]:
                        piece = translate(piece_variant, (x, y))
                        if not piece <= region:
                            continue

                        new_region = region - piece
                        bottom = max(y for _, y in piece)
                        right = max(x for x, _ in piece)
                        can_place = _place(
                            new_region,
                            counter,
                            max(last_row_used, bottom),
                            max(last_col_used, right),
                        )
                        if can_place:
                            return True

                    counter[piece_idx] += 1

        return False

    return _place(region, counter, -1, -1)


def part1(pieces, problems):

    impossible = 0
    obvious = 0
    solvable = 0
    for width, height, counter in problems:
        print(width, height, counter)

        # --- Is this problem OBVIOUSLY solvable with a very inefficient packing?
        nr_pieces = counter.total()
        nr_3_by_3_subgrids = (width // 3) * (height // 3)
        if nr_pieces <= nr_3_by_3_subgrids:
            print("Obvious!")
            obvious += 1
            continue

        # --- Is this problem IMPOSSIBLE even if you were to cut pieces into squares?
        total_area = sum(qntty * pieces[idx][0] for idx, qntty in counter.items())
        if total_area >= width * height:
            print("Impossible!")
            impossible += 1
            continue

        pieces_without_area = [pieces_set for _, pieces_set in pieces]
        solvable += (res := place(pieces_without_area, width, height, counter))
        print(res)

    print(f"{obvious = }")
    print(f"{impossible = }")
    print(f"{solvable = }")
    
    return solvable + obvious


if __name__ == "__main__":
    pieces, problems = parse_input("input.txt")
    print(part1(pieces, problems))