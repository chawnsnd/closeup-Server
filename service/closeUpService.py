#!/usr/bin/env python3.6

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets
import pymongo
import sys
from bson.json_util import dumps
from algorithm.Recommend_System_div_ver import recommend_system
from dao.closeUpDao import query_pois, query_poi , update_star, query_poi_temp,query_square_bound_and_keyword
from ast import literal_eval


def getPois(keyWord,count,page):
    res = query_pois(keyWord,count,page)
    return res

def updateStar(poiId,req):
    res = update_star(poiId,req['starPoint'])
    return res

def getPoi(poiId):
    res = query_poi(poiId)
    return dumps(res)

def recommendPois(keyWord, people_chosen):
    newPeople  = list()
    for person in people_chosen:
        newPeople.append(literal_eval(person))
    peopleList = list(newPeople)

    # 세사람이랑 중심간 평균거리 1/2 만큼 중심으로부터의 좌표만 쏘는거
    sumLat, sumLon = 0,0
    for person in peopleList:
        sumLat += person['lat']
        sumLon += person['lon']
    midLat = sumLat/len(peopleList)
    midLon = sumLon/len(peopleList)
    
    avgDistFromMid=0
    sumDistFromMid=0
    for person in peopleList:
        sumDistFromMid +=(person['lat'] - midLat)**2 + (person['lon'] - midLon)**2
    avgDistFromMid = sumDistFromMid/len(peopleList)
        
    query_poisList = list(query_square_bound_and_keyword(newPeople,keyWord))
    nearMidPlaces=[]
    for poi in query_poisList:
        if (poi['lat'] - midLat)**2 + (poi['lon'] - midLon)**2 < (avgDistFromMid/4):
            nearMidPlaces.append(poi)

    # sorted(query_poisList, key=lambda poi: (midLat- poi['lat'])**2 +(midLon -poi['lon'])**2)
    
    #알고리즘
    recommendation = recommend_system(peopleList,nearMidPlaces)
    # recommendation = recommend_system(peopleList,query_poisList)
    pois = []
    for r in recommendation :
        poi = {}
        poi = query_poi_temp(r['id'])
        poi['weight'] = r['weight']
        pois.append(poi)
    return pois