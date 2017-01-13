import datetime

from pymongo import MongoClient

import pandas as pd

client = MongoClient('mongodb://localhost:27017/')

# db raw
# db formatted
# db compressed

class DataBaseProxy (object):
    
    def __init__ (self):
        
        self.db_raw = client['CSMS']
        self.db_compressed = client['CSMS_']
#        self.compress()
        self.db = self.db_compressed

    def compress (self):
    
        input_db = self.db_raw
        output_db = self.db_compressed
        
        for provider in ["enjoy","car2go"]:
    
            print provider
                
            if provider is "enjoy":
                for city in ["torino"]:

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
            
    def insert_park (self, 
                     provider, 
                     city, 
                     car, 
                     lat, lon, 
                     start, end):

        park = {
                    "provider": provider,
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

    def insert_park_v2 (self, city, park):
        
        collection = self.db[city + "_parks_v2"]            
        try:
            collection.insert_one(park)
        except:
            print "Invalid data coding!"

    def insert_book_v2 (self, city, book):
        
        collection = self.db[city + "_books_v2"]            
        try:
            collection.insert_one(book)
        except:
            print "Invalid data coding!"

                
    def insert_book (self, 
                     provider, 
                     city, 
                     car, 
                     start_lat, start_lon, 
                     end_lat, end_lon, 
                     start, end):

        park = {
                    "provider": provider,
                    "car": car, 
                    "start_lat": start_lat,
                    "start_lon": start_lon,
                    "end_lat": end_lat,
                    "end_lon": end_lon,
                    "start": start,
                    "end": end
                }
        
#        print park
        
        collection = self.db[city + "_books_v2"]            
        try:
            collection.insert_one(park)
        except:
            print "Invalid data coding!"

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
        
        return self.db[city + "_parks_v2"].find \
                    ({"start":
                         {
                             '$gte': start,
                             '$lt': end
                         },
                     "provider":provider
                    }).sort([("_id", 1)])

    def query_book_by_time (self, provider, city, start, end):
        
        return self.db[city + "_books_v2"].find \
                    ({"start":
                         {
                             '$gte': start,
                             '$lt': end
                         },
                     "provider":provider
                    }).sort([("_id", 1)])                        
                                                                        
dbp = DataBaseProxy()
