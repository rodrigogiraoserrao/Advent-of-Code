# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "pygame",
# ]
# ///

from collections import Counter
from math import log

import pygame


def draw_cell(x, y, color):
    pygame.draw.rect(
        screen,
        color,
        pygame.rect.Rect(
            x * CELL_SIZE,
            y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE,
        ),
    )

with open("input.txt", "r") as f:
    input_grid = f.read().splitlines()

GRID_WIDTH = len(input_grid[0])
GRID_HEIGHT = len(input_grid)

CELL_SIZE = 6
WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(WHITE)

for y, row in enumerate(input_grid):
    for x, cell in enumerate(row):
        if cell == "^":
            draw_cell(x, y, BLACK)

pygame.display.flip()


# --- Run the simulation.
beams = Counter()
beams[input_grid[0].index("S")] = 1

# For each row:
for row_idx, row in enumerate(input_grid):
    splitter_positions = {idx for idx, cell in enumerate(row) if cell == "^"}
    next_beams = Counter()

    hits = beams.keys() & splitter_positions
    for hit in hits:
        next_beams[hit - 1] += beams[hit]
        next_beams[hit + 1] += beams[hit]

    misses = beams.keys() - hits
    for miss in misses:
        next_beams[miss] += beams[miss]
    
    beams = next_beams

    total_beams_log = log(beams.total() + 1)
    for beam_pos, beam_count in beams.items():
        beam_per = log(beam_count + 1) / total_beams_log
        red = 255
        g = b = int(255 * (1 - beam_per))
        draw_cell(beam_pos, row_idx, (red, g, b))

    pygame.display.update(
        pygame.rect.Rect(
            0,
            row_idx * CELL_SIZE,
            WIDTH,
            CELL_SIZE,
        )
    )


pygame.display.flip()
while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit()