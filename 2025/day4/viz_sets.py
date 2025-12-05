# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "pygame",
# ]
# ///


import pygame

CELL_SIZE = 8
WIDTH = CELL_SIZE * 136
HEIGHT = CELL_SIZE * 136

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

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


def draw_cell(x, y, colour, update=False):
    pygame.draw.rect(
        screen,
        colour,
        (rect := pygame.rect.Rect(
            x * CELL_SIZE,
            y * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE,
        )),
    )
    if update:
        pygame.display.update(rect)


def parse_input(filepath):
    with open(filepath, "r") as f:
        at_signs = {
            (x, y)
            for y, line in enumerate(f) for x, cell in enumerate(line)
            if cell == "@"
        }
    return at_signs

def part2(at_signs):
    may_be_removed = at_signs

    was_removed = set()
    while may_be_removed:

        to_be_removed = set()
        next_layer = set()
        for x, y in may_be_removed:
            neighbours = {
                (x + dx, y + dy)
                for dx, dy in _NEIGHBOUR_OFFSETS
                if (x + dx, y + dy) in at_signs
            }
            if len(neighbours) <= 3:
                to_be_removed.add((x, y))
                draw_cell(x, y, RED)

                next_layer.update(neighbours)
                for nx, ny in neighbours:
                    if (nx, ny) not in to_be_removed:
                        draw_cell(nx, ny, BLUE)
            else:
                draw_cell(x, y, BLACK)

        paused = True
        pygame.display.flip()
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    paused = False

        at_signs -= to_be_removed
        was_removed |= to_be_removed  # was_removed = was_removed | to_be_removed
        may_be_removed = next_layer & at_signs
        for x, y in to_be_removed:
            draw_cell(x, y, WHITE)
        pygame.display.flip()

    return len(was_removed)


screen = pygame.display.set_mode((WIDTH, HEIGHT))


if __name__ == "__main__":
    at_signs = parse_input("input.txt")
    screen.fill(WHITE)
    for x, y in at_signs:
        draw_cell(x, y, BLACK)
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

    print(part2(at_signs))