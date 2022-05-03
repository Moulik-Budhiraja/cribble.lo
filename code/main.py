# Prolly gonna make some platformer where u do some spinny shit and yea
import pygame
import time
import os

import frames
from constants import Colors

os.system('clear')
os.system("color")


def move(y, x):
    print("\033[%d;%dH" % (y, x))


class Game:
    def __init__(self, width, height):
        pygame.init()

        self.WIDTH = width
        self.HEIGHT = height

        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def draw_window(self):

        self.canvas.draw()
        self.win.blit(self.canvas, (0, 0))

        pygame.display.update()

    def main(self):
        self.canvas = frames.DrawingFrame(
            self.WIDTH // 4 * 3, self.HEIGHT // 4 * 3)

        last_mouse_pos = pygame.mouse.get_pos()

        clock = pygame.time.Clock()
        while True:
            start = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        for row in self.canvas.pixels:
                            for pixel in row:
                                pixel.color = Colors.WHITE

            if pygame.mouse.get_pressed()[0]:
                self.canvas.update_pixel(pygame.mouse.get_pos(), Colors.RED)

            if pygame.mouse.get_pressed()[2]:
                self.canvas.update_pixel(pygame.mouse.get_pos(), Colors.WHITE)

            self.draw_window()

            clock.tick(60)


if __name__ == "__main__":
    game = Game(800, 600)
    game.main()
