#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 15:46:14 2017

@author: Flavia
"""

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

#import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

#import geopandas as gpd
#from shapely.geometry import LineString


from DataBaseProxy import DataBaseProxy
dbp = DataBaseProxy()


def process_books_df(provider, books_df):


        
    books_df["durations"] = \
        (books_df["end"] - books_df["start"])/np.timedelta64(1, 'm')
    books_df["beeline_distances"] = books_df.apply\
        (lambda row: haversine(row["start_lon"], row["start_lat"], 
                               row["end_lon"], row["end_lat"]), axis=1)
#    books_df = max_bill(books_df, provider)
        
#    books_df["geometry"] = books_df.apply\
#        (lambda row: LineString([(row["start_lon"], row["start_lat"]),
#                                 (row["end_lon"], row["end_lat"])]), axis=1)
#    books_df = gpd.GeoDataFrame(books_df, geometry="geometry")
#    books_df.crs = {"init": "epsg:4326"}
    
    books_df = books_df[books_df.durations < 120]
    books_df = books_df[books_df.beeline_distances > 1]

    return books_df  
    

    
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
    df.loc[indexes,"max_bill"] = df.loc[indexes, 'durations'].apply(lambda x: x * ticket)
                                          
    indexes = df.loc[(df.reservation_time <= free_reservation) & (df.reservation_time > 0)].index
    df.loc[indexes,"min_bill"] = df.loc[indexes, 'riding_time'].apply(lambda x: x * ticket)                     
    df.loc[indexes,"max_bill"] = df.loc[indexes, 'riding_time'].apply(lambda x: x * ticket)
    
    indexes = df.loc[df.reservation_time < 0].index
    df.loc[indexes,"min_bill"] = df.loc[indexes, 'riding_time'].apply(lambda x: x * ticket)
    df.loc[indexes,"max_bill"] = df.loc[indexes, 'riding_time'].apply(lambda x: x * ticket)        
    return df 
    
   
def riding_time (provider, df):    
#    if provider == "car2go":
#        free_reservation = 20
#    elif provider == "enjoy":
#        free_reservation = 15
    df["reservation_time"] = df["durations"] - df["duration_driving"]
#    df.loc[df.reservation_time < 0, "reservation_time"] = 0
    df.loc[df.reservation_time < 0, "riding_time"] = df["durations"]
    df.loc[df.reservation_time > 0, "riding_time"] = df["duration_driving"]
    return df
 
free_reservation = 20    
end = datetime.datetime(2016, 12, 8, 0, 0, 0)
start = end - datetime.timedelta(days = 1)
bookings_DF = dbp.get_books("car2go", "torino", start, end)
df = process_books_df("car2go", bookings_DF)
df = riding_time("car2go", df)
df = get_bill("car2go", df)


#df = get_bill(df, "car2go")

plt.plot(df['max_bill'])    
 
plt.plot(df['min_bill'])    


plt.show()
