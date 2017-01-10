#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 17:22:16 2016

@author: Flavia
"""

from pymongo import MongoClient
import datetime
import json
from bson import json_util
import logging

LOG_FILENAME = 'fleet.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

MONGO_HOME = 'mongodb://localhost:27017/'

client = MongoClient(MONGO_HOME)
input_db = client['MobilityDataLakeTrial']
collection = input_db['torino']
fleet_car2go = input_db['fleetC2G']



cursor = collection.find({'provider' : 'car2go'})

cars = []
count_error = 0


for document in cursor:
    try:    
        for available_car in document['state']['placemarks']:
            if available_car['name'] not in cars:
                cars.append(available_car['name'])
    except:
        count_error += 1
        message = 'ERROR! in entry {}'.format(document['_id'])
        logging.debug(message)       
            

for car_name in cars:
    record = {
                  'sequence_number': car_name.split('/')[0], 
                  'plate': car_name.split('/')[1],
			 'rent_times': []
			 }
    try:
        fleet_car2go.insert_one(record)
        message = 'SUCCESS! added car: {}'.format(car_name)
        logging.debug(message)

    except:
        message = 'FAIL! error in: {}'.format(car_name)
        logging.debug(message)
        print 'error!'
    
