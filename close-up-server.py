#!/usr/bin/env python3.6

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets
import pymongo
import sys
from bson.json_util import dumps
from component.apis import *

logging.basicConfig()

STATE = {'value': 0}
LONLAT = {'a_lonlat': None, 'b_lonlat': None}
USERS = set()

# START DB
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["CloseUpDB2"]
mycol = mydb["TestPoisCollection"]


# CHECK DB CONNECTION
dblist = myclient.list_database_names()
if "CloseUpDB2" in dblist:
    print("CloseUpDB connected")
else:
    print("NO DATABASE")


# SAMPLE CODE
# print(myclient.list_database_names())
# collist = mydb.list_collection_names()
# print(mycol.find_one())

async def notify_state(message):
    if USERS:       # asyncio.wait doesn't accept an empty list
        await asyncio.wait([user.send(message) for user in USERS])

async def register(websocket):
    print("Client Connected")
    USERS.add(websocket)

async def unregister(websocket):
    print("Client disconnected")
    USERS.remove(websocket)

async def serve_api(websocket, path):
    global mycol
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        # await websocket.send(query_square_bound())
        async for message in websocket:
            data = json.loads(message)
            #do command
            command = data['command']
            if command == "connect()":
                print("Client Connected")
            elif command == "insert_pois":
                await notify_state(insert_pois(data['pois'],data['categories']))
            elif command =="query_square_bound":
                await notify_state(dumps({"type":"query_square_bound","response":query_square_bound(data['people_chosen'])}))    
            elif command =="query_poi":
                await notify_state(dumps({"type":"query_poi","response":query_poi(data['id'])}))
            elif command =="update_star":
                await notify_state(update_star(data['id'],data['starPoint']))
            elif command == "query_pois":
                await notify_state(dumps({"type":"query_pois","response":query_pois(data['keyWord'],data['count'],data['page'],mycol)}))
            elif command == "recommend_api":
                await notify_state(dumps({"type":"recommend_api","response":recommend_api(data['people_chosen'],data['keyWord'])}))
            elif command == "query_square_bound_and_keyword":
                await notify_state(dumps({"type":"query_square_bound_and_keyword","response":query_square_bound_and_keyword(data['people_chosen'],data['keyWord'])}))            
            
    finally:
        await unregister(websocket)

# asyncio.get_event_loop().run_until_complete(websockets.serve(serve_api, 'ec2-13-125-249-233.ap-northeast-2.compute.amazonaws.com', 49152))
asyncio.get_event_loop().run_until_complete(websockets.serve(serve_api, 'localhost', 49152))
asyncio.get_event_loop().run_forever()
