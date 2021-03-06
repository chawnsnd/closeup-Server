#!/usr/bin/env python3.6

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import pymongo
import sys
from bson.json_util import dumps


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["CloseUpDB"]
mycol = mydb["TestPoisCollection"]


# CHECK DB CONNECTION
dblist = myclient.list_database_names()
if "CloseUpDB" in dblist:
    print("CloseUpDB connected")
else:
    print("NO DATABASE")

def insert_pois(pois,categories):
    global mycol 

    if pois is None:
        print("Failed (no pois)")
        return {"type":"insert_pois","response":"insertion/update fail"}


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
    return {"type":"insert_pois","response":"insertion/update success"}


def query_pois(keyWord, count, page):
    global mycol
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
    # result = dumps({"type":"query_pois","response":col.find(query)}) #return json
    skips = count * (page - 1)
    totalCount = mycol.count(query)
    result = mycol.find(query).skip(skips).limit(count)  #return cursor
    returnResult = {"pois": result, "totalCount": totalCount}
    return dumps(returnResult)


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
        return {"type":"update_star","response":"update failed"}
    
    setStar = {"$set" : {"starPoint":starPoint,"starCount":starCount}}
    mycol.update_one(criteria,setStar)
    return {"type":"starPoint", "response":"update successed"}
    # print("star is not updated/ nothing to update")
    # return dumps({"type":"update_star","response":"nothing updated"})

def query_poi(id):
    global mycol
    query = {"id":id}
    return mycol.find(query).limit(1)[0]


def query_poi_temp(id):
    global mycol
    query = {"id":id}
    poi = mycol.find(query).limit(1)[0]
    return poi

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
    result = mycol.find(myquery)
    return result
def query_poi_temp(id):
    global mycol
    query = {"id":id}
    poi = mycol.find(query).limit(1)[0]
    return poi

def query_square_bound_and_keyword(people_chosen,keyWord):
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
  
    queryKeyWord = {"$or":[{"upperBizName":{"$regex":keyWord}},
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
    queryBound = {"lat":{"$gt":minLat, "$lt":maxLat},"lon":{"$gt":minLon,"$lt":maxLon}}
    # result = dumps({"type":"query_square_bound","response":mycol.find(myquery)})
    result = mycol.find({"$and":[queryKeyWord,queryBound]})
    return result


