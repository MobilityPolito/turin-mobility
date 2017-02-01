from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km
    
import datetime

import pandas as pd

import numpy as np

from workalendar.europe import Italy

from pymongo import MongoClient
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

        collection = self.db["parks"]            
        try:
            collection.insert_one(park)
        except:
            print "Invalid data coding!"

    def insert_book (self, provider, city, book):

        collection = self.db["books"]            
        try:
            collection.insert_one(book)
        except:
            print "Invalid data coding!"            

    def insert_fleet_day(self, day, provider, city, fleet):

        record = {
                     "day" : day,
                     "city": city,
                     "provider": provider,
                     "fleet": fleet
                 }     

        collection = self.db['fleet']

        try:
            collection.insert_one(record)
        except:
            print ('Error in insert_one INSERT_FLEET_DAY')
            
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
        
        return self.db["books"].update_one({"_id":  object_id},
                                              {"$set": feed},
                                              upsert = True)
        
    def query_fleet_by_day (self, provider, city, start, end):
        
        return self.db['fleet'].find \
                           ({
                               'day':
                                   {
                                       '$gt': start,
                                       '$lt': end
                                   },
                               'provider': provider,
                               'city':city
                           }).sort([("_id", 1)])        
                
    def query_raw_by_time (self, provider, city, start, end):
        
        return self.db["snapshots"].find \
                    ({"timestamp":
                         {
                             '$gte': start,
                             '$lt': end
                         },
                     "provider":provider,
                     "city":city
                    }).sort([("_id", 1)])

    def query_fleet (self, provider, city):

        return self.db["fleet"].find \
                    ({
                     "provider":provider,
                     "city":city
                    }).sort([("_id", 1)])
                        
    def query_parks (self, provider, city, start, end):
        
        return self.db["parks"].find \
                    ({"start":
                         {
                             '$gte': start,
                             '$lt': end
                         },
                     "provider":provider,
                     "city":city
                     }).sort([("_id", 1)])

    def query_books (self, provider, city, start, end):
        
        return self.db["books"].find \
                    ({"start":
                         {
                             '$gte': start,
                             '$lt': end
                         },
                     "provider":provider,
                     "city":city
                    }).sort([("_id", 1)])

    def process_books_df (self, provider, books_df):

        def riding_time (provider, df):    
         
            df["reservation_time"] = df["duration"] - df["duration_driving"]
            df.loc[df.reservation_time < 0, "riding_time"] = df["duration"]
            df.loc[df.reservation_time > 0, "riding_time"] = df["duration_driving"]
            
            return df        
        
        def get_bill (provider, df):
            
            if provider == "car2go":
                free_reservation = 20
                ticket = 0.24
                extra_ticket = 0.24    
            elif provider == "enjoy":
                free_reservation = 15
                ticket = 0.25
                extra_ticket = 0.10    
         
            indexes = df.loc[df.reservation_time > free_reservation].index
            extra_minutes = df.loc[indexes, 'reservation_time'] - free_reservation
            df.loc[indexes,"min_bill"] = df.loc[indexes, 'riding_time'].apply(lambda x: x * ticket) + \
                                                    extra_minutes.apply(lambda x: x * extra_ticket)                                            
            df.loc[indexes,"max_bill"] = df.loc[indexes, 'duration'].apply(lambda x: x * ticket)
                                                 
            indexes = df.loc[(df.reservation_time <= free_reservation) & (df.reservation_time > 0)].index
            df.loc[indexes,"min_bill"] = df.loc[indexes, 'riding_time'].apply(lambda x: x * ticket)                    
            df.loc[indexes,"max_bill"] = df.loc[indexes, 'riding_time'].apply(lambda x: x * ticket)
           
            indexes = df.loc[df.reservation_time < 0].index
            df.loc[indexes,"min_bill"] = df.loc[indexes, 'riding_time'].apply(lambda x: x * ticket)
            df.loc[indexes,"max_bill"] = df.loc[indexes, 'riding_time'].apply(lambda x: x * ticket)        
            
            return df
                       
        books_df["duration"] = \
            (books_df["end"] - books_df["start"])/np.timedelta64(1, 'm')
        books_df["distance"] = books_df.apply\
            (lambda row: haversine(row["start_lon"], row["start_lat"], 
                                   row["end_lon"], row["end_lat"]), axis=1)
        books_df["fuel_consumption"] = \
            books_df["start_fuel"] - books_df["end_fuel"]

        books_df = riding_time(provider, books_df)
        books_df = get_bill(provider, books_df)

        return books_df                         
                        
    def query_parks_df (self, provider, city, start, end):
        
        parks_cursor = self.query_parks(provider, city, start, end)
        parks_df = pd.DataFrame(columns = pd.Series(parks_cursor.next()).index)
        for doc in parks_cursor:
            s = pd.Series(doc)
            parks_df = pd.concat([parks_df, pd.DataFrame(s).T], ignore_index=True)    

        parks_df["duration"] = \
            (parks_df["end"] - parks_df["start"])/np.timedelta64(1, 'm')            
            
        return parks_df\
                    [
                     [
                         "city",
                         "provider",
                         "plate",
                         "_id",
                         "start",
                         "end",
                         "lat",
                         "lon",
                         "duration", 
                     ]
                    ]
                        
    def query_books_df (self, provider, city, start, end):
        
        books_cursor = self.query_books(provider, city, start, end)    
        books_df = pd.DataFrame(columns = pd.Series(books_cursor.next()).index)
        for doc in books_cursor:
            s = pd.Series(doc)
            books_df = pd.concat([books_df, pd.DataFrame(s).T], ignore_index=True)           
        
        return self.process_books_df(provider, books_df).replace({None:np.NaN})\
                    [
                     [
                         "city",
                         "provider",
                         "plate",
                         "_id",
                         "start",
                         "end",
                         "start_lat",
                         "start_lon",
                         "end_lat", 
                         "end_lon", 
                         "distance", 
                         "duration", 
                         "fuel_consumption",
                         "reservation_time",
                         "riding_time",
                         "distance_driving",
                         "duration_driving",
                         "distance_google_transit",
                         "duration_google_transit",
                         "tot_duration_google_transit",
                         "min_bill",
                         "max_bill",
                         "fare_google_transit"
                     ]
                    ]

    def query_parks_df_intervals (self, provider, city, dates_list):
        
        parks_cursor = self.query_parks_intervals(provider, city, dates_list)
        parks_df = pd.DataFrame(columns = pd.Series(parks_cursor.next()).index)
        for doc in parks_cursor:
            s = pd.Series(doc)
            parks_df = pd.concat([parks_df, pd.DataFrame(s).T], ignore_index=True)    

        parks_df["duration"] = \
            (parks_df["end"] - parks_df["start"])/np.timedelta64(1, 'm')            
            
        return parks_df\
                    [
                     [
                         "city",
                         "provider",
                         "plate",
                         "_id",
                         "start",
                         "end",
                         "lat",
                         "lon",
                         "duration", 
                     ]
                    ]

    def query_books_df_intervals (self, provider, city, dates_list):
        
        books_cursor = self.query_books_intervals(provider, city, dates_list)    
        books_df = pd.DataFrame(columns = pd.Series(books_cursor.next()).index)
        for doc in books_cursor:
            s = pd.Series(doc)
            books_df = pd.concat([books_df, pd.DataFrame(s).T], ignore_index=True)           
        
        return self.process_books_df(provider, books_df).replace({None:np.NaN})\
                    [
                     [
                         "city",
                         "provider",
                         "plate",
                         "_id",
                         "start",
                         "end",
                         "start_lat",
                         "start_lon",
                         "end_lat", 
                         "end_lon", 
                         "distance", 
                         "duration", 
                         "fuel_consumption",
                         "reservation_time",
                         "riding_time",
                         "distance_driving",
                         "duration_driving",
                         "distance_google_transit",
                         "duration_google_transit",
                         "tot_duration_google_transit",
                         "min_bill",
                         "max_bill",
                         "fare_google_transit"
                     ]
                    ]

    def filter_df_outliers (self, df):
        return df[(df.distance > 0.03) & (df.duration > 5) & (df.duration < 120)]
                    
    def filter_df_days (self, df, day_type, start, end):
        
        cal = Italy()
        
        holidays = []
        pre_holidays = []
       
        #holidays collection creation
        if start.year == end.year:
            for h in cal.holidays(start.year):
                holidays.append(h[0])
        else:
            for year in range (start.year, end.year+1):
                for h in cal.holidays(year):
                    holidays.append(h[0])
                     
        for d in holidays:
            if (d - datetime.timedelta(days = 1)) not in holidays:
                pre_holidays.append(d - datetime.timedelta(days = 1))
                             
        df['week_day'] = df['start'].apply(lambda x: x.weekday())

        df['h_day'] = df['start'].apply(lambda x: x.date()).isin(holidays)

        df['ph_day'] = df['start'].apply(lambda x: x.date()).isin(pre_holidays)
        
        if day_type == "business":
            return df[(df.week_day >= 0) & (df.week_day <= 4) & (df.h_day == False)]
        if day_type == "weekend":
            return df[(df.week_day >= 5) & (df.week_day <= 6) & (df.h_day == False)]
        if day_type == "holiday":
            return df[df.h_day == True]
        if day_type == "preholiday":
            return df[df.ph_day == True]

        return df

    def filter_date (self, start, end, day_type):
        
        cal = Italy()
        
        holidays = []
        holidays_ = []
        pre_holidays = []
        pre_holidays_ = []
        business = []
        weekends = []
       
        #holidays collection creation
        if start.year == end.year:
            for h in cal.holidays(start.year):
                holidays.append(h[0])
        else:
            for year in range (start.year, end.year+1):
                for h in cal.holidays(year):
                    holidays.append(h[0])
                     
        for d in holidays:
            if (d - datetime.timedelta(days = 1)) not in holidays:
                pre_holidays.append(d - datetime.timedelta(days = 1))

        date_list = [end - datetime.timedelta(days=x) for x in range(0, (end-start).days+1)]

        if day_type == "business":
            for day in date_list:
                if (day.weekday() >= 0) & (day.weekday() <= 4) & (day not in holidays):
                    business.append(day)
            return business

        if day_type == "weekend":
            for day in date_list:
                if (day.weekday() >= 5) & (day.weekday() <= 6) & (day not in holidays):
                    weekends.append(day)
            return weekends

        if day_type == "holiday":
            for day in date_list:
                if (day.date() in holidays):
                    holidays_.append(day)
            return holidays_

        if day_type == "preholiday":
            for day in date_list:
                if (day.date() in holidays):
                    pre_holidays_.append(day)
            return pre_holidays_

    def query_books_intervals(self, provider, city, dates_list):

        query = []
        for end_ in dates_list:
            start_ = (end_ - datetime.timedelta(days = 1))
            q = {'start': {
                            '$gt': start_,
                            '$lt': end_
                            }
                }
            query.append(q)

        return self.db['books'].find \
                    ({ 
                        '$or': query,
                        'provider': provider,
                        'city': city                      
                    })

    def query_parks_intervals(self, provider, city, dates_list):

        query = []
        for end_ in dates_list:
            start_ = (end_ - datetime.timedelta(days = 1))
            q = {'start': {
                            '$gt': start_,
                            '$lt': end_
                            }
                }
            query.append(q)

        return self.db['parks'].find \
                    ({ 
                        '$or': query,
                        'provider': provider,
                        'city': city                      
                    })
        
    def query_books_df_filtered (self, provider, city, start, end, day_type):

        books_df = self.query_books_df(provider, city, start, end)
        return self.filter_df_days(books_df, day_type, start, end)

    def query_parks_df_filtered (self, provider, city, start, end, day_type):

        parks_df = self.query_parks_df(provider, city, start, end)
        return self.filter_df_days(parks_df, day_type, start, end)

    def query_books_df_filtered_v2 (self, provider, city, start, end, day_type):

        if day_type == "full":
            return self.query_books_df(provider, city, start, end)
        else:
            lista_date = self.filter_date(start, end, day_type)
            return self.query_books_df_intervals(provider, city, lista_date)

    def query_parks_df_filtered_v2 (self, provider, city, start, end, day_type):
        
        if day_type == "full":
            return self.query_parks_df(provider, city, start, end)
        else:
            lista_date = self.filter_date(start, end, day_type)
            return self.query_parks_df_intervals(provider, city, lista_date)
