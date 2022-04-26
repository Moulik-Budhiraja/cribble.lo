import pygame
from constants import Colors


class Pixel:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    @property
    def rect(self):
        return pygame.Rect(self.x * 5, self.y * 5, 5, 5)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)


class DrawingFrame(pygame.Surface):
    def __init__(self, width, height):
        super().__init__((width, height))
        self.WIDTH = width
        self.HEIGHT = height

        self.generate_frame()

    def generate_frame(self, win):
        self.pixels = [[Pixel(x, y, Colors.WHITE) for x in range(
            self.WIDTH // 5)] for y in range(self.HEIGHT // 5)]

    def blit(self, *args, **kwargs):
        # Do my own stuff

        super().blit(*args, **kwargs)
