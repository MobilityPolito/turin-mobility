#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 12:24:53 2016

@author: Flavia
"""

from pymongo import MongoClient
from datetime import datetime
import json
from bson import json_util
import logging
import pandas as pd

LOG_FILENAME = 'getinfo_car2go.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

MONGO_HOME = 'mongodb://localhost:27017/'

client = MongoClient(MONGO_HOME)
input_db = client['MobilityDataLakeTrial']
collection = input_db['torino']
fleet_car2go = input_db['fleetC2G']

day = datetime(2016,11,25)
day2 = datetime(2016,11,26)

cursor = collection.find( {'$and': [ {'provider':'car2go'},{'timestamp': {'$lt': day2, '$gte': day} } ]} )
cursor_cars = fleet_car2go.find()
cars = {}

class Car2GoVehicle():
    
    def __init__(self,sn,plate):
        self.sn = sn
        self.plate = plate
        self.day = []


for document in cursor_cars:
    cars[document['plate']] = Car2GoVehicle(document['sequence_number'],document['plate'])

for document in cursor:
    for available_car in document['state']['placemarks']:
        car_traces = cars[available_car['name'].split('/')[1]].day
        car_shot = {'coordinates' : available_car['coordinates'], \
                    'last_seen': document['timestamp']}                
        if not any(d['coordinates'] == available_car['coordinates'] for d in car_traces): # BISOGNERà GESTIRE SOGLIA DI CAMBIAMENTO COORDINATE
            car_traces.append(car_shot)
        else:
            for shot in car_traces:
                if shot['coordinates'] == available_car['coordinates']:
                    shot['last_seen'] = document['timestamp']
        cars[available_car['name'].split('/')[1]].day = car_traces
             
        
    
        

