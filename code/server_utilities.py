from aioconsole import ainput
import uuid
import os
import asyncio

from setuptools import Command


class CommandLineInterface:
    def __init__(self, server):
        self.server = server

    async def _main(self):
        os.system("clear")
        print("Command line interface is enabled.")

        while True:
            command = await ainput(">>> ")
            if command == "exit":
                exit()

            try:
                if command[0] == "_":
                    print(f"{command} is a private command.")
                    continue
                else:
                    if len(command.split()) > 1:
                        await self.__getattribute__(command.split()[0])(
                            *command.split()[1:])
                    else:
                        await self.__getattribute__(command.split()[0])()
            except IndexError:
                print("Please enter a command.")
            except AttributeError as e:
                print("Command not found.")
            except TypeError:
                print("Invalid arguments.")

            print()

    async def help(self, command=None):
        """Shows this message"""
        lines = []
        if command is None:
            lines.append("Available commands:")
            for command in dir(self):
                if command[0] != "_" and callable(self.__getattribute__(command)):
                    lines.append(
                        f"\t{command} - {self.__getattribute__(command).__doc__}")
        else:
            lines.append(
                f"{command} - {self.__getattribute__(command).__doc__}")

        print("\n".join(lines))

    async def clients(self):
        """Lists all clients"""
        print(f"Clients: {self.server.clients}")

    async def inbox(self):
        """Lists all messages in the inbox"""
        print(f"Inbox: {self.server.inbox}")

    async def send(self, message, client_id):
        """Sends a message to the client with the given id"""
        try:
            client_id = uuid.UUID(client_id)
        except ValueError:
            print("Invalid client id.")
            return

        try:
            client = self.server.clients[client_id]
        except KeyError:
            print("Client not found.")
            return

        message = {"message": message}

        await self.server._send_message(client["websocket"], message)

    async def send_all(self, message):
        """Sends a message to all clients"""
        message = {"message": message}
        await self.server._send_global_message(message)

    async def clear(self):
        """Clears the screen"""
        os.system("clear")
