# Prolly gonna make some platformer where u do some spinny shit and yea
import pygame
import time
import os
import asyncio
import numpy as np

import frames
from constants import Colors
from client import Client
from game_utilities import Clock


class Game:
    def __init__(self, width, height):
        pygame.init()

        self.WIDTH = width
        self.HEIGHT = height

        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    async def _draw_window(self):
        self.win.fill(Colors.BLUE)

        self.canvas.draw()
        self.win.blit(self.canvas, (0, 0))

        self.color_palette.draw()
        self.win.blit(self.color_palette, (0, self.HEIGHT // 4 * 3))

        pygame.display.update()

    async def _handle_messages(self):
        for message in self.client.inbox:
            if message["action"] == "update_board":
                self.canvas.update_canvas(message["data"])

    async def _handle_requests(self):
        timestamp = time.time()

        if timestamp - self.last_board_update > 0.2:
            await self._send_board()
            self.last_board_update = timestamp

    async def _send_board(self):
        self.client.send_message({
            "action": "update_board",
            "data": self.canvas.formated_pixels
        })

    async def _main_menu(self):
        pass

    async def _play(self):
        # Network stuff
        self.client = Client("localhost", 6969)
        asyncio.create_task(self.client.connect())

        self.last_board_update = time.time()

        # Thing to draw on
        self.canvas = frames.DrawingFrame(
            self.WIDTH // 4 * 3, self.HEIGHT // 4 * 3)

        # Color selection goes here
        self.color_palette = frames.ColorFrame(
            self.WIDTH // 4 * 3, self.HEIGHT // 4)

        # Prolly will make some chat thing here

        # Main loop
        clock = Clock(60)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    await self.client.disconnect()
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        for row in self.canvas.pixels:
                            for pixel in row:
                                pixel.color = Colors.WHITE

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.color_palette.check_selection(
                        event.pos, (0, self.HEIGHT // 4 * 3))

            if pygame.mouse.get_pressed()[0]:
                self.canvas.update_pixel(
                    pygame.mouse.get_pos(), self.color_palette.selected_color)

            if pygame.mouse.get_pressed()[2]:
                self.canvas.update_pixel(pygame.mouse.get_pos(), Colors.WHITE)

            await self._handle_messages()
            await self._handle_requests()

            await self._draw_window()

            await clock.tick()

    def main(self):
        asyncio.get_event_loop().run_until_complete(self._main_menu())
        asyncio.get_event_loop().run_until_complete(self._play())


if __name__ == "__main__":
    game = Game(800, 600)
    game.main()
