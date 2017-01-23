import datetime

from pymongo import MongoClient

import pandas as pd

from workalendar.europe import Italy
from bdateutil import isbday

client = MongoClient('mongodb://localhost:27017/')

class DataBaseProxy (object):
    
    def __init__ (self):
        
        self.db_raw = client['CSMS']
        self.db_compressed = client['CSMS_']
        self.db = self.db_compressed

    def compress (self):
        
        input_db = self.db_raw
        output_db = self.db_compressed    
        for provider in ["enjoy","car2go"]:
            if provider is "enjoy":
                for city in ["torino"]:
                    input_collection = input_db["snapshots"]
                    output_collection = output_db["snapshots"]
                    cursor = input_collection.find({
                                                    "provider": provider,
                                                    "city": city
                                                    })
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
                    input_collection = input_db["snapshots"]
                    output_collection = output_db["snapshots"]
                    cursor = input_collection.find({
                                                    "provider": provider,
                                                    "city": city
                                                    })
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
        
    def insert_snapshot (self, provider, city, state):
    
        record = {
                     "timestamp": datetime.datetime.now(),
                     "provider": provider,
                     "city": city,
                     "state": state
                 }

        collection = self.db_raw["snapshots"]
        try:
            collection.insert_one(record)
        except:
            print "Invalid data coding!"

    def insert_park (self, provider, city, park):

        record = {
                     "provider": provider,
                     "city": city,
                     "start": park["start"],
                     "end": park["end"],
                     "park": park
                 }
        
        collection = self.db["parks"]            
        try:
            collection.insert_one(record)
        except:
            print "Invalid data coding!"

    def insert_book (self, provider, city, book):

        record = {
                     "provider": provider,
                     "city": city,
                     "start": book["start"],
                     "end": book["end"],
                     "book": book
                 }
        
        collection = self.db["books"]            
        try:
            collection.insert_one(record)
        except:
            print "Invalid data coding!"            
            
    def insert_day_analysis(self, day, city, provider, stats, od):

        record = {
                     "day" : day,
                     "city": city,
                     "provider": provider,
                     "stats": stats, 
                     "od": od
                 }

        collection = self.db["statistics"]

        try:
            collection.insert_one(record)
        except:
            print "Error in insert_one STATISTICS!" 

    def update_bookings (self, city, feed, object_id):
        
        return self.db[city + "_books_v2"].update_one({"_id":  object_id},
                                                      {"$set": feed },
                                                      upsert = True)
            
    def query_raw_by_time (self, provider, city, start, end):
        
        return self.db[city].find \
                    ({"timestamp":
                         {
                             '$gte': start,
                             '$lt': end
                         },
                     "provider":provider
                    }).sort([("_id", 1)])

    def query_parks (self, provider, city, start, end):
        
        return self.db["parks"].find \
                    ({"start":
                         {
                             '$gte': start,
                             '$lt': end
                         },
                     "provider":provider
                     "city":city
                     }).sort([("_id", 1)])

    def query_books (self, provider, city, start, end):
        
        return self.db["books"].find \
                    ({"start":
                         {
                             '$gte': start,
                             '$lt': end
                         },
                     "provider":provider
                     "city":city
                    }).sort([("_id", 1)])

    def get_parks_df (self, provider, city, start, end):
        
        parks_cursor = self.query_parks(provider, city, start, end)
        parks_df = pd.DataFrame(columns = pd.Series(parks_cursor.next()).index)
        for doc in parks_cursor:
            s = pd.Series(doc)
            parks_df = pd.concat([parks_df, pd.DataFrame(s).T], ignore_index=True)    

        return parks_df
                        
    def get_books_df (self, provider, city, start, end):
        
        books_cursor = self.query_books(provider, city, start, end)    
        books_df = pd.DataFrame(columns = pd.Series(books_cursor.next()).index)
        for doc in books_cursor:
            s = pd.Series(doc)
            books_df = pd.concat([books_df, pd.DataFrame(s).T], ignore_index=True)    
        
        return books_df

    '''
    Aggregation of bookings, in a given time interval, aggregated per
    #1 -> weekday
    #2 -> pre-holiday
    #3 -> holiday
    #4 -> weekend
    '''

    def get_books_df_filtered (self, provider, city, start, end, day_type):

        books_df = self.get_books(provider, city, start, end)
        books_df['b_day'] = books_df['start'].apply(isbday)
       
        cal = Italy()
        holidays = []
       
        #holidays collection creation
        if start.year == end.year:
            for h in cal.holidays(start.year):
                holidays.append(h[0])
        else:
            for year in range (start.year, end.year+1):
                 for h in cal.holidays(year):
                     holidays.append(h[0])
       
        if day_type == "business":
            business_books_df = books_df[books_df['b_day'] == True]
            return business_books_df

        elif day_type == "weekend":
            weekend_books_df = books_df[books_df['b_day'] == False]
            return weekend_books_df            
            
        #only the day BEFORE the holiday. WEEKends are not considered            
        elif day_type == "pre-holiday":
            pre_holidays = []
            for d in holidays:
                pre_holidays.append(d - datetime.timedelta(days = 1))
            pre_holidays.pop()
            #ph_day = pre hoiday day
            books_df['ph_day'] = books_df['start'].apply(lambda x: x.date())
            books_df['ph_day'] = books_df[books_df['ph_day'].isin(pre_holidays)]
            pre_holidays_books_df = books_df.dropna(subset=['ph_day'],how='all')
            del pre_holidays_books_df['b_day']
            del pre_holidays_books_df['ph_day']
            return pre_holidays_books_df
           
        #holidays WEEKEND EXCLUDED
        elif day_type == "holiday":
            books_df['h_day'] = books_df['start'].apply(lambda x: x.date())
            books_df['h_day'] = books_df[books_df['h_day'].isin(holidays)]
            holidays_books_df = books_df.dropna(subset=['h_day'],how='all')
            del holidays_books_df['b_day']
            del holidays_books_df['h_day']
            return holidays_books_df
                       
        else:
            raise Exception("day_type error")