#!/usr/bin/env python3.6

# WS server example that synchronizes state across clients

import asyncio
import json
import logging

from flask import Flask, request, jsonify, Response
import pymongo
import sys
from bson.json_util import dumps
from component.apis import *
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={
  r"/v1/*": {"origin": "*"},
  r"/api/*": {"origin": "*"},
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




@app.route("/pois", methods=["POST"])
def insertPois():
    req = request.json
    res = insert_pois(req['pois'],req['categories'])
    return jsonify(res)


@app.route("/pois", methods=["GET"])
def getPois():
    req = request.json
    res = query_pois(req['keyWord'],req['count'],req['page'],mycol)
    return jsonify(res)

@app.route("/pois/<poiId>/<starPoint>", methods=["PUT"])
def updateStar(poiId,starPoint):
    res = update_star(poiId,starPoint)
    return jsonify(res)

@app.route("/pois/<poiId>", methods=["GET"])
def getPoi(poiId):
    res = query_poi(poiId)
    return jsonify(res)

@app.route("/recommendPois", methods=["GET"])
def recommendPois():
    req = request.json
    res = recommend_api(req['people_chosen'],req['keyWord'])
    return jsonify(res)

if __name__ == '__main__':
    # app.run(host='ec2-13-125-249-233.ap-northeast-2.compute.amazonaws.com',port=5000)
    app.run(host='localhost',port=5000)