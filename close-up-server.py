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

def insert_pois(pois,category):
    global mycol 

    if pois is None:
        print("Failed (no pois)")
        return False

    for poi in pois:
        criteria = {"id":poi['id']}
        setCategory= {"$set" : {"categories":category}}
        addCategory = {"$push": {"categories":category}}
        if mycol.find(criteria).limit(1).count():
            if poi['categories'] is None: 
                mycol.update_one(criteria,setCategory)
            else:
                mycol.update_one(criteria,addCategory)
            continue
        mycol.insert(poi)

    print("insertion/update complete")
    return False


def query_pois(keyWord,col):
    query = {"$or":[{"name":keyWord},{"address_big":keyWord},
                    {"address_mid":keyWord},{"address_small":keyWord},
                    {"address_detail":keyWord},{"address_road":keyWord}]}
    #Sample code for querynig included str 
    # query = {"$or":[{"name":/searchStr/},{"address_big":/searchStr/}]}
    pois = col.find({},query)
    return dumps(pois)


def update_star(id,starPoint):
    global mycol
    starCount = 1
    criteria = {"id":id}
    setStar = {"$set" : {"starPoint":starPoint,"starCount":starCount}}
    poi = mycol.find(criteria)
    if poi['star'] is None:
        mycol.update_one(criteria,setStar)
        return True
    else :
        starCount+=poi['starCount']
        starPoint /=starCount
        mycol.update_one(criteria,setStar)
        return True

    return False

def query_poi(id):
    global mycol
    query = {"id":id}
    poi = mycol.find(query).limit(1)
    return dumps(poi)

def query_square_bound(squareBound):
    global mycol
    maxLat = squareBound[0]
    minLat = squareBound[1]
    maxLon = squareBound[2]
    minLon = squareBound[3]
    myquery = {"lat":{"$gt":minLat, "$lt":maxLat},"lon":{"$gt":minLon,"$lt":maxLon}}
    result = mycol.find(myquery)
    return dumps(result)

#이름, 큰 ,주소, 중간주소, 잗은 디테일소, 카테고리들, 도로명주소 
def query_pois_all(keyWord):
    global mycol 
    query = {"$or":[{"name":keyWord},{"address_big":keyWord},
                    {"address_mid":keyWord},{"address_small":keyWord},
                    {"address_detail":keyWord},{"address_road":keyWord}]}
    #Sample code for querynig included str 
    # query = {"$or":[{"name":/searchStr/},{"address_big":/searchStr/}]}
    pois = mycol.find({},query)
    return dumps(pois)





async def notify_state(squareBound):
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = query_square_bound(squareBound)
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS.add(websocket)

async def unregister(websocket):
    USERS.remove(websocket)

async def serve_api(websocket, path):
    global mycol
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        # await websocket.send(query_square_bound())
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
            
    finally:
        await unregister(websocket)

asyncio.get_event_loop().run_until_complete(
    websockets.serve(serve_api, 'ec2-13-59-71-223.us-east-2.compute.amazonaws.com', 49152))
asyncio.get_event_loop().run_forever()
