from itertools import chain, combinations, pairwise


_NEIGHBOURS = (
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
)


def parse_input(filepath):
    with open(filepath, "r") as f:
        return [
            tuple(map(int, line.split(",")))
            for line in f
        ]


def part1(points):
    return max(
        (1 + abs(ax - bx)) * (1 + abs(ay - by))
        for (ax, ay), (bx, by) in combinations(points, 2)
    )


def part2(points):
    # Create the compressed coordinates.
    xs = sorted(set(x for x, _ in points))
    xs_to_compressed = {x: idx for idx, x in enumerate(xs)}
    ys = sorted(set(y for _, y in points))
    ys_to_compressed = {y: idx for idx, y in enumerate(ys)}

    def compress(point):
        x, y = point
        return (
            xs_to_compressed[x],
            ys_to_compressed[y],
        )

    # Now, we compress our input:
    compressed_points = [compress(point) for point in points]
    horizontal_edges = set()  # Set with all points from horizontal edges.
    vertical_edges = set()  # Set with all points from vertical edges.
    full_chain = chain(compressed_points, [compressed_points[0]])
    for (fx, fy), (tx, ty) in pairwise(full_chain):
        if fx == tx:
            vertical_edges.update(
                (fx, y) for y in range(min(fy, ty), max(fy, ty) + 1)
            )
        else:
            horizontal_edges.update(
                (x, fy) for x in range(min(fx, tx), max(fx, tx) + 1)
            )
    edges = vertical_edges | horizontal_edges
    print(len(edges))
    topmost_point = max(horizontal_edges, key=lambda p: p[1])

    # We know that the point immediately _below_ `topmost_point`
    # is inside the region.
    start = (topmost_point[0], topmost_point[1] - 1)
    print(start)
    assert start not in edges
    # Now, we floodfill the region.
    queued = [start]
    tracked = {start}
    inside = set()

    while queued:
        x, y = queued.pop()
        inside.add((x, y))
        if len(inside) % 1000 == 0:
            print(len(inside))

        for dx, dy in _NEIGHBOURS:
            nx, ny = x + dx, y + dy
            if (nx, ny) in edges or (nx, ny) in tracked:
                continue
            queued.append((nx, ny))
            tracked.add((nx, ny))


if __name__ == "__main__":
    points = parse_input("sample.txt")
    print(part1(points))
    print(part2(points))