import datetime

import numpy as np
import pandas as pd
from scipy import ndimage

#import geopandas as gpd
#from shapely.geometry import Point
#from shapely.geometry import LineString

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

from pandas.tools.plotting import scatter_matrix

from DataBaseProxy import DataBaseProxy
dbp = DataBaseProxy()
    
from BooksAnalysis import get_books_day, get_books_days
#from ParksAnalysis import get_parks_day

def day_analysis (books_df, city, provider, year, month, day, fleet_size):

    stats = pd.DataFrame(columns = [
                                    "n_books",
                                    "n_books_norm",
                                    "avg_books_duration",
                                    "med_books_duration",
                                    "avg_books_duration_driving",
                                    "med_books_duration_driving",
                                    "avg_books_distance",
                                    "med_books_distance",
                                    "avg_books_distance_driving",
                                    "med_books_distance_driving",
                                    "avg_books_bill",
                                    "cum_books_bill",
                                    "avg_books_min_bill",
                                    "cum_books_min_bill",
                                    "avg_books_max_bill",
                                    "cum_books_max_bill"
                                    ])
    
    for hour in range(0, 24, 1):
        sup_datetime = datetime.datetime(year, month, day, hour, 59, 59)
        inf_datetime = datetime.datetime(year, month, day, hour)

        stats.loc[sup_datetime, "n_books"] = \
            float(len(books_df[inf_datetime:sup_datetime]))
        stats.loc[sup_datetime, "n_books_norm"] = \
            float(len(books_df[inf_datetime:sup_datetime])) / fleet_size

        stats.loc[sup_datetime, "avg_books_duration"] = \
            books_df[inf_datetime:sup_datetime]["durations"].mean()
        stats.loc[sup_datetime, "med_books_duration"] = \
            books_df[inf_datetime:sup_datetime]["durations"].median()
#        stats.loc[sup_datetime, "mode_books_duration"] = \
#            books_df[inf_datetime:sup_datetime]["durations"].mode()

        stats.loc[sup_datetime, "avg_books_duration_driving"] = \
            books_df[inf_datetime:sup_datetime]["duration_driving"].mean()
        stats.loc[sup_datetime, "med_books_duration_driving"] = \
            books_df[inf_datetime:sup_datetime]["duration_driving"].median()
#        stats.loc[sup_datetime, "mode_books_duration_driving"] = \
#            books_df[inf_datetime:sup_datetime]["durations"].mode()            
            
        stats.loc[sup_datetime, "avg_books_distance"] = \
            books_df[inf_datetime:sup_datetime]["distances"].mean()
        stats.loc[sup_datetime, "med_books_distance"] = \
            books_df[inf_datetime:sup_datetime]["distances"].median()
#        stats.loc[sup_datetime, "mode_books_distance"] = \
#            books_df[inf_datetime:sup_datetime]["distances"].mode()

        stats.loc[sup_datetime, "avg_books_distance_driving"] = \
            books_df[inf_datetime:sup_datetime]["distance_driving"].mean()
        stats.loc[sup_datetime, "med_books_distance_driving"] = \
            books_df[inf_datetime:sup_datetime]["distance_driving"].median()
#        stats.loc[sup_datetime, "mode_books_distance_driving"] = \
#            books_df[inf_datetime:sup_datetime]["distances"].mode()
            
        stats.loc[sup_datetime, "avg_books_bill"] = \
            books_df[inf_datetime:sup_datetime]["bill"].mean()
        stats.loc[sup_datetime, "cum_books_bill"] = \
            books_df[inf_datetime:sup_datetime]["bill"].sum()

        stats.loc[sup_datetime, "avg_books_min_bill"] = \
            books_df[inf_datetime:sup_datetime]["min_bill"].mean()
        stats.loc[sup_datetime, "cum_books_min_bill"] = \
            books_df[inf_datetime:sup_datetime]["min_bill"].sum()

        stats.loc[sup_datetime, "avg_books_max_bill"] = \
            books_df[inf_datetime:sup_datetime]["max_bill"].mean()
        stats.loc[sup_datetime, "cum_books_max_bill"] = \
            books_df[inf_datetime:sup_datetime]["max_bill"].sum()
            
    return stats

def getODmatrix (city, provider, year, month, day):
    
    end = datetime.datetime(year, month, day, 23, 59, 59)
    #depth = 15
    depth = 1 

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

    OD = pd.DataFrame(0.0, index = zones.index, 
                      columns = zones.index)

    for i in range(len(books_df)):
        try:

            o = origins.ix[i, "geometry"]
            d = destinations.ix[i, "geometry"]
            intersect_o = zones.contains(o)
            intersect_d = zones.contains(d)
            zo = intersect_o[intersect_o == True].index.values[0]
            zd = intersect_d[intersect_d == True].index.values[0]
            OD.loc[zo, zd] += 1
        except:
            print i

#    OD["sum"] = OD.sum(axis=1)
#    OD.loc["sum"] = OD.sum()
#    OD.loc["sum","sum"]

    return zones, origins, destinations, OD

stats = day_analysis(df, "torino", "car2go", 2016, 12, 7, 403.0)

fig, ax = plt.subplots(1, 2, figsize=(16, 8))
db_handle, = ax[0].plot(stats["cum_books_bill"].index, 
                         stats["cum_books_bill"], label="DB")
google_handle1, = ax[0].plot(stats["cum_books_min_bill"].index, 
                        stats["cum_books_min_bill"], label="GoogleMin")
google_handle2, = ax[0].plot(stats["cum_books_max_bill"].index, 
                        stats["cum_books_max_bill"], label="GoogleMax")
plt.legend(handles=[db_handle, google_handle1, google_handle2])
ax[0].set_title("Cumulative Bills")

db_handle, = ax[1].plot(stats["avg_books_bill"].index, 
                         stats["avg_books_bill"], label="DB")
google_handle1, = ax[1].plot(stats["avg_books_min_bill"].index, 
                        stats["avg_books_min_bill"], label="GoogleMin")
google_handle2, = ax[1].plot(stats["avg_books_max_bill"].index, 
                        stats["avg_books_max_bill"], label="GoogleMax")
plt.legend(handles=[db_handle, google_handle1, google_handle2])
ax[1].set_title("Average Bills")


plt.savefig("Bills")

fig, ax = plt.subplots(1, 2, figsize=(16, 8))
db_handle, = ax[0].plot(stats["med_books_duration"].index, 
                         stats["med_books_duration"], label="DB")
google_handle, = ax[0].plot(stats["med_books_duration_driving"].index, 
                        stats["med_books_duration_driving"], label="Google")
plt.legend(handles=[db_handle, google_handle])
ax[0].set_title("Median Booking Durations")

db_handle, = ax[1].plot(stats["avg_books_duration"].index, 
                         stats["avg_books_duration"], label="DB")
google_handle, = ax[1].plot(stats["avg_books_duration_driving"].index, 
                        stats["avg_books_duration_driving"], label="Google")
plt.legend(handles=[db_handle, google_handle])
ax[1].set_title("Average Booking Durations")
plt.savefig("Booking Durations")


fig, ax = plt.subplots(1, 2, figsize=(16, 8))
db_handle, = ax[0].plot(stats["med_books_distance"].index, 
                         stats["med_books_distance"], label="DB")
google_handle, = ax[0].plot(stats["med_books_distance_driving"].index, 
                        stats["med_books_distance_driving"], label="Google")
plt.legend(handles=[db_handle, google_handle])
ax[0].set_title("Median Booking Distances")

db_handle, = ax[1].plot(stats["avg_books_distance"].index, 
                         stats["avg_books_distance"], label="DB")
google_handle, = ax[1].plot(stats["avg_books_distance_driving"].index, 
                        stats["avg_books_distance_driving"], label="Google")
plt.legend(handles=[db_handle, google_handle])
ax[1].set_title("Average Booking Distances")
plt.savefig("Booking Distances")

#zones, origins, destinations, od = getODmatrix("torino", "car2go", 2017, 1, 8)
#
#od_norm = (od - od.mean())/od.std()
#x = od_norm.index.values
#y = od_norm.index.values
#fig = plt.figure(figsize=(8,8))
##plt.pcolormesh(x, y, od_norm.values, cmap='RdBu', vmin=-1, vmax=2)
##plt.pcolor(od_norm)
#plt.imshow(od, interpolation='nearest', cmap='YlOrRd')
#plt.title('pcolor')
## set the limits of the plot to the limits of the data
#plt.axis([x.min(), 100, y.min(), 100])
#plt.colorbar()

# demography_zones = gpd.read_file("../../dati_torino/zonestat_popolazione_residente_2015_geo.dbf")\
#         .to_crs({"init": "epsg:4326"})

# "zonestat_popolazione_residente_2015_geo.dbf"
