#!/usr/bin/env python3.6

import asyncio
import websockets


async def hello():
    async with websockets.connect('ws://ec2-13-59-71-223.us-east-2.compute.amazonaws.com:49152') as websocket:
        name = input("what is your name ? ")

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
