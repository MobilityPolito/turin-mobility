#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 17:26:00 2016
@author: root
"""
import googlemaps
import datetime

def next_weekday(now, rental_time):
    days_ahead = rental_time.weekday() - now.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    nextday = now + datetime.timedelta(days_ahead)
    return nextday.replace(hour = rental_time.hour, 
                           minute = rental_time.minute, 
                           second = rental_time.second)

google_day = next_weekday(datetime.datetime.now(), books_df['start'][0])
    
o_lat = books_df['start_lat'][0]
o_lon = books_df['start_lon'][0]
d_lat = books_df['end_lat'][0]
d_lon = books_df['end_lon'][0]

gmaps = googlemaps.Client(key='AIzaSyBnUsB3u6Blg23D5uqIQPnM_1Pawkp5VLY')
directions_result = gmaps.directions([o_lat, o_lon], 
                                     [d_lat, d_lon], 
                                     mode="transit", 
                                     departure_time = google_day)
