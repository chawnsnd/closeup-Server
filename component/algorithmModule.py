#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 11:01:48 2018

@author: parkheechan

Team Project : Close UP
""" 
import numpy as np
import numpy.linalg as nlg
import json
from math import sin, cos, asin, sqrt, atan2, radians
from sklearn.cluster import KMeans
import matplotlib.pylab as plt
import matplotlib as ds


def get_weights(self):
    data = self.test_data
    data = json.loads(data)
    print("JSON CONVERTER INITIALIZE")
    parsing_name = data['Name']
    parsing_Lat = data['Latitude']
    parsing_Har = data['Longitude']
    parsing_rest = data['Restaurant']
    #parsing_star = data['Star']
    #print(parsing_name, parsing_Lat, parsing_Har, parsing_rest)
    dataset_weights = np.ones((1,len(parsing_rest)), dtype=float)
    
    
    dist_list = list()
    star_list = list()
    
    for values in parsing_rest:
        distance = self.distance_normalizer(data, values)
        dist_list.append(distance)
        star_list.append(values['Star'])
        
    norm_data, dist_rank = self.get_rank_weights(dist_list)
    print(norm_data,dist_rank)
    dist_weights = self.convert_distance_weights(weights=dataset_weights.copy(), earn_weights=norm_data)
    star_weights = self.convert_starPoint_weights(weights=dataset_weights.copy(), earn_weights=star_list)
    
    converted_weights = dist_weights + star_weights
    print(dist_weights)
    print(star_weights)
    print(converted_weights)
    print(converted_weights.argsort())
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
        print("%f data To %f Normalized" %(data[index], norm_value))
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

def distance_normalizer(self, source_data, target_data):
    s_d = source_data
    t_d = target_data
    
    distance = self.route_distance(lat1=s_d['Latitude'], lat2=t_d['Latitude'],  lon1= s_d['Longitude'], lon2=t_d['Longitude'])
    return distance

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

def overlap_remove(self):
    # not Work
    temp_route_list = list()
    for index in range(len(self.route_list) - 1):
        route = self.route_list[index]['Restaurant']

def send_Info(self):
    print("DATA SEND INITIALIZE")
    


# 