from pymongo import MongoClient
import datetime
import json

MONGO_HOME = 'mongodb://localhost:27017/'

client = MongoClient(MONGO_HOME)
input_db = client['test']
collection = input_db['torino']

client = MongoClient(MONGO_HOME)
output_db = client['MobilityDataLakeTrial']
output_db.torino.drop()
output_collection = output_db['torino']

start = datetime.datetime(2016, 11, 10)
end = datetime.datetime.now()

cursor = collection.find({"timestamp":{'$gte': start, '$lt': end}})

for document in cursor:
    
#    print type(document["provider"])
    
    if type(document["state"]) == dict:
#        print document["state"]["placemarks"][0].keys()
        document["provider"] = "car2go"
    
    elif type(document["state"]) == list:
#        for car in document["state"]:
#            print car["car_plate"]
        document["provider"] = "enjoy"
    
    elif type(document["state"]) == unicode:
#        print json.loads(document["state"]).keys()
        document["provider"] = "tobike"
        
    output_collection.insert_one(document)
