#!/usr/bin/env python3.6

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets
import pymongo
import sys
from bson.json_util import dumps

logging.basicConfig()

STATE = {'value': 0}
LONLAT = {'a_lonlat': None, 'b_lonlat': None}
USERS = set()

# START DB
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["CloseUpDB"]
mycol = mydb["TestPoisCollection"]


# CHECK DB CONNECTION
dblist = myclient.list_database_names()
if "CloseUpDB" in dblist:
    print("CloseUpDB connected")
else:
    print("NO DATABASE")


# SAMPLE CODE
# print(myclient.list_database_names())
# collist = mydb.list_collection_names()
# print(mycol.find_one())

def state_event(squareBound):
    global mycol
    maxLat = squareBound[0]
    minLat = squareBound[1]
    maxLon = squareBound[2]
    minLon = squareBound[3]
    myquery = {"lat":{"$gt":minLat, "$lt":maxLat},"lon":{"$gt":minLon,"$lt":maxLon}}
    result = mycol.find(myquery)
    # for poi in result:
    #     # print(poi)
    #     markers.append([poi['lon'],poi['lat']])
    # # return json.dumps({'type': 'state', **STATE})
    return dumps(result)


async def notify_state(squareBound):
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = state_event(squareBound)
        # for user in USERS:
        #     user.send(message) 
        await asyncio.wait([user.send(message) for user in USERS])



async def register(websocket):
    USERS.add(websocket)


async def unregister(websocket):
    USERS.remove(websocket)


async def counter(websocket, path):
    global mycol
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        # await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            maxLat = 0
            minLat = sys.maxsize
            maxLon = 0
            minLon = sys.maxsize

            # WRITE CODE
            # insert if does not exist 
            for poi in data['pois']:
                #check if poi exists in collecion
                poiexist = mycol.find({"key":poi[0]}).limit(1).count()
                if poiexist:
                    continue
                #update if no poi in collection 
                myquery = { "key": poi[0] }
                newvalues = { "$set": { "lon": poi[1]['lon'],"lat":poi[1]['lat'] } }
                mycol.update_one(myquery,newvalues,True)
            for person in data['persons']:
                # print(person)
                maxLat = max(person['lat'],maxLat)
                minLat = min(person['lat'],minLat)
                maxLon = max(person['lon'],maxLon)
                minLon = min(person['lon'],minLon)

            squareBound = [maxLat,minLat,maxLon,minLon]
            await notify_state(squareBound)
            
            # SAMPLE CODE
            # mycol.insert_many(data['persons'])
            # mycol.insert_many(data['pois'])
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
