#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 16:03:06 2017

@author: root
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 17:26:00 2016

@author: root
"""
from DataBaseProxy import DataBaseProxy
import googlemaps
import datetime
import googlemaps
import pandas as pd
import time

dbp = DataBaseProxy()
gmaps = googlemaps.Client(key='AIzaSyDbPG5qS-g0pROiPRcOT2G-keWi54ie2-M')

# Books durations

def get_books (provider, city, start, end):
    books_cursor = dbp.query_book_by_time(provider, city, start, end)    
    books_df = pd.DataFrame(columns = pd.Series(books_cursor.next()).index)
    for doc in books_cursor:
        s = pd.Series(doc)
        books_df = pd.concat([books_df, pd.DataFrame(s).T], ignore_index=True)    

    return books_df

class futureDay():
    def __init__(self):
        pass
        
    def next_weekday(self, d, rental_time):
        days_ahead = rental_time.weekday() - d.weekday()
        if days_ahead <= 0: # Target day already happened this week
            days_ahead += 7
        nextday = d + datetime.timedelta(days_ahead)
        self.nextday = nextday.replace(hour = rental_time.hour, minute = rental_time.minute, second = rental_time.second)

    
giorno = futureDay()  
end = datetime.datetime(2016, 12, 10, 0, 0, 0)
start = end - datetime.timedelta(days = 1)

books_df = get_books("car2go","torino", start, end) 
   
giorno1 = giorno.next_weekday(datetime.datetime.now(), books_df['start'][0])

directions_result = gmaps.directions([books_df['start_lat'][0], books_df['start_lon'][0]], [books_df['end_lat'][0], books_df['end_lon'][0]], mode="transit", departure_time = giorno1)
time.sleep(10)
directions_result_ = gmaps.directions([books_df['start_lat'][0], books_df['start_lon'][0]], [books_df['end_lat'][0], books_df['end_lon'][0]], departure_time = giorno1)

#
#gmaps2 = googlemaps.Client(key='AIzaSyAcPVep5aXJLbuBDV7Qn_JaWSpD4o6s30w')
#
#
#giorno2 = giorno.next_weekday(datetime.datetime.now(), books_df['start'][2])
#
#directions_result_2 = gmaps.directions([books_df['start_lat'][1], books_df['start_lon'][1]], [books_df['end_lat'][1], books_df['end_lon'][1]], mode="transit", departure_time = giorno.nextday)


#directions_result = gmaps.directions("via giovanni fattori 4 torino", "corso peschiera 200 torino", mode="transit")
#
#
#def get_directions(bookings):
#    giorno = futureDay()  
#    df = pd.DataFrame(columns=['start_lat','start_lon','end_lat','end_lon','departure_time','distance','duration','fare'], index=bookings.index.values)
#    i = 0
#    for index, row in bookings.iterrows():
#        giorno.next_weekday(datetime.datetime.now(), row['start']) 
#        directions_result = gmaps.directions([row['start_lat'],  row['start_lon']],
#                                        [row['end_lat'], row['end_lon']],
#                                         mode='transit',
#                                         departure_time=giorno.nextday)
#        i = i+1
#        print i
#        if "fare" in directions_result[0]:        
#            df.loc[index] = pd.Series({'start_lat':row['start_lat'], 
#                                                    'start_lon' :row['start_lon'], 
#                                                    'end_lat' :row['end_lat'], 
#                                                    'end_lon': row['end_lon'],
#                                                    'departure_time':giorno.nextday,
#                                                    'distance': directions_result[0]["legs"][0]["distance"]["value"],
#                                                    'duration': directions_result[0]["legs"][0]["duration"]["value"],
#                                                    'fare': directions_result[0]["fare"]["value"]
#                                                     })
#    return df
#
#   
#directions_df = get_directions(books_df)



    