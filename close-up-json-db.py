#!/usr/bin/env python3.6

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets
import pymongo

logging.basicConfig()

STATE = {'value': 0}
LONLAT = {'a_lonlat': None, 'b_lonlat': None}
USERS = set()

#START DB
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["CloseUpDB"]
mycol = mydb["PoisCollection"]

#CHECK DB CONNECTION
dblist = myclient.list_database_names()
if "CloseUpDB" in dblist:
    print("CloseUpDB connected")
else:
    print("NO DATABASE")


# SAMPLE CODE
# print(myclient.list_database_names())
# collist = mydb.list_collection_names()
# print(mycol.find_one())

def state_event():
    return json.dumps({'type': 'state', **STATE})


def users_event():
    return json.dumps({'type': 'users', 'count': len(USERS)})


async def notify_state():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = state_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_users():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)
    await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()


async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            # WRITE CODE 


            # SAMPLE CODE
            # if data['a_lonlat'] != None and data['b_lonlat'] != None:
            #     LONLAT['a_lonlat'] = data['a_lonlat']
            #     LONLAT['b_lonlat'] = data['b_lonlat']
            #     await notify_state()
            # else:
            #     logging.error(
            #         "unsupported event: {}", data)
    finally:
        await unregister(websocket)

asyncio.get_event_loop().run_until_complete(
    websockets.serve(counter, 'localhost', 6789))
asyncio.get_event_loop().run_forever()
