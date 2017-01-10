from pymongo import MongoClient
import datetime
import json
from bson import json_util
import logging

LOG_FILENAME = 'fleet.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

MONGO_HOME = 'mongodb://localhost:27017/'

client = MongoClient(MONGO_HOME)
input_db = client.test
#input_db.authenticate('csms', '1234')
collection = input_db['torino']
collection_cars = input_db['enjoy_fleet']

cursor = collection.find({'provider':'enjoy'})

cars = []

for doc in cursor:
	
	try:
		for available_car in doc['state']:
			if available_car['car_plate'] not in cars:
				cars.append(available_car['car_plate'])
	except:
		count_error += 1
		message = 'ERROR! in entry {}'.format(doc['_id'])
		logging.debug(message)


for plate in cars:

	record = {
				'plate': plate,
				'rent_times': []
			 }
	try:
		collection_cars.insert_one(record)
		message = 'SUCCESS! added plate: {}'.format(plate)
		logging.debug(message)
	except:
		message = 'FAIL! error in: {}'.format(plate)
		logging.debug(message)
		print 'error!'