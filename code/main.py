# Prolly gonna make some platformer where u do some spinny shit and yea
import pygame
import time


class Game:
    def __init__(self):
        pygame.init()

        self.win = pygame.display.set_mode((800, 600))

    def draw_window(self, win):
        win.fill()

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()


if __name__ == "__main__":
    game = Game()
    game.main()
