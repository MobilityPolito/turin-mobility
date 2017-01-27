
import googlemaps
import datetime
from DataBaseProxy import DataBaseProxy
import pandas as pd
from pymongo import MongoClient
dbp = DataBaseProxy()
import numpy as np
import pytz
client = MongoClient('mongodb://localhost:27017/')



def get_books (provider, city, start, end):
    books_cursor = dbp.query_book_by_time(provider, city, start, end)    
    books_df = pd.DataFrame(columns = pd.Series(books_cursor.next()).index)
    for doc in books_cursor:
        s = pd.Series(doc)
        books_df = pd.concat([books_df, pd.DataFrame(s).T], ignore_index=True)    

    return books_df



def next_weekday(now, rental_time):
    days_ahead = rental_time.weekday() - now.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    nextday = now + datetime.timedelta(days_ahead)
    return nextday.replace(hour = rental_time.hour, 
                           minute = rental_time.minute, 
                           second = rental_time.second)
    
end = datetime.datetime(2016, 12, 15, 0, 0, 0)
start = end - datetime.timedelta(days = 10)

city = "torino"
provider = "car2go"
start = datetime.datetime(2016, 12, 5, 0, 0, 0)
end = datetime.datetime(2016, 12, 20, 0, 0, 0)
books_df = dbp.query_books_df(provider, city, start, end)
books_df = books_df.replace({"nan":np.NaN})
books_df = books_df.replace({"None":np.NaN})
books_df = books_df.replace({None:np.NaN})

print "books acquired"
for i in range(len(books_df)):
    row = books_df.iloc[i]
    if ((row['start_lat']== row['end_lat']) and (row['end_lon']==row['end_lon'])):
        continue
    else:
        if ('arrival_time_google_transit' in row) and row.isnull()['arrival_time_google_transit'] == False and type(row['arrival_time_google_transit'])==int:
            print row['_id']
            scheduled_start = next_weekday(datetime.datetime.now(), row['start'])
            if type(row['arrival_time_google_transit'])==int:
                scheduled_end = next_weekday(datetime.datetime.now(),\
                                             datetime.datetime.fromtimestamp(row['arrival_time_google_transit'], pytz.utc))
            else:
                scheduled_end = next_weekday(datetime.datetime.now(), row['arrival_time_google_transit'])
            tot_dur = scheduled_end - scheduled_start
            tot_dur = tot_dur.total_seconds() / 60.0
            dbp.db["books"].update_one({"_id":  row['_id']},
                                       {"$set": {"tot_duration_google_transit": tot_dur }}, 
                                        upsert = True)
            print "1"
            
        if ('departure_time_google_transit' in row) and row.isnull()['departure_time_google_transit'] == False and type(row['departure_time_google_transit'])==int:
            departure_time_google_transit = datetime.datetime.fromtimestamp(row['departure_time_google_transit'], pytz.utc)
            dbp.db["books"].update_one({"_id":  row['_id']},
                           {"$set": {"departure_time_google_transit": departure_time_google_transit }}, 
                            upsert = True)
            print "2"


        if ('duration_google_transit' in row) and row.isnull()['duration_google_transit'] == False and type(row['duration_google_transit'])==int:
            duration_google_transit = row['duration_google_transit']/60.0
            dbp.db["books"].update_one({"_id":  row['_id']},
               {"$set": {"duration_google_transit": duration_google_transit }}, 
                upsert = True)
            print "3"

 
        if ('duration_driving' in row) and row.isnull()['duration_driving'] == False and type(row['duration_driving'])==int:
            duration_driving = row['duration_driving']/60.0
            dbp.db["books"].update_one({"_id":  row['_id']},
               {"$set": {"duration_driving": duration_driving }}, 
                upsert = True)
            print "3"
        
            
        if ('distance_driving' in row) and row.isnull()['distance_driving'] == False and type(row['distance_driving'])==int:
            distance_driving = row['distance_driving']/1000.0
            dbp.db["books"].update_one({"_id":  row['_id']},
               {"$set": {"distance_driving": distance_driving }}, 
                upsert = True)
            print "4"

        
        if ('distance_google_transit' in row) and row.isnull()['distance_google_transit'] == False and type(row['distance_google_transit'])==int:
            distance_google_transit = row['distance_google_transit']/1000.0
            dbp.db["books"].update_one({"_id":  row['_id']},
               {"$set": {"distance_google_transit": distance_google_transit }}, 
                upsert = True)
            print "5"

            
