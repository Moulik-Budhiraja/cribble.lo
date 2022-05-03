import time
import asyncio


class Clock:
    def __init__(self, fps=60):
        self.fps = fps

        self.last_tick = 0

    async def tick(self):
        if 1 / self.fps - (time.time() - self.last_tick) > 0:
            await asyncio.sleep(1 / self.fps - (time.time() - self.last_tick))

        self.last_tick = time.time()
