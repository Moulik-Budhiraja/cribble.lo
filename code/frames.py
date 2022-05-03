import pygame
from operator import add
from functools import reduce

from constants import Colors, General


class Pixel:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    @property
    def rect(self):
        return pygame.Rect(self.x * General.PIXEL_SIZE, self.y * General.PIXEL_SIZE, General.PIXEL_SIZE, General.PIXEL_SIZE)

    def __repr__(self):
        return f"Pixel({self.x}, {self.y}, {self.color})"

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def __hash__(self):
        return hash((self.x, self.y, self.color))


class DrawingFrame(pygame.Surface):
    def __init__(self, width, height):
        super().__init__((width, height))
        self.WIDTH = width
        self.HEIGHT = height

        self.generate_frame()

    @property
    def parsed_pixels(self):
        pixels = []
        for row in self.pixels:
            pixels.append(list(map(lambda pixel: pixel.color, row)))

        return pixels

    def generate_frame(self):
        self.pixels = [[Pixel(x, y, Colors.WHITE) for x in range(
            self.WIDTH // General.PIXEL_SIZE)] for y in range(self.HEIGHT // General.PIXEL_SIZE)]

        self.old_pixels = set()

    def update_pixel(self, pos, color, canvas_pos=(0, 0)):
        try:
            self.pixels[(pos[1] - canvas_pos[1]) // General.PIXEL_SIZE][(pos[0] - canvas_pos[0]) //
                                                                        General.PIXEL_SIZE].color = color
        except IndexError:
            pass

    def draw(self):
        new_pixels = set(reduce(add, self.pixels))

        for pixel in new_pixels - self.old_pixels:
            pixel.draw(self)

        self.old_pixels = new_pixels
