import datetime

from pymongo import MongoClient

import pandas as pd

client = MongoClient('mongodb://localhost:27017/')

# db raw
# db formatted
# db compressed

class DataBaseProxy(object):
    
    def __init__ (self):
        
        self.db_raw = client['CSMS']
        self.db_fix_providers = client['CSMS_']
        self.db_fix_cities = client['CSMS__']
        self.db_compressed = client['CSMS___']
        
#        self.db_formatted = client['CSMS____']

        self.db = self.db_raw

    def insert (self, provider, city, state):
    
        record = {
                     "timestamp": datetime.datetime.now(),
                     "provider": provider,
                     "state": state
                 }

        collection = self.db_raw[city]            
        try:
            collection.insert_one(record)
        except:
            print "Invalid data coding!"
            
    def insert_park (self, provider, city, car, lat, lon, start, end):

        park = {
                    "provider":provider,
                    "car": car, 
                    "lat": lat,
                    "lon": lon,
                    "start": start,
                    "end": end
                }
        
#        print park
        
        collection = self.db[city + "_parks"]            
        try:
            collection.insert_one(park)
        except:
            print "Invalid data coding!"
                
    def insert_book (self, provider, city, car, start_lat, start_lon, end_lat, end_lon, start, end, bill):

        park = {
                    "provider": provider,
                    "car": car, 
                    "start_lat": start_lat,
                    "start_lon": start_lon,
                    "end_lat": end_lat,
                    "end_lon": end_lon,
                    "start": start,
                    "end": end,
                    "bill" : bill
                }
        
#        print park
        
        collection = self.db[city + "_books"]            
        try:
            collection.insert_one(park)
        except:
            print "Invalid data coding!"

    def query_test (self, provider, city, start, end):
        return self.db[city].find().count()
    
    def query_raw_by_time (self, provider, city, start, end):
        
        return self.db[city].find \
                    ({"timestamp":
                         {
                             '$gte': start,
                             '$lt': end
                         },
                     "provider":provider
                    }).sort([("_id", 1)])

    def query_park_by_time (self, provider, city, start, end):
        
        return self.db[city + "_parks"].find \
                    ({"start":
                         {
                             '$gte': start,
                             '$lt': end
                         },
                     "provider":provider
                    }).sort([("_id", 1)])

    def query_book_by_time (self, provider, city, start, end):
        
        return self.db[city + "_books"].find \
                    ({"start":
                         {
                             '$gte': start,
                             '$lt': end
                         },
                     "provider":provider
                    }).sort([("_id", 1)])                        
                        
    def fix_providers(self):
        
        input_db = self.db_raw
        output_db = self.db_fix_providers
        
        for city in ['torino','milano']:
    
            input_collection = input_db[city]
            output_collection = output_db[city]
            
            cursor = input_collection.find()
            
            for document in cursor:
                
                if type(document["state"]) == dict:
                    document["provider"] = "car2go"
                
                elif type(document["state"]) == list:
                    document["provider"] = "enjoy"
                
                elif type(document["state"]) == unicode:
                    document["provider"] = "tobike"
                    
                output_collection.insert_one(document)
    
            
    def fix_cities (self):
        
        input_db = self.db_fix_providers
        output_db = self.db_fix_cities
    
        torino_collection = output_db['torino']        
        milano_collection = output_db['milano']
        
        def check_cap (document, cap):
            if cap.startswith("10"):
                torino_collection.insert_one(document)
            elif cap.startswith("20") or cap == "Milano" or cap == "Segrate":
                milano_collection.insert_one(document)
            else:
                print "Unknown CAP: " + cap
                print document["address"]
        
        for city in ['torino','milano']:
    
            input_collection = input_db[city]
            cursor = input_collection.find()
            
            for document in cursor:
                if document["provider"] == "enjoy":                    
                    car = document["state"][0]
                    if len(car["address"].split(',')) == 3:
                        cap = car["address"].split(',')[2].split(' ')[1]
                    elif len(car["address"].split(',')) == 2:
                        cap = car["address"].split(',')[1].split(' ')[1]
                    else:
                        cap = ""
                    check_cap(document, cap)
                else:
                    torino_collection.insert_one(document)
                            
    def compress (self):
    
        input_db = self.db_fix_cities
        output_db = self.db_compressed
        
        for provider in ["enjoy","car2go"]:
    
            print provider
                
            if provider is "enjoy":
                for city in ["torino", "milano"]:

                    input_collection = input_db[city]
                    output_collection = output_db[city]

                    cursor = input_collection.find({"provider": provider})

                    last = cursor.next()
                    output_collection.insert_one(last)                    
                    
                    for document in cursor: 
                        
                        current = document

                        try:
                            last_df = pd.DataFrame(last["state"])
                            current_df = pd.DataFrame(current["state"])
                            if not last_df.equals(current_df):
                                output_collection.insert_one(document)
                        except:
                            print type(current["state"])

                        last = document
                                
            elif provider is "car2go":
                
                for city in ["torino"]:
                    
                    print city
                    
                    input_collection = input_db[city]
                    output_collection = output_db[city]

                    cursor = input_collection.find({"provider": provider})

                    last = cursor.next()
                    output_collection.insert_one(last)                    
                    
                    for document in cursor: 
                        
                        current = document

                        try:
                            last_df = pd.DataFrame(last["state"]["placemarks"])
                            current_df = pd.DataFrame(current["state"]["placemarks"])
                            if not last_df.equals(current_df):
                                output_collection.insert_one(document)
                        except:
                            print type(current["state"]["placemarks"])

                        last = document
                        
    def format_providers (self):
        
        input_db = self.db_compressed
        output_db = self.db_formatted
        
        for provider in ["enjoy", "car2go"]:
            if provider == "car2go":
                for city in ["torino"]:

                    input_collection = input_db[city]
                    output_collection = output_db[city]
            
                    cursor = input_collection.find({"provider": provider})
                    
                    lats = []
                    lons = []
                    for doc in cursor:
                        new_state = doc["state"]["placemarks"]
                        df = pd.DataFrame(new_state)
                        coordinates = list(df["coordinates"].values)
                        for car_coordinates in coordinates:
                            if len(car_coordinates) is not 3:
                                print len(car_coordinates)
                            else:
                                lats += [car_coordinates[1]]
                                lons += [car_coordinates[0]]
                        df["lat"] = pd.Series(lats)
                        df["lon"] = pd.Series(lats)
                        df = df.drop("coordinates", axis=1)
            
                        new_doc = doc
                        new_doc["state"] = df.T.to_dict().values()
                        output_collection.insert_one(new_doc)

            elif provider == "enjoy":
                for city in ["torino", "milano"]:
                    
                    input_collection = input_db[city]
                    output_collection = output_db[city]
            
                    cursor = input_collection.find({"provider": provider})

                    for doc in cursor:
                        output_collection.insert_one(doc)
                    
def test():
    dbp = DataBaseProxy()
#    dbp.fix_providers()
#    dbp.fix_cities()
#    dbp.compress()
    
    #dbp.format_providers()

#    return dbp
    
#dbp = test()