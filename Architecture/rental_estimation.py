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
#
#import geopandas as gpd
#from shapely.geometry import Point
#from shapely.geometry import LineString
 
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
       
#    books_df["geometry"] = books_df.apply\
#        (lambda row: LineString([(row["start_lon"], row["start_lat"]),
#                                 (row["end_lon"], row["end_lat"])]), axis=1)
#    books_df = gpd.GeoDataFrame(books_df, geometry="geometry")
#    books_df.crs = {"init": "epsg:4326"}
   
    books_df = books_df[books_df.durations < 120]
    books_df = books_df[books_df.distances > 1]
 
    return books_df
   
def minmax_bill (provider, df):
    process_books_df(provider,df)
    riding_time(provider, df)
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
                                            extra_minutes.apply(lambda x: x * extra_ticket) # extra bill to res                                      
    df.loc[indexes,"max_bill"] = df.loc[indexes, 'durations'].apply(lambda x: x * ticket)   # no reservation, all rentals
                                         
    indexes = df.loc[(df.reservation_time <= free_reservation) & (df.reservation_time > 0)].index
    df.loc[indexes,"min_bill"] = df.loc[indexes, 'riding_time'].apply(lambda x: x * ticket) #                    
    df.loc[indexes,"max_bill"] = df.loc[indexes, 'riding_time'].apply(lambda x: x * ticket) #
   
    indexes = df.loc[df.reservation_time < 0].index
    df.loc[indexes,"min_bill"] = df.loc[indexes, 'riding_time'].apply(lambda x: x * ticket)
    df.loc[indexes,"max_bill"] = df.loc[indexes, 'riding_time'].apply(lambda x: x * ticket)
    return df
   
def get_duration_transit(df):
    indexes = df.loc[df.fare.notnull].index
    waiting_time = (df[indexes,"departure_time_google"].time() - df[indexes,"start"].time())/np.timedelta64(1, 'm')
    df[indexes,"tot_duration_transit"] = df[indexes, "duration_google_transit"] + waiting_time
 
def riding_time (provider, df):    
 
   
    df["reservation_time"] = df["durations"] - df["duration_driving"]
    df.loc[df.reservation_time < 0, "riding_time"] = df["durations"]
    df.loc[df.reservation_time > 0, "riding_time"] = df["duration_driving"]
    return df
   
def get_books_days (city, provider, end, depth):
   
    start = end - datetime.timedelta(days = depth)
    books_df = dbp.get_books(provider, city, start, end)
   
    return process_books_df(provider, books_df)
 
def get_books_day (city, provider, year, month, day):
       
    end = datetime.datetime(year, month, day, 23, 59, 59)
    start = end - datetime.timedelta(days = 1)
    books_df = dbp.get_books(provider, city, start, end)
   
    return process_books_df(provider, books_df)
 
#df = process_books_df("car2go", df)
df = minmax_bill("car2go", df)
 
#books_df = get_books_day("torino", "car2go", 2016, 12, 6)
 
#fig, ax = plt.subplots(1,1,figsize=(10,10))
#ax = scatter_matrix(df[["durations", "distances", "bill", "max_bill", "min_bill", "riding_time"]].astype("float64"),
#               figsize=(10, 10), diagonal='kde')
#plt.savefig("car2go" + "_books_scatter_matrix.png")
 
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