# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pygame",
# ]
# ///

from itertools import chain, pairwise

import pygame


with open("input.txt", "r") as f:
    points = [
        tuple(map(int, line.split(",")))
        for line in f
    ]

"""
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
points = [compress(point) for point in points]
"""

MIN_X = min(x for x, _ in points)
MAX_X = max(x for x, _ in points)
MIN_Y = min(y for _, y in points)
MAX_Y = max(y for _, y in points)

WIDTH = MAX_X + MIN_X
HEIGHT = MAX_Y + MIN_Y

surface = pygame.Surface((WIDTH // 10, HEIGHT // 10))
surface.fill((255, 255, 255))

full_chain = chain(points, [points[0]])
for start, end in pairwise(full_chain):
    pygame.draw.line(
        surface,
        (0, 0, 0),
        (start[0] // 10, start[1] // 10),
        (end[0] // 10, end[1] // 10),
        width=10,
    )

pygame.image.save(surface, "region.png")