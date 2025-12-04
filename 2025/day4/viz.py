# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "pygame",
# ]
# ///


import pygame

with open("input.txt", "r") as f:
    grid = [
        list(line.strip())
        for line in f
    ]

CELL_SIZE = 8
WIDTH = CELL_SIZE * len(grid[0])
HEIGHT = CELL_SIZE * len(grid)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

_NEIGHBOUR_OFFSETS = (
    (-1, -1),
    (0, -1),
    (1, -1),
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
)

screen = pygame.display.set_mode((WIDTH, HEIGHT))


def draw_grid(grid):
    """Draw a white grid with @ signs in black."""
    screen.fill(WHITE)
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "@":
                pygame.draw.rect(
                    screen,
                    BLACK,
                    pygame.rect.Rect(
                        x * CELL_SIZE,
                        y * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE
                    )
                )


draw_grid(grid)
pygame.display.flip()

# Wait for the user to press S
start = False
while not start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            start = True


grid_height = len(grid)
grid_width = len(grid[0])
while True:
    to_be_removed = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != "@":
                continue

            neighbours = 0
            for dx, dy in _NEIGHBOUR_OFFSETS:
                nx, ny = x + dx, y + dy
                if 0 <= nx < grid_width and 0 <= ny < grid_height and grid[ny][nx] == "@":
                    neighbours += 1
            if neighbours <= 3:
                to_be_removed.append((x, y))
                # Draw this cell in red.
                cell_rect = pygame.rect.Rect(
                    x * CELL_SIZE,
                    y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                )
                pygame.draw.rect(screen, RED, cell_rect)
                pygame.display.update(cell_rect)

    if not to_be_removed:
        break

    for x, y in to_be_removed:
        grid[y][x] = "."
        # Draw this cell in white.
        cell_rect = pygame.rect.Rect(
            x * CELL_SIZE,
            y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE,
        )
        pygame.draw.rect(screen, WHITE, cell_rect)
        pygame.display.update(cell_rect)