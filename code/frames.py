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

        self.old_pixels = set()
        self.old_sent_pixels = set()

        self.generate_frame()

    @property
    def formated_pixels(self):
        new_pixels = set(reduce(add, self.pixels))
        changed_pixels = new_pixels - self.old_sent_pixels

        self.old_sent_pixels = new_pixels

        return [[pixel.x, pixel.y, pixel.color] for pixel in changed_pixels]

        pixels = []
        for row in self.pixels:
            row_pixels = []
            for pixel in row:
                row_pixels.append(pixel.color)

            pixels.append(row_pixels)

        return pixels

    def generate_frame(self):
        self.pixels = [[Pixel(x, y, Colors.WHITE) for x in range(
            self.WIDTH // General.PIXEL_SIZE)] for y in range(self.HEIGHT // General.PIXEL_SIZE)]

    def update_pixel(self, pos, color, canvas_pos=(0, 0)):
        try:
            self.pixels[(pos[1] - canvas_pos[1]) // General.PIXEL_SIZE][(pos[0] - canvas_pos[0]) //
                                                                        General.PIXEL_SIZE].color = color
        except IndexError:
            pass

    def update_canvas(self, pixels):
        for x, y, color in pixels:
            self.update_pixel((x * General.PIXEL_SIZE, y *
                              General.PIXEL_SIZE), tuple(color))

    def draw(self):
        # Only draws the pixels that have changed
        new_pixels = set(reduce(add, self.pixels))

        for pixel in new_pixels - self.old_pixels:
            pixel.draw(self)

        self.old_pixels = new_pixels


class ColorFrame(pygame.Surface):
    def __init__(self, width, height):
        super().__init__((width, height))
        self.WIDTH = width
        self.HEIGHT = height

        self.colors = {}
        self.selected_color = Colors.BLACK

        self.generate_frame()

    def generate_frame(self):
        self.colors = {
            Colors.RED: pygame.Rect(0, 0, 40, 40),
            Colors.GREEN: pygame.Rect(50, 0, 40, 40),
            Colors.BLUE: pygame.Rect(100, 0, 40, 40),
            Colors.YELLOW: pygame.Rect(150, 0, 40, 40),
            Colors.ORANGE: pygame.Rect(200, 0, 40, 40),
            Colors.PURPLE: pygame.Rect(0, 50, 40, 40),
            Colors.BROWN: pygame.Rect(50, 50, 40, 40),
            Colors.DARK_GRAY: pygame.Rect(100, 50, 40, 40),
            Colors.WHITE: pygame.Rect(150, 50, 40, 40),
            Colors.BLACK: pygame.Rect(200, 50, 40, 40)
        }

        for color, rect in self.colors.items():
            self.colors[color] = pygame.Rect(
                self.WIDTH // 2 - 240 // 2 + rect.x, self.HEIGHT // 2 - 100 // 2 + rect.y, rect.width, rect.height)

    def check_selection(self, pos, blit_pos=(0, 0)):
        for color, rect in self.colors.items():
            if rect.collidepoint((pos[0] - blit_pos[0], pos[1] - blit_pos[1])):
                self.selected_color = color

    def draw(self):
        self.fill(Colors.LIGHT_GRAY)

        for color, rect in self.colors.items():
            pygame.draw.rect(self, color, rect)
