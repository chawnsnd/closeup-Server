#!/usr/bin/env python3.6

# WS server example that synchronizes state across clients

import json
import logging
from flask import Flask, request, jsonify, Response
import pymongo
import sys
from bson.json_util import dumps
from flask_cors import CORS
from dao.closeUpDao import insert_pois
from service.closeUpService import updateStar, getPoi, getPois, recommendPois

app = Flask(__name__)
cors = CORS(app, resources={
  r"/*": {"origin": "*"},
})


@app.route("/api/pois", methods=["POST"])
def DBinsert():
    req = request.json
    res = insert_pois(req['pois'],req['categories'])
    return dumps(res)


@app.route("/api/pois", methods=["GET"])
def pagination():
    keyWord = request.args.get('keyWord')
    count = int(request.args.get('count'))
    page = int(request.args.get('page'))
    res = getPois(keyWord,count,page)
    return res

@app.route("/api/pois/<poiId>", methods=["PUT"])
def starUpdate(poiId):
    req = request.json
    res = updateStar(poiId,req)
    return jsonify(res)

# @app.route("/api/pois/<poiId>", methods=["GET"])
# def getPoi(poiId):
#     res = query_poi(poiId)
#     return dumps(res)

@app.route("/api/recommendPois", methods=["GET"])
def recommendation():
    keyWord = request.args.get('keyWord')
    people_chosen = request.args.getlist('people_chosen[]')
    res = recommendPois(keyWord,people_chosen)
    return dumps(res)

if __name__ == '__main__':
    # app.run(host='ec2-13-125-249-233.ap-northeast-2.compute.amazonaws.com',port=5000)
    app.run(host='localhost',port=5000)
