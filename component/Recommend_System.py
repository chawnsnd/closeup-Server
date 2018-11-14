#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 11:01:48 2018

@author: parkheechan

Team Project : Close UP
"""
import numpy as np
import numpy.linalg as nlg
#import pandas as pd
import json
from math import sin, cos, asin, sqrt, atan2, radians
from sklearn.cluster import KMeans
import matplotlib.pylab as plt
import matplotlib as ds

# Name
# Latitude : 위도 
# Longitude : 경도
# Category

class recommend:
    def __init__(self):
        self.route_list = list()
        self.R = 6373.0
    
    def json_data_converter(self, json_data):
        print("맛집 정보들")
        
        #data = json.loads(json_data)    
        #parsing_id = data["_id"]
        #parsing_key = data["key"]

        Lat = list()
        Lon = list()
        Category = list()
        Star = list()
        
        for lists in json_data:                  
            parsing_Lat = lists["lat"]
            parsing_Lon = lists["lon"]
            parsing_Category = lists["categories"]
            parsing_Star = lists["starPoint"]
            Lat.append(parsing_Lat)
            Lon.append(parsing_Lon)
            Category.append(parsing_Category)
            Star.append(parsing_Star)
        
        dataset_weights = np.ones((1,len(Lat)), dtype=float)
        #parsing_rest = data['Restaurant']
        
        return  Lat, Lon, Category, Star, dataset_weights, json_data
    
    def json_mens_converter(self, json_data):
        print("사람 데이터들")
        
        #data = json.loads(json_data)
        Lat = list()
        Lon = list()
        
        for lists in json_data:
            parsing_Lat = lists["lat"]
            parsing_Lon = lists["lon"]
        
        return Lat, Lon, json_data
        
        #dataset_weights = np.ones((1,len(parsing_Lat)), dtype=float)
        
        return parsing_Lat, parsing_Lon #, dataset_weights

    def json_dummy_init(self):
        dummy0 = {"lat" : 13.02, "lon" : 11.33, "_id" : 'e28321', "key" : 'e23121', 'starPoint' : 2.5, 'categories' : 'cafe'}
        dummy1 = {"lat" : 16.72, "lon" : 14.12, "_id" : 'e26311', "key" : 'e333121', 'starPoint' : 1.5, 'categories' : 'chicken'}
        
        dummy_man0 = {"lat" : 15.55, "lon" : 17.11}
        dummy_man1 = {"lat" : 19.05, "lon" : 31.28}
        dummy_list = list()
        dummy_man_list = list()
        #dummy_total = {"place" : [dummy0, dummy1]}
        #men_dum0 = {"identity" : "ParkHeeChan", "lon" : 15.3, "lat" : 22.1}
        
        dummy_list.append(dummy0)
        dummy_list.append(dummy1)
        
        dummy_man_list.append(dummy_man0)
        dummy_man_list.append(dummy_man1)
        
        #temp_data = json.dumps(dummy_total)
        #data2 = json.dumps(men_dum0)
        #self.test_temp_data = temp_data
        #self.test_temp_mens = data2
        self.dummy = dummy_list
        self.dummy_man = dummy_man_list
        
    
    def get_weights(self, earn_data, earn_men_data, isTest):
        
        #parsing_Key = data['key']
        #parsing_Lat = data['lat']
        #parsing_Har = data['lon']
        #parsing_star = data['Star']
        #print(parsing_name, parsing_Lat, parsing_Har, parsing_rest)
        #dataset_weights = np.ones((1,len(parsing_Key)), dtype=float)
        
        print("INITIALIZE")
        if isTest == True:       
            data = self.dummy
            mens = self.dummy_man
        else:
            data = earn_data
            mens = earn_men_data
        
        #mens = json.loads(men_data)
        #data = json.loads(data)
        
        lat, lon, category, star, weights, data = self.json_data_converter(data)
        men_lat, men_lon, mens = self.json_mens_converter(mens)
        
        mens_info = dict()
        star_list = list()
        
        for value in star:
            star_list.append(value)

        count = 0
        for men in mens:
            dist_list = list()
            for values in data:    
                distance = self.distance_normalizer(values, men)
                dist_list.append(distance)
            mens_info[count] = dist_list
            count += 1
        
        for key, values in mens_info.items():
            print(values)
        norm_data, dist_rank = self.get_rank_weights(dist_list)
        print(norm_data,dist_rank)
        
        #dist_weights = self.convert_distance_weights(weights=dataset_weights.copy(), earn_weights=norm_data)
        #star_weights = self.convert_starPoint_weights(weights=dataset_weights.copy(), earn_weights=star_list)
        
        #converted_weights = dist_weights + star_weights
        #print(dist_weights)
        #print(star_weights)
        #print(converted_weights)
        #print(converted_weights.argsort())
        #dist_rank = nlg.matrix_rank(dist_list)
    
    def route_distance(self, lat1, lon1, lat2, lon2):
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        distance = self.R * c
        
        print(distance)
        return distance
    
    def distance_normalizer(self, source_data, target_data):
        s_d = source_data
        t_d = target_data
        
        distance = self.route_distance(lat1=s_d['lat'], lat2=t_d['lon'],  lon1= s_d['lat'], lon2=t_d['lon'])
        return distance
    
        

    def convert_starPoint_weights(self, weights, earn_weights):
        # 0.125 weights
        weights_sum = 0
        for index in range(len(earn_weights)):
            if earn_weights[index] == 'none':
                earn_weights[index] = 1
            weights_sum = weights_sum + earn_weights[index]
        
        weights_mean = weights_sum / len(earn_weights)
        print("STAR POINTS MEAN is ", weights_mean)
        
        irow, icol = weights.shape        
        for index in range(icol):
            if earn_weights[index] == 'none':
                weights[:,index] = weights[:, index] * weights_mean * 0.125
            else:
                weights[:, index] = weights[:, index] * earn_weights[index] * 0.125
        
        return weights
    
    def convert_distance_weights(self, weights, earn_weights):
        # 0.875 weights
        irow, icol = weights.shape
        for index in range(icol):
            weights[:, index] = weights[:, index] * earn_weights[index] * 0.875

        return weights
        
    
    def get_rank_weights(self, data):
        #sorted_data = np.argsort(data)
        #weight_rate = 0.7
        temp_list = list()
        data_max = np.max(data)
        data_min = np.min(data)
        for index in range(len(data)):
            #norm_value = (data[index] - data_min) / (data_max - data_min)
            norm_value = (1 / (1 + data[index]))
            #print("%f data To %f Normalized" %(data[index], norm_value))
            temp_list.append(norm_value)
        
        norm_data = temp_list
        sorted_arg = np.argsort(data)
        return norm_data, sorted_arg
    
    def kmean_clustering(self, parameter, datasets):
        print("clustering_init")
        clustering = KMeans(n_clusters=4)
        clustering.fit(datasets)
        
        y_predict = clustering.predict(datasets)
        
        print(y_predict)
        print(y_predict.labels_) 
        print(y_predict.cluster_centers_)

    def scatter(self, datasets, predict):
        print("Plot Clustering")
    
    def compare_with_datasets(self, datasets):
        var_list = list()
        for key in datasets.keys():
             var_values = np.var(datasets[key])
             var_list.append(var_values)
        
        print(np.min(var_list))
        
    def decision_datasets(self, datasets):
        print("decision datasets Initialize")
        for key in datasets.keys():
            temp_datasets = dataset[key]
    
    #def overlap_remove(self):
    #    # not Work
    #    temp_route_list = list()
    #    for index in range(len(self.route_list) - 1):
    #        route = self.route_list[index]['Restaurant']
    
    def send_Info(self):
        print("DATA SEND INITIALIZE")
        
    
#dummy = {"Name" : "GilDong", "Latitude"}

dummy_data1 = 0
dummy_data2 = 0

json_test = recommend()
json_test.json_dummy_init()
#json_test.json_data_converter(json_test.dummy)
#json_test.json_mens_converter(json_test.dummy_man)
json_test.get_weights(dummy_data1, dummy_data2, True)

# 