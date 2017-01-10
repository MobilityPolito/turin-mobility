from pymongo import MongoClient
import datetime
import json
from bson import json_util
import logging

LOG_FILENAME = 'consistency.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

MONGO_HOME = 'mongodb://localhost:27017/'

client = MongoClient(MONGO_HOME)
input_db = client.test
#input_db.authenticate('csms', '1234')
collection = input_db['torino']

#start = datetime.datetime(2016, 12, 1)
#end = datetime.datetime.now()

#cursor = collection.find({"timestamp":{'$gte': start, '$lt': end}})
cursor = collection.find({'provider':'enjoy'})

entries = 0
count = 0
count_error = 0
torino = 0
milano = 0

for doc in cursor:

	entries += 1
	
	try:
		if doc['provider'] == 'enjoy':
			flag_milano = 0

			for available_car in doc['state']:

				print ('{}<{}?').format(available_car['lon'], 8)

				if available_car['lon'] < 8:
					pass
				else:
					flag_milano = 1

			if(flag_milano):
				milano += 1
				message = 'milano in {} at timestamp {}'.format(doc['_id'], doc['timestamp'])
				logging.debug(message)
			else:
				torino += 1
	except:
		count_error += 1
		message = 'ERROR! in entry {}'.format(doc['_id'])
		logging.debug(message)

print "---------"
print "Tot enjoy torino: ", torino
print "Tot enjoy milano: ", milano
print "Tot enjoy: ", entries
print "Tor error: ", count_error