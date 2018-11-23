#!/usr/bin/env python3.6

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
from ast import literal_eval
from flask import Flask, request, jsonify, Response
import pymongo
import sys
from bson.json_util import dumps
from component.apis import *
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={
  r"/*": {"origin": "*"},
})

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



@app.route("/api/pois", methods=["POST"])
def insertPois():
    req = request.json
    res = insert_pois(req['pois'],req['categories'])
    return dumps(res)


@app.route("/api/pois", methods=["GET"])
def getPois():
    keyWord = request.args.get('keyWord')
    count = int(request.args.get('count'))
    page = int(request.args.get('page'))

    res = query_pois(keyWord,count,page,mycol)
    return res

@app.route("/api/pois/<poiId>", methods=["PUT"])
def updateStar(poiId):
    req = request.json
    res = update_star(poiId,req['starPoint'])
    return jsonify(res)

@app.route("/api/pois/<poiId>", methods=["GET"])
def getPoi(poiId):
    res = query_poi(poiId)
    return dumps(res)

@app.route("/api/recommendPois", methods=["GET"])
def recommendPois():
    keyWord = request.args.get('keyWord')
    people_chosen = request.args.getlist('people_chosen[]')
    newPeople  = list()
    for person in people_chosen:
        newPeople.append(literal_eval(person))
    res = recommend_api(newPeople,keyWord)
    return dumps(res)

if __name__ == '__main__':
    # app.run(host='ec2-13-125-249-233.ap-northeast-2.compute.amazonaws.com',port=5000)
    app.run(host='localhost',port=5000)
