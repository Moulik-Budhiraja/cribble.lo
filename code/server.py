import websockets
import json
import asyncio
import uuid
import random

import backend


class Server:
    def __init__(self, host, port=6969, debug=False):
        self.host = host
        self.port = port

        self.inbox = []
        self.clients = {}

        self.debug = debug

    async def _send_message(self, websocket, message: dict):
        """Sends a single message to the given client"""
        await websocket.send(json.dumps(message))

    async def _send_global_message(self, message: dict, exclude: set = {}):
        """Sends a message to all clients"""
        for client_id, client in self.clients.items():
            if client_id not in exclude:
                await self._send_message(client["websocket"], message)

    async def _handle_connection(self, websocket, path):
        """Handles a single connection to the server"""
        client_id = uuid.uuid4()
        default_name = f"guest{random.randint(10000000, 99999999)}"

        self.clients[client_id] = {
            "websocket": websocket,
            "name": default_name,
            "drawing": False
        }

        if len(self.clients) == 1:
            self.clients[client_id]["drawing"] = True

        try:
            async for message in websocket:
                message = json.loads(message)
                # Add the client id to the message
                message["client_id"] = client_id
                self.inbox.append(message)

        except websockets.exceptions.ConnectionClosedError:
            # On unexpected disconnection
            # Remove the client from the clients list
            self.clients.pop(client_id)

    async def _handle_disconnect(self, message: dict):
        """Handles a disconnection from the server"""
        client_id = message["client_id"]
        self.clients.pop(client_id)

    async def _handle_messages(self):
        """Handles all messages from the server"""
        while True:
            if len(self.inbox) > 0:
                message = self.inbox.pop(0)

                if message.get("action") == "disconnect":
                    await self._handle_disconnect(message)

                elif message.get("action") == "update_board":
                    client_id = message.pop("client_id")
                    if self.clients[client_id]["drawing"]:
                        await self._send_global_message(message, {client_id})

            await asyncio.sleep(0.01)

    async def main(self):
        """Routes connections to the server"""
        async with websockets.serve(self._handle_connection, self.host, self.port):
            await asyncio.Future()

    async def start(self):
        """Starts the server"""
        if self.debug:
            from server_utilities import CommandLineInterface
            cli = CommandLineInterface(self)

            asyncio.create_task(cli._main(), name="CLI")

        messages = asyncio.create_task(
            self._handle_messages(), name="handle_messages")
        connections = asyncio.create_task(self.main(), name="main")

        await asyncio.gather(messages, connections)


if __name__ == "__main__":
    server = Server("localhost", debug=True)
    asyncio.run(server.start())
