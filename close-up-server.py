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

async def notify_state(message):
    if USERS:       # asyncio.wait doesn't accept an empty list
        await asyncio.wait([user.send(message) for user in USERS])

async def register(websocket):
    USERS.add(websocket)

async def unregister(websocket):
    USERS.remove(websocket)

# SAMPLE CODE
# print(myclient.list_database_names())
# collist = mydb.list_collection_names()
# print(mycol.find_one())

def insert_pois(pois,categories):
    global mycol 

    if pois is None:
        print("Failed (no pois)")
        return dumps({"type":"insert_pois","response":"insertion/update fail"})


    for poi in pois:
        criteria = {"id":poi['id']}
        setCategories= {"$set" : {"categories":categories}}
        addCategories = {"$push": {"categories":{"$each":categories}}}
        poi_doc = mycol.find_one(criteria)
        
        #check categories if exists
        if poi_doc:
            #update categories
            if not 'categories' in poi_doc:
                mycol.update_one(criteria,setCategories,True)
                continue
            if poi_doc['categories'] is None: 
                mycol.update_one(criteria,setCategories,True)
            else:
                #skip if all elements in categories are in poi_doc , update all if not
                if all(category in poi_doc['categories'] for category in categories):
                    continue
                mycol.update_one(criteria,addCategories)
            continue
        
        mycol.insert(poi)

    print("insertion/update complete")
    return dumps({"type":"insert_pois","response":"insertion/update success"})


def query_pois(keyWord,col):
    query = {"$or":[{"upperBizName":{"$regex":keyWord}},
                    {"middleBizName":{"$regex":keyWord}},
                    {"lowerBizName":{"$regex":keyWord}},
                    {"detailBizName":{"$regex":keyWord}},
                    {"name":{"$regex":keyWord}},
                    {"upperAddrName":{"$regex":keyWord}},
                    {"middleAddrName":{"$regex":keyWord}},
                    {"lowerAddrName":{"$regex":keyWord}},
                    {"detailAddrName":{"$regex":keyWord}},
                    {"roadName":{"$regex":keyWord}},
                    ]}
    #Sample code for querynig included str 
    # query = {"$or":[{"name":/searchStr/},{"address_big":/searchStr/}]}
    # "upperBizName" : "쇼핑",
    # "middleBizName" : "상설할인매장",
    # "lowerBizName" : "상설할인매장기타",
    # "detailBizName" : "기타",
    # "name" : "콜렉티드 죽전점",
    # "upperAddrName" : "경기",
    # "middleAddrName" : "용인시 수지구",
    # "lowerAddrName" : "죽전동",
    # "detailAddrName" : "",
    # "roadName" : "용구대로",
    result = dumps({"type":"query_pois","response":col.find(query)})
    return result


def update_star(id,starPoint):
    global mycol
    starCount = 1
    starPoint = float(starPoint)
    criteria = {"id":id}
    poi = mycol.find_one(criteria)

    if poi['starPoint'] is 0:
        print("star update new")
    elif poi['starPoint']:
        starPoint += poi['starPoint']*poi['starCount']
        starCount+=poi['starCount']
        starPoint /=starCount
        print("star updated existing")
    else :
        return dumps({"type":"update_star","response":"update failed"})
    
    setStar = {"$set" : {"starPoint":starPoint,"starCount":starCount}}
    mycol.update_one(criteria,setStar)
    return dumps({"type":"starPoint", "response":"update successed"})
    # print("star is not updated/ nothing to update")
    # return dumps({"type":"update_star","response":"nothing updated"})

def query_poi(id):
    global mycol
    query = {"id":id}
    poi = mycol.find(query).limit(1)
    return dumps({"type":"query_poi","response":poi})

def query_square_bound(people_chosen):
    global mycol
    maxLat = 0
    minLat = sys.maxsize
    maxLon = 0
    minLon = sys.maxsize

    for person in people_chosen:
        # print(person)
        maxLat = max(person['lat'],maxLat)
        minLat = min(person['lat'],minLat)
        maxLon = max(person['lon'],maxLon)
        minLon = min(person['lon'],minLon)

    myquery = {"lat":{"$gt":minLat, "$lt":maxLat},"lon":{"$gt":minLon,"$lt":maxLon}}
    result = dumps({"type":"query_square_bound","response":mycol.find(myquery)})
    return result

#이름, 큰 ,주소, 중간주소, 잗은 디테일소, 카테고리들, 도로명주소 
def query_pois_all(keyWord):
    global mycol 
    query = {"$or":[{"name":keyWord},{"address_big":keyWord},
                    {"address_mid":keyWord},{"address_small":keyWord},
                    {"address_detail":keyWord},{"address_road":keyWord}]}
    #Sample code for querynig included str 
    # query = {"$or":[{"name":/searchStr/},{"address_big":/searchStr/}]}
    pois = mycol.find(query)
    return dumps({"type":"query_pois_all","response":pois})


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
                await notify_state(query_square_bound(data['people_chosen']))    
            elif command =="query_poi":
                await notify_state(query_poi(data['id']))

            elif command =="update_star":
                await notify_state(update_star(data['id'],data['starPoint']))
            elif command == "query_pois":
                await notify_state(query_pois(data['keyWord'],mycol))
            
            
    finally:
        await unregister(websocket)

# asyncio.get_event_loop().run_until_complete(websockets.serve(serve_api, 'ec2-13-59-71-223.us-east-2.compute.amazonaws.com', 49152))
asyncio.get_event_loop().run_until_complete(websockets.serve(serve_api, '192.168.0.19', 49152))
asyncio.get_event_loop().run_forever()
