from pymongo import MongoClient
import datetime
import json

MONGO_HOME = 'mongodb://64.137.240.27:27017/'

client = MongoClient(MONGO_HOME)
input_db = client.CSMS
input_db.authenticate('csms', '1234')
collection = input_db['torino']

#start = datetime.datetime(2016, 12, 1)
#end = datetime.datetime.now()

#cursor = collection.find({"timestamp":{'$gte': start, '$lt': end}})
cursor = collection.find()

count = 0
count_error = 0

for document in cursor:

	try:
		if document['provider'] == 'car2go':
			car = document['state'][0]
			if car['lon'] < 8:
				count += 1
				print count
	except:
		print document['_id']
		count_error += 1

print "---------"
print "Tot enjoy torino: ", count
print "Tor error: ", count_error