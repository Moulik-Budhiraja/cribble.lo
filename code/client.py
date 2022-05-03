import websockets
import asyncio
import json
from aioconsole import ainput


import time


class Client:
    def __init__(self, host, port=6969):
        self.host = host
        self.port = port
        self.url = f"ws://{host}:{port}"

        self.outbox = []
        self.inbox = []

        self.active = False

    async def connect(self):
        """Keeps the connection to the server alive and 
        sends messages when they are available"""
        async with websockets.connect(self.url) as websocket:
            asyncio.create_task(self.receive_messages(websocket))

            self.active = True
            while True:
                if self.outbox:
                    asyncio.create_task(self.send_messages(websocket))

                if self.active == False:
                    await self._send_message(websocket, {"action": "disconnect", "data": None})
                    await websocket.close(reason="Disconnected")

                await asyncio.sleep(0.01)

    async def disconnect(self):
        """Disconnects from the server"""
        self.active = False
        await asyncio.sleep(0.1)

    async def _send_message(self, websocket, message: dict):
        """Sends a single message to the server"""
        await websocket.send(json.dumps(message))
        # print(f"Sent: {message}\n")

    async def _receive_message(self, websocket):
        """Receives a single message from the server"""
        message = await websocket.recv()
        message = json.loads(message)
        # print(f"Received: {message}\n")
        return message

    async def send_messages(self, websocket):
        """Creates tasks to send all pending messages to the server"""
        while len(self.outbox) > 0:
            message = self.outbox.pop(0)
            asyncio.create_task(self._send_message(websocket, message))

    async def receive_messages(self, websocket):
        """Receives all messages from the server and adds them to the inbox"""
        while True:
            message = await self._receive_message(websocket)
            self.inbox.append(message)

    def send_message(self, message: dict):
        """Adds a message to the outbox"""
        self.outbox.append(message)


if __name__ == "__main__":
    client = Client("localhost")
    client.send_message({"action": "hello", "data": "world"})
    asyncio.get_event_loop().run_until_complete(client.connect())
