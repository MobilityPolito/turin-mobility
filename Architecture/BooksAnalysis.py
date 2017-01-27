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

import numpy as np
import pandas as pd

import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import LineString

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

from pandas.tools.plotting import scatter_matrix

from DataBaseProxy import DataBaseProxy
dbp = DataBaseProxy()
    
def process_books_df (provider, books_df):

    def get_bill (books_df, provider):
        
        if provider == "car2go":
            books_df["bill"] = books_df["durations"].apply(lambda x: x * 0.24)
        elif provider == "enjoy":
            books_df["bill"] = books_df["durations"].apply(lambda x: x * 0.25)
            
        return books_df
    
    books_df["durations"] = \
        (books_df["end"] - books_df["start"])/np.timedelta64(1, 'm')
    books_df["distances"] = books_df.apply\
        (lambda row: haversine(row["start_lon"], row["start_lat"], 
                               row["end_lon"], row["end_lat"]), axis=1)
    books_df = get_bill(books_df, provider)
        
    books_df["geometry"] = books_df.apply\
        (lambda row: LineString([(row["start_lon"], row["start_lat"]),
                                 (row["end_lon"], row["end_lat"])]), axis=1)
    books_df = gpd.GeoDataFrame(books_df, geometry="geometry")
    books_df.crs = {"init": "epsg:4326"}
    
    books_df = books_df[books_df.durations < 120]
    books_df = books_df[books_df.distances > 1]

    return books_df    
    
def get_books_days (city, provider, end, depth):
    
    start = end - datetime.timedelta(days = depth)
    books_df = dbp.get_books(provider, city, start, end)
    
    return process_books_df(provider, books_df)

def get_books_day (city, provider, year, month, day):
        
    end = datetime.datetime(year, month, day, 23, 59, 59)
    start = end - datetime.timedelta(days = 1)
    books_df = dbp.get_books(provider, city, start, end)
    
    return process_books_df(provider, books_df)

def day_analysis (books_df, year, month, day):

    day_stats = pd.DataFrame()
    start = datetime.datetime(year, month, day, 0, 0, 0)
    end = datetime.datetime(year, month, day, 23, 59, 0)
    provider = books_df["provider"].unique()[0]
    city = books_df["city"].unique()[0]
    fleet_size = float(len(dbp.query_fleet_by_day(provider, city, start, end)[0]["fleet"]))

    for hour in range(0, 24, 1):
        sup_datetime = datetime.datetime(year, month, day, hour, 59, 59)
        inf_datetime = datetime.datetime(year, month, day, hour, 0, 0)

        day_stats.loc[sup_datetime, "n"] = \
            float(len(books_df[inf_datetime:sup_datetime]))
            
        day_stats.loc[sup_datetime, "n_norm"] = \
            float(len(books_df[inf_datetime:sup_datetime]))/fleet_size

        day_stats.loc[sup_datetime, "avg_duration"] = \
            books_df[inf_datetime:sup_datetime]["duration"].mean()
            
        day_stats.loc[sup_datetime, "med_duration"] = \
            books_df[inf_datetime:sup_datetime]["duration"].median()

        day_stats.loc[sup_datetime, "avg_books_distance"] = \
            books_df[inf_datetime:sup_datetime]["distance_driving"].mean()
        day_stats.loc[sup_datetime, "med_books_distance"] = \
            books_df[inf_datetime:sup_datetime]["distance_driving"].median()
        
        day_stats.loc[sup_datetime, "min_bill"] = \
            books_df[inf_datetime:sup_datetime]["min_bill"].sum()

        day_stats.loc[sup_datetime, "max_bill"] = \
            books_df[inf_datetime:sup_datetime]["max_bill"].sum()

    return day_stats

def get_books_hours_stats (books_df):

    books_df = books_df[books_df.duration < 300]
    books_df = books_df[books_df.distance > 0.1]
    
    books_df["start_"] = books_df["start"]
    books_df = books_df.set_index("start_").sort_index()
    books_df["date"] = books_df["start"].apply(lambda x: x.date())
    
    stats = pd.DataFrame()
    for date, group in books_df.groupby("date"):
        stats = pd.concat([stats, day_analysis(group, date.year, date.month, date.day)])
    stats["time"] = pd.Series(stats.index.values).apply(lambda x: x.time()).values

    return books_df, stats.groupby("time").aggregate(np.mean)

def group_books_by_hour (books_df):

    books_df["start_"] = books_df["start"]
    books_df = books_df.set_index("start_").sort_index()
    books_df["hour"] = books_df["start"].apply(lambda x: x.hour)
    
    return books_df


# start = datetime.datetime(2016, 12, 5, 0, 0, 0)
# end = datetime.datetime(2016, 12, 16, 23, 59, 59)
# #end = datetime.datetime.now()

# car2go_books = dbp.query_books_df_filtered("car2go", "torino", start, end, "business")
# #enjoy_books = dbp.query_books_df_filtered("enjoy", "torino", start, end, "business")
 
# car2go_books_modified, car2go_books_stats = get_books_hours_stats(car2go_books)
#enjoy_books_modified, enjoy_books_stats = get_hours_stats(enjoy_books)

#car2go_books_hour = group_books_by_hour(car2go_books)
#enjoy_books_hour = group_books_by_hour(enjoy_books)

#books_df = get_books_day("torino", "car2go", 2016, 12, 6)

#fig, ax = plt.subplots(1,1,figsize=(10,10))
#ax = scatter_matrix(books_df_car2go[["start_lat","start_lon","end_lat","end_lon","durations", "distances"]].astype("float64"), 
#               figsize=(10, 10), diagonal='kde')
#plt.savefig(provider + "_books_scatter_matrix.png")

#zones = gpd.read_file("../../SHAPE/Zonizzazione.dbf")\
#        .to_crs({"init": "epsg:4326"})
#zones_geo = zones["geometry"]

#fig, ax = plt.subplots(1,1,figsize=(10,10))
#ax = zones_geo.plot(color="white", ax=ax)
##-car2go
#ax.set_xlim([7.6, 7.8])
#ax.set_ylim([45.0,45.20])
##-enjoy
##ax.set_xlim([7.6, 7.8])
##ax.set_ylim([44.95,45.12])
#ax = books_df.plot(ax=ax)
#fig.savefig(provider + "_books_pattern.png")
