from collections import Counter


def parse_input(filepath):
    with open(filepath, "r") as f:
        start_line, *splitter_lines = f

    splitter_rows = []
    for line in splitter_lines:
        splitter_pos = {idx for idx, cell in enumerate(line) if cell == "^"}
        if splitter_pos:
            splitter_rows.append(splitter_pos)

    return start_line.index("S"), splitter_rows


def part1(start, splitters):
    beams = {start}

    split_count = 0
    for splitter_positions in splitters:
        hits = beams & splitter_positions
        split_count += len(hits)
        misses = beams - hits
        # New beams are created by splitting the beams that were a hit.
        new_beams = {beam - 1 for beam in hits} | {beam + 1 for beam in hits}
        beams = misses | new_beams

    return split_count


def part2(start, splitters):
    beams = Counter()
    beams[start] = 1

    for splitter_positions in splitters:
        next_beams = Counter()

        hits = beams.keys() & splitter_positions
        for hit in hits:
            next_beams[hit - 1] += beams[hit]
            next_beams[hit + 1] += beams[hit]

        misses = beams.keys() - hits
        for miss in misses:
            next_beams[miss] += beams[miss]
        
        beams = next_beams

    return beams.total()


if __name__ == "__main__":
    start, splitters = parse_input("input.txt")
    print(part1(start, splitters))
    print(part2(start, splitters))