# /// script
# requires-python = "==3.12"
# dependencies = [
#     "pygame",
# ]
# ///

"""
Creates an animation for Day 1 of Advent of Code.
Unfinished.
"""

import math
import pygame
from pygame.locals import *

WIDTH = 600
HEIGHT = 600
RADIUS = 2 * WIDTH // 5
WHITE = (255, 252, 240)
MAGENTA = (206, 93, 151)
BLACK = (16, 15, 15)
PURPLE = (139, 126, 200)
FPS = 10

pygame.font.init()
FONT = pygame.font.Font(size=70)

rotations = []
with open("input.txt", "r") as f:
    for line in f:
        direction = line[0]  # 'L' or 'R'
        magnitude = line[1:]  # the number of ticks

        rotations.append(
            (-1 if direction == "L" else 1)
            * int(magnitude)
        )

screen = pygame.display.set_mode((WIDTH, HEIGHT))

screen.fill(WHITE)
pygame.display.flip()


def draw_dial():
    screen.fill(WHITE)
    pygame.draw.circle(
        screen,
        MAGENTA,
        (WIDTH // 2, HEIGHT // 2),
        RADIUS,
    )
    tick_x = WIDTH // 2
    tick_y = HEIGHT // 2 - RADIUS
    pygame.draw.line(
        screen,
        BLACK,
        (tick_x, tick_y - 10),
        (tick_x, tick_y + 10),
        width=7,
    )

def draw_pointer(position):
    # `position - 25` moves the 0 to the top of the dial.
    angle = (position - 25) * (2 * math.pi / 100)
    offset_x = RADIUS * math.cos(angle)
    offset_y = RADIUS * math.sin(angle)
    end_point = (
        WIDTH // 2 + offset_x,
        HEIGHT // 2 + offset_y,
    )

    pygame.draw.line(
        screen,
        BLACK,
        (WIDTH // 2, HEIGHT // 2),
        end_point,
        width=5,
    )


# Writes the part 1 and part 2 scores on the screen.
def draw_scores():
    rendered_text = FONT.render(str(part1_score), 1, BLACK)
    text_width, text_height = rendered_text.get_size()
    screen.blit(
        rendered_text,
        (
            10,
            HEIGHT - text_height,
        ),
    )

# Draw the frames of the pointer moving.
def animate_pointer(start, move):
    global part1_score

    direction = -1 if move < 0 else 1
    for tick in range(1, abs(move) + 1):
        draw_dial()
        position = (start + tick * direction) % 100
        if position == 0:
            part1_score += 1
        draw_pointer(position)
        draw_scores()
        yield  # Give pygame the opportunity to update the screen.
    # Here, we're done.

clock = pygame.time.Clock()

part1_score = 0
position = 50
current_animation = None
current_rotation_index = 0
while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    if current_animation is None:
        if current_rotation_index >= len(rotations):
            break
        rotation = rotations[current_rotation_index]
        current_rotation_index += 1
        current_animation = animate_pointer(position, rotation)

    try:
        next(current_animation)
    except StopIteration:
        position += rotation
        position %= 100
        current_animation = None

    pygame.display.flip()