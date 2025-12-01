# /// script
# requires-python = ">=3.14"
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

def draw_pointer(position):
    angle = position * (2 * math.pi / 100)
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

# Draw the frames of the pointer moving.
def animate_pointer(start, move):
    direction = -1 if move < 0 else 1
    for tick in range(1, abs(move) + 1):
        draw_dial()
        position = (start + tick * direction) % 100
        draw_pointer(position)
        yield  # Give pygame the opportunity to update the screen.
    # Here, we're done.

clock = pygame.time.Clock()

position = 50
current_animation = None
while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    if current_animation is None:
        rotation = rotations[0]
        current_animation = animate_pointer(position, rotation)

    try:
        next(current_animation)
    except StopIteration:
        break
    pygame.display.flip()