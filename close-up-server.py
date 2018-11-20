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

app = Flask(__name__)
# SAMPLE CODE
# print(myclient.list_database_names())
# collist = mydb.list_collection_names()
# print(mycol.find_one())

@app.route("/pois", methods=["POST"])
def insertPois():
    req = request.json
    res = insert_pois(req['pois'],req['categories'])
    return jsonify(res)

@app.route("/pois", methods=["GET"])
def queryPois():
    req = request.json
    res = query_pois(req['keyWord'],req['count'],req['page'],mycol)
    return jsonify(res)

@app.route("/pois/{poiId}", methods=["PUT"])
def updateStar():
    req = request.json
    res = update_star(req['id'],req['starPoint'])
    return jsonify(res)

@app.route("/pois/{poiId}", methods=["GET"])
def getPoi():
    req = request.json
    res = query_poi(req['id'])
    return jsonify(res)
@app.route("/recommendPois", methods=["GET"])
def insertPois():
    req = request.json
    res = insert_pois(req['pois'],req['categories'])
    return jsonify(res)

if __name__ == '__main__':

    app.run(host='ec2-13-125-249-233.ap-northeast-2.compute.amazonaws.com',port=5000)