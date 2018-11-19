#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 03:22:55 2018

@ project : close up
@ author: Dankook of University (Republic of Korea) 32121882 Park Hee Chan
@ mail : hchan11@naver.com

"""

import numpy as np
from math import sin, cos, asin, sqrt, atan2, radians
from sklearn.cluster import KMeans

def json_dataset_converter(datasets):
    print("Earn Datasets Process Init")

    '''
    'name'
    'lat'
    'lon'
    'categories'
    'starPoint'
    '_id'
    '''
    
    Name_list = list()
    Lat = list()
    Lon = list()
    Category = list()
    Star = list()
    ID_list = list()
    image_list = list()
    for lists in datasets:     
        parsing_Name = lists["name"]         
        parsing_Lat = lists["lat"]
        parsing_Lon = lists["lon"]
        parsing_Img = lists["image"]
        # parsing_Category = lists["categories"]
        parsing_Star = lists["starPoint"]
        parsing_ID = lists["id"]
        image_list.append(parsing_Img)
        Name_list.append(parsing_Name)
        Lat.append(parsing_Lat)
        Lon.append(parsing_Lon)
        # Category.append(parsing_Category)
        Star.append(parsing_Star)
        ID_list.append(parsing_ID)
    
    dataset_weights = np.ones((1,len(Lat)), dtype=float)
    data_nb = len(Lat)
    #parsing_rest = data['Restaurant']
    
    return  image_list,Name_list, Lat, Lon, Category, Star, ID_list, dataset_weights, datasets, data_nb

def json_people_converter(datasets):
    print("Earn People Datasets Process Init")
    
    Lat = list()
    Lon = list()
    
    for lists in datasets:
        parsing_Lat = lists["lat"]
        parsing_Lon = lists["lon"]
        Lat.append(parsing_Lat)
        Lon.append(parsing_Lon)
    
    people_nb = len(Lat)
    return Lat, Lon, datasets, people_nb

def get_clustering(parameter, datasets):
    print("K-Mean Clustering Init")
    clustering = KMeans(n_clusters=parameter)
    clustering.fit(datasets)
    
    labels = clustering.predict(datasets)
    centers = np.array(clustering.cluster_centers_)
    
    print("Datasets Labeling Completed : ",labels)
    print("Centroids Data : ",clustering.cluster_centers_)
    
    return labels, centers

def get_distance_each_value(lat1, lon1, lat2, lon2):
    print("get Distance Based on lat & lon Initialize")
    R = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c
    
    #print("distance value : ",distance)
    return distance

def get_norm_weights(data):

    data_len = len(data)
    
    norm_data = np.zeros([1,data_len])
    
    for index in range(len(data)):
        
        '''
        # choice 1 : norm_value = (data[index] - data_min) / (data_max - data_min)
        # choice 2 : norm value = data / (1 + data)
        '''
        
        norm_value = (1 / (1 + data[index]))
        norm_data[0,index] = norm_value

    return norm_data

def get_starPoint_weights(weights, earn_weights):
    print("Star Point Weight Apply Init")
    
    weights_sum = 0
    for index in range(len(earn_weights)):
        if earn_weights[index] == 0:
            earn_weights[index] = 1
        weights_sum = weights_sum + earn_weights[index]
    
    weights_mean = weights_sum / len(earn_weights)
    #print("STAR POINTS MEAN is ", weights_mean)
    
    irow, icol = weights.shape        
    for index in range(icol):
        if earn_weights[index] == 0:
            weights[:,index] = (weights[:, index] * weights_mean)/(1 + (weights[:, index] * weights_mean)) #* parameter
        else:
            weights[:, index] = (weights[:, index] * earn_weights[index])/ (1 + (weights[:, index] * earn_weights[index])) #* parameter
    
    return weights

def decision_datasets(datasets, star_weights, star_parameter):
    print("decision datasets Init")
    
    drow, dcol = datasets.shape
    result_datasets = np.zeros((drow,dcol))
    for index in range(dcol):
        if star_weights[0,index] != 0:
            star_weights[0,index] = (1 - star_weights[0,index]) * star_parameter
        result_datasets[0,index] = datasets[0,index] * star_weights[0,index]
   
    return result_datasets

def get_rank_of_decision( weight, datasets, decision_index, isOver, parameter):
    rank_list = list()
    if isOver == False:
        recommend_nb = len(weight)
    else:
        recommend_nb = parameter
    
    for ranked in range(recommend_nb):
        decision_nb = weight[ranked]
        rank_nb = decision_index[decision_nb]
        datasets[2,rank_nb] = ranked + 1
        rank_list.append(rank_nb)
        
    return datasets, rank_list

def Convert_Info(image_list,name_list, weight ,Ranked, Lat, Lon, Category, Star, ID):
    print("DATA Convert INITIALIZE")
    dict_list = list()
    for index in Ranked:
        parsing_dict = dict()
        parsing_dict["name"] = name_list[index]
        parsing_dict["lat"] = Lat[index]
        parsing_dict["lon"] = Lon[index]
        # parsing_dict["categoris"] = Category[index]
        parsing_dict["starPoint"] = Star[index]
        parsing_dict["id"] = ID[index]
        parsing_dict["weight"] = weight[0,index]
        parsing_dict["image"] = image_list[0,index]
        dict_list.append(parsing_dict)
    
    return dict_list

def recommend_system(people_datasets, earn_datasets):
    
    # Data Variable Init & Parameter Setting
    
    '''
    set Clustering number in datasets (default = 4)
    set Distance weight rate      (default = 0.875)
    set Star Point weight rate    (default = 0.275)
    set Recommend Datasets number (default = 10) # It must lower than data number
    '''
    
    print("Recommend System Init")
    PARAMETER_FOR_KMEAN = 3
    PARAMETER_FOR_DIST = 0.825
    PARAMETER_FOR_STAR = 0.275
    PARAMETER_FOR_DECISION = 30
    
    data = earn_datasets
    mens = people_datasets
    
    # list Data convert To Decision datasets
    image_list, Name_list, lat, lon, category, star, id_list, weights , data, data_nb= json_dataset_converter(data)
    men_lat, men_lon, mens, people_nb = json_people_converter(mens)
    
    # Data Vectorized for Algorithm
    dataset_arr = np.zeros((2,data_nb))
    for lat_index in range(len(lat)):
        dataset_arr[0,lat_index] = lat[lat_index]
    for lon_index in range(len(lon)):
        dataset_arr[1,lon_index] = lon[lon_index]    
        
    # K-Means Clustering
    label_data, centroid = get_clustering(parameter=PARAMETER_FOR_KMEAN, datasets=dataset_arr.transpose())
    
    # Clustering Selection
    mens_info = dict()
    count = 0
    for men in mens:
        dist_list = list()
        for value in range(PARAMETER_FOR_KMEAN):
            c_lat, c_lon = centroid[value,:]
            distance = get_distance_each_value(men['lat'], men['lon'], c_lat, c_lon)
            dist_list.append(distance)
        mens_info[count] = dist_list
        count += 1
    
    # Cluster Centroids Normalization
    norm_mens_info = dict()
    
    for key, value in mens_info.items():
        norm_data = get_norm_weights(value)
        norm_mens_info[key] = norm_data
    
    sum_list = list()
    sum_temp = 0
    for index in range(PARAMETER_FOR_KMEAN):
        for key in norm_mens_info.keys():
            temp = norm_mens_info[key]
            sum_temp += temp[0,index]
        sum_list.append(sum_temp/PARAMETER_FOR_KMEAN)
        sum_temp = 0
        
    #print(sum_list)
    #print(np.argmin(sum_list))
    
    #Cluster Selected
    select_label = np.argmin(sum_list)
    dist_index_list = list()
    
    # get datasets in Cluster & Remove other Clusters
    label_nb = 0
    for index in label_data:
        if index == select_label:
            dist_index_list.append(label_nb)
        label_nb +=1
    
    deci_mens_info = dict()
    count = 0
    
    # get distances each place
    print("Route Distance Initialize")
    for men in mens:
        print(men)
        dist_list = list()
        for index in dist_index_list:
            distance = get_distance_each_value(men['lat'], men['lon'], lat[index], lon[index])
            dist_list.append(distance)
        deci_mens_info[count] = dist_list
        count += 1
    
    #print(deci_mens_info)
    
    # Decision Datasets Normalization
    norm_deci_mens_info = dict()
    for key,value in deci_mens_info.items():
        deci_norm_data = get_norm_weights(value)
        norm_deci_mens_info[key] = deci_norm_data
    
    # get Distance Weights
    sum_list = list()
    sum_temp = 0
    for index in range(len(dist_index_list)):
        for key in norm_deci_mens_info.keys():
            temp = norm_deci_mens_info[key]
            sum_temp += temp[0,index]
        sum_list.append(sum_temp/len(dist_index_list))
        sum_temp = 0
    
    #print(sum_list)
    #print(np.argsort(sum_list))
    
    # make decision datasets & weight datasets
    decision_people_arr = np.zeros((3,data_nb))
    decision_dataset_arr = np.zeros((1,data_nb))
    decision_star_arr = np.zeros((1,data_nb))
    for index in dist_index_list:
        decision_people_arr[0,index] = lat[index]
        decision_people_arr[1,index] = lon[index]
        decision_dataset_arr[0,index] = 1
        decision_star_arr[0,index] = 1
    
    # distance weight applied
    sum_count = 0
    for nb in range(data_nb):
        if decision_dataset_arr[0,nb] != 0:
            decision_dataset_arr[0,nb] = sum_list[sum_count] * PARAMETER_FOR_DIST
            sum_count+=1
    
    # star point weight applied
    add_star_weights = get_starPoint_weights(weights = decision_star_arr, earn_weights=star)
    
    #print(add_star_weights)
    
    # decision algorithmn
    weight_decision = decision_datasets(datasets=decision_dataset_arr, star_weights=add_star_weights, star_parameter=PARAMETER_FOR_STAR)
    
    #print(weight_decision)
    weight_list = list()
    for index in dist_index_list:
        weight_list.append(weight_decision[0,index])
    
    # decision datasets Ranking
    sorted_weight = sorted(range(len(weight_list)), key=lambda k: weight_list[k])
    
    
    if len(sorted_weight) < PARAMETER_FOR_DECISION:
        dataset_arr,rank_list = get_rank_of_decision(weight=sorted_weight, decision_index=dist_index_list, 
                                                        datasets=decision_people_arr,isOver=False, parameter=PARAMETER_FOR_DECISION) 
    else:
        decision_people_arr,rank_list = get_rank_of_decision(weight=sorted_weight, decision_index=dist_index_list, 
                                                        datasets=decision_people_arr,isOver=True, parameter=PARAMETER_FOR_DECISION) 
    
    # Convert decision datasets to list
    decision = Convert_Info(image_list = image_list , name_list=Name_list ,weight= weight_decision ,Ranked=rank_list ,Lat=lat ,Lon=lon ,Category=category ,Star=star ,ID=id_list)
    
    return decision
