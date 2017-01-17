import datetime

import numpy as np
import pandas as pd
from scipy import ndimage

import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import LineString

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

from pandas.tools.plotting import scatter_matrix

from DataBaseProxy import DataBaseProxy
dbp = DataBaseProxy()
    
from BooksAnalysis import get_books_day, get_books_days
from ParksAnalysis import get_parks_day

def day_analysis (city, provider, year, month, day, fleet_size):

    books_df = get_books_day(city, provider, year, month, day)\
        .set_index("start").sort_index()
    parks_df = get_parks_day(city, provider, year, month, day)\
        .set_index("start").sort_index()
    day_stats = pd.DataFrame(columns = ["n_parks", 
                                        "n_books", 
                                        "avg_books_duration", 
                                        "avg_books_distance"])
    for hour in range(0, 24, 1):
        sup_datetime = datetime.datetime(year, month, day, hour, 59, 59)
        inf_datetime = datetime.datetime(year, month, day, hour)
        day_stats.loc[sup_datetime, "n_parks"] = \
            len(parks_df[inf_datetime:sup_datetime])
        day_stats.loc[sup_datetime, "n_books_norm"] = \
            float(len(books_df[inf_datetime:sup_datetime])) / fleet_size
        day_stats.loc[sup_datetime, "avg_books_duration"] = \
            books_df[inf_datetime:sup_datetime]["durations"].mean()
        day_stats.loc[sup_datetime, "avg_books_distance"] = \
            books_df[inf_datetime:sup_datetime]["distances"].mean()
        day_stats.loc[sup_datetime, "avg_books_bill"] = \
            books_df[inf_datetime:sup_datetime]["bill"].sum()
        
    return books_df, parks_df, day_stats

def getODmatrix (city, provider, year, month, day):
    
    end = datetime.datetime(year, month, day + 1, 0, 0, 0)
    depth = 7    

    books_df = get_books_days(city, provider, end, depth)\
        .set_index("start").sort_index()
    
    origins = books_df[["start_lat","start_lon"]]
    origins["geometry"] = origins.apply\
        (lambda row: Point(row.loc["start_lon"], row.loc["start_lat"]), 
         axis=1)    

    destinations = books_df[["end_lat","end_lon"]]
    destinations["geometry"] = destinations.apply\
        (lambda row: Point(row.loc["end_lon"], row.loc["end_lat"]), 
         axis=1)    

    zones = gpd.read_file("../../SHAPE/Zonizzazione.dbf")\
            .to_crs({"init": "epsg:4326"})

    OD = pd.DataFrame(0.0, index = zones.index.union(["sum"]), 
                      columns = zones.index.union(["sum"]))

    for i in range(len(books_df)):
        o = origins.ix[i, "geometry"]
        d = destinations.ix[i, "geometry"]
        intersect_o = zones.contains(o)
        intersect_d = zones.contains(d)
        zo = intersect_o[intersect_o == True].index.values[0]
        zd = intersect_d[intersect_d == True].index.values[0]
        OD.loc[zo, zd] += 1

#    OD["sum"] = OD.sum(axis=1)
#    OD.loc["sum"] = OD.sum()
#    OD.loc["sum","sum"]

    return zones, origins, destinations, OD
    
#zones, origins, destinations, od = getODmatrix("torino", "car2go", 2017, 1, 8)
