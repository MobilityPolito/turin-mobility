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
    
# Books durations

def get_books_df (provider, city, start, end):

    books_cursor = dbp.query_book_by_time(provider, city, start, end)
    
    books_df = pd.DataFrame(columns = pd.Series(books_cursor.next()).index)
    for doc in books_cursor:
        s = pd.Series(doc)
        books_df = pd.concat([books_df, pd.DataFrame(s).T], ignore_index=True)    

    return books_df
    
provider = "car2go"
    
end = datetime.datetime(2016, 12, 10, 0, 0, 0)
start = end - datetime.timedelta(days = 1)
books_df = get_books_df(provider, "torino", start, end)
books_df["durations"] = (books_df["end"] - books_df["start"])/np.timedelta64(1, 'm')
books_df["distances"] = books_df.apply\
    (lambda row: haversine(row["start_lon"], row["start_lat"], row["end_lon"], row["end_lat"]), axis=1)
books_df = books_df[books_df.durations < 120]
books_df = books_df[books_df.distances > 1]

books_df["geometry"] = books_df.apply\
    (lambda row: LineString([(row["start_lon"], row["start_lat"]),(row["end_lon"], row["end_lat"])]), axis=1)
books_df = gpd.GeoDataFrame(books_df, geometry="geometry")
books_df.crs = {"init": "epsg:4326"}
zones = gpd.read_file("../../SHAPE/Zonizzazione.dbf")\
        .to_crs({"init": "epsg:4326"})

#fig, ax = plt.subplots(1,1,figsize=(10,10))
#ax = scatter_matrix(books_df[["start_lat","start_lon","end_lat","end_lon","durations", "distances"]].astype("float64"), 
#               figsize=(10, 10), diagonal='kde')
#plt.savefig(provider + "_books_scatter_matrix.png")
#
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
