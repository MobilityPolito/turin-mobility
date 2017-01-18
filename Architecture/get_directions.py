#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 17:26:00 2016
@author: root
"""
import googlemaps
import datetime
from DataBaseProxy import DataBaseProxy
import pandas as pd
import time
from pymongo import MongoClient
dbp = DataBaseProxy()
gmaps = googlemaps.Client(key='AIzaSyBnUsB3u6Blg23D5uqIQPnM_1Pawkp5VLY')

client = MongoClient('mongodb://localhost:27017/')


# Books durations

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

end = datetime.datetime(2016, 12, 9, 0, 0, 0)
start = end - datetime.timedelta(days = 1)

books_df = get_books("car2go","torino", start, end) 
ii = 454
google_day = next_weekday(datetime.datetime.now(), books_df['start'][ii])
    
o_lat = books_df['start_lat'][ii]
o_lon = books_df['start_lon'][ii]
d_lat = books_df['end_lat'][ii]
d_lon = books_df['end_lon'][ii]


directions_result_2 = gmaps.directions([o_lat, o_lon], 
                                     [d_lat, d_lon], 
                                     mode="transit", 
                                     departure_time = google_day)
#
#if directions_result_2[0]["legs"][0]["steps"][0]["travel_mode"] == 'DRIVING':
#    print directions_result_2[0]["legs"][0]["duration_in_traffic"]
#else:
#    print "soppalco"

#
#time.sleep(10)
#
#directions_result = gmaps.directions([o_lat, o_lon], 
#                                     [d_lat, d_lon], 
#                                     mode="transit", 
#                                     departure_time = google_day)
#
#
#db = client['CSMS_']['torino_books_v2']
#db.update_one({"_id":  books_df['_id'][ii]}, {"$set": { 'departure_time_google_transit': directions_result[0]["legs"][0]["departure_time"]["value"],
#                                                        'arrival_time_google_transit': directions_result[0]["legs"][0]["arrival_time"]["value"],
##                                                        'arrival_time_google_driving': directions_result_2[0]["legs"][0]["arrival_time"]["value"],
#                                                        'distance_driving' : directions_result_2[0]["legs"][0]["distance"]["value"],
#                                                        'duration_driving' : directions_result_2[0]["legs"][0]["duration"]["value"],
#                                                        'distance_google_transit': directions_result[0]["legs"][0]["distance"]["value"],
#                                                        'duration_google_transit': directions_result[0]["legs"][0]["duration"]["value"],
#                                                        'fare_google_transit': directions_result[0]["fare"]["value"]} }, 
#                                                         upsert = True)
#
#


#
#
#
#def get_directions(bookings):
#    df = pd.DataFrame(columns=['start_lat','start_lon','end_lat','end_lon','departure_time','arrival_time','distance','duration','fare'], index=bookings.index.values)
#
#    i = 0
#    for index, row in bookings.iterrows():
#        googleday = next_weekday(datetime.datetime.now(), row['start']) 
#        origin = [row['start_lat'],  row['start_lon']]
#        destination =[row['end_lat'], row['end_lon']]
#        if index < 10:
#            directions_result = gmaps.directions(origin,
#                                                 destination,
#                                                 mode='transit',
#                                                 departure_time=googleday)
#            print index
#            try:
#                df.loc[index] = pd.Series({ 'start_lat':row['start_lat'],
#                                                'start_lon' :row['start_lon'],
#                                                'end_lat' :row['end_lat'], 
#                                                'end_lon': row['end_lon'],
#                                                'departure_time': directions_result[0]["legs"][0]["departure_time"]["value"],
#                                                'arrival_time': directions_result[0]["legs"][0]["arrival_time"]["value"],
#                                                'distance': directions_result[0]["legs"][0]["distance"]["value"],
#                                                'duration': directions_result[0]["legs"][0]["duration"]["value"],
#                                                'fare': directions_result[0]["fare"]["value"]
#                                                })  
#            except:
#                print "problema su index "
#                print index
#        else:
#            return i, df
#        time.sleep(7)
#
#   
#i, directions_df = get_directions(books_df)

