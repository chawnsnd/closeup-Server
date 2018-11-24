#!/usr/bin/env python3.6

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets
import pymongo
import sys
from bson.json_util import dumps
from algorithm.Recommend_System_div_ver4 import recommend_system
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

    query_poisList = list(query_square_bound_and_keyword(newPeople,keyWord))

    #알고리즘
    recommendation = recommend_system(peopleList,query_poisList)
    pois = []
    for r in recommendation :
        poi = {}
        poi = query_poi_temp(r['id'])
        poi['weight'] = r['weight']
        pois.append(poi)
    return pois