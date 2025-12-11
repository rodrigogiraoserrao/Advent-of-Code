from itertools import chain, combinations, pairwise


_NEIGHBOURS = (
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
)

_EDGE_CHECK = {
    (0, 1): (-0.5, +0.5),
    (0, -1): (-0.5, -0.5),
    (1, 0): (+0.5, +0.5),
    (-1, 0): (-0.5, +0.5),
}


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
    print(compressed_points)
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
    top_left_most_point = max(horizontal_edges, key=lambda p: (-p[1], -p[0]))

    # We know that the point immediately _below_ `topmost_point`
    # is inside the region.
    start = (top_left_most_point[0] + 0.5, top_left_most_point[1] + 0.5)
    # Now, we floodfill the region.
    queued = [start]
    tracked = {start}

    while queued:
        x, y = queued.pop()

        for dx, dy in _NEIGHBOURS:
            nx, ny = x + dx, y + dy
            edx, edy = _EDGE_CHECK[(dx, dy)]
            ex, ey = x + edx, y + edy
            if (ex, ey) in edges or (nx, ny) in tracked:
                continue
            queued.append((nx, ny))
            tracked.add((nx, ny))

    print("Floodfill finished.")
    interior = {(round(x - 0.5), round(y - 0.5)) for x, y in tracked} - edges

    full_region = edges | interior

    largest_area = 0
    for (ax, ay), (bx, by) in combinations(points, 2):
        area = (1 + abs(ax - bx)) * (1 + abs(ay - by))
        if area <= largest_area:
            continue
        
        cax, cay = compress((ax, ay))
        cbx, cby = compress((bx, by))
        rect_edges = (
            {(x, cay) for x in range(min(cax, cbx), max(cax, cbx) + 1)}
            | {(x, cby) for x in range(min(cax, cbx), max(cax, cbx) + 1)}
            | {(cax, y) for y in range(min(cay, cby), max(cay, cby) + 1)}
            | {(cbx, y) for y in range(min(cay, cby), max(cay, cby) + 1)}
        )
        if rect_edges <= full_region:
            largest_area = area

    return largest_area


if __name__ == "__main__":
    points = parse_input("input.txt")
    print(part1(points))
    print(part2(points))