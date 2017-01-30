import datetime

import numpy as np
import pandas as pd
from scipy import ndimage

import statsmodels.api as sm
import statsmodels.formula.api as smf         

import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import LineString

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

from pandas.tools.plotting import scatter_matrix

from DataBaseProxy import DataBaseProxy
dbp = DataBaseProxy()
    
#from BooksAnalysis import get_books_day, get_books_days
#from ParksAnalysis import get_parks_day

def day_analysis (city, provider, year, month, day, fleet_size):

    books_df = get_books_day(city, provider, year, month, day)\
        .set_index("start").sort_index()

    day_stats = pd.DataFrame()
    
    for hour in range(0, 24, 1):
        sup_datetime = datetime.datetime(year, month, day, hour, 59, 59)
        inf_datetime = datetime.datetime(year, month, day, hour)

        day_stats.loc[sup_datetime, "n_books"] = \
            float(len(books_df[inf_datetime:sup_datetime]))
        day_stats.loc[sup_datetime, "n_books_norm"] = \
            float(len(books_df[inf_datetime:sup_datetime])) / fleet_size

        day_stats.loc[sup_datetime, "avg_books_duration"] = \
            books_df[inf_datetime:sup_datetime]["durations"].mean()
        day_stats.loc[sup_datetime, "med_books_duration"] = \
            books_df[inf_datetime:sup_datetime]["durations"].median()

        day_stats.loc[sup_datetime, "avg_books_distance"] = \
            books_df[inf_datetime:sup_datetime]["distances"].mean()
        day_stats.loc[sup_datetime, "med_books_distance"] = \
            books_df[inf_datetime:sup_datetime]["distances"].median()
        
        day_stats.loc[sup_datetime, "cum_books_bill"] = \
            books_df[inf_datetime:sup_datetime]["bill"].sum()
        
    return books_df, day_stats

def getODmatrix (city, provider, zones, start, end):
    
#    end = datetime.datetime(year, month, day, 23, 59, 59)

#    books_df = get_books_days(city, provider, end, depth)\
#        .set_index("start").sort_index()
        
    books_df = dbp.query_books_df_filtered_v2(provider, city, start, end, 'full')\
        .set_index('start').sort_index()

    books_df = books_df[books_df.duration < 120]
    books_df = books_df[books_df.distance > 0.1]
    
    origins = books_df[["start_lat","start_lon"]]
    origins["geometry"] = origins.apply\
        (lambda row: Point(row.loc["start_lon"], row.loc["start_lat"]), 
         axis=1)    

    destinations = books_df[["end_lat","end_lon"]]
    destinations["geometry"] = destinations.apply\
        (lambda row: Point(row.loc["end_lon"], row.loc["end_lat"]), 
         axis=1)    

    OD = pd.DataFrame(0.0, index = zones.index, columns = zones.index)

    for i in range(len(books_df)):
        o = origins.ix[i, "geometry"]
        d = destinations.ix[i, "geometry"]
        intersect_o = zones.contains(o)
        intersect_d = zones.contains(d)
        try:
            zo = intersect_o[intersect_o == True].index.values[0]
            zd = intersect_d[intersect_d == True].index.values[0]
            OD.loc[zo, zd] += 1
        except:
            "Book" + str(i) + "has points not contained in any zone!"
            
#    OD["sum"] = OD.sum(axis=1)
#    OD.loc["sum"] = OD.sum()
#    OD.loc["sum","sum"]

    return books_df, origins, destinations, OD
    
## 2
#gdf1 = gpd.read_file("../../dati_torino/zonestat_popolazione_residente_2015_geo.dbf").to_crs({"init": "epsg:4326"})
#origins, destinations, od = getODmatrix("torino", "car2go", gdf1, 2017, 1, 8, 7)
#
#df = pd.DataFrame(index = gdf1.index)
#df["n_trips_origins"] = od.sum(axis=1)
#df[["n_males", "n_females", "tot"]] = gdf1[["NMASCHI", "NFEMMINE", "TOTALE"]]
#df["area"] = gdf1.area * 1000
#df["lons"] = gdf1.centroid.apply(lambda x: x.coords[0][0])
#df["lats"] = gdf1.centroid.apply(lambda x: x.coords[0][1])
#df = (df - df.mean())/df.std()
#
#mod = smf.ols(formula='n_trips_origins ~ tot + area + lons + lats', data=df)
#res = mod.fit()
#print res.summary()
#
#fig, ax = plt.subplots()
#fig = sm.graphics.plot_fit(res, 1, ax=ax)
#
## 2
#gdf2 = gpd.read_file("../../dati_torino/microzone_censuarie_geo.dbf").to_crs({"init": "epsg:4326"})
#origins, destinations, od = getODmatrix("torino", "car2go", gdf2, 2017, 1, 8, 7)
#
#df = pd.DataFrame(index = gdf2.index)
#df["n_trips_origins"] = od.sum(axis=1)
#df[["a", "b", "c", "d", "e", "f"]] = gdf2[["N_MAX", "N_MED", "N_MIN", "U_MAX", "U_MED", "U_MIN"]]
#df["area"] = gdf2.area * 1000
#df["lons"] = gdf2.centroid.apply(lambda x: x.coords[0][0])
#df["lats"] = gdf2.centroid.apply(lambda x: x.coords[0][1])
#df = (df - df.mean())/df.std()
#
#mod = smf.ols(formula='n_trips_origins ~ a + b + c + d + e + f + area + lons + lats', data=df)
#res = mod.fit()
#print res.summary()
#
#fig, ax = plt.subplots()
#fig = sm.graphics.plot_fit(res, 1, ax=ax)
#
#od_norm = (od - od.mean())/od.std()
#x = od_norm.index.values
#y = od_norm.index.values
#fig = plt.figure(figsize=(8,8))
##plt.pcolormesh(x, y, od_norm.values, cmap='RdBu', vmin=-1, vmax=2)
##plt.pcolor(od_norm)
#plt.imshow(od_norm, interpolation='nearest', cmap='YlOrRd')
#plt.title('pcolor')
## set the limits of the plot to the limits of the data
#plt.axis([x.min(), 70, y.min(), 70])
#plt.colorbar()
#
## 2
#gdf3 = gpd.read_file("../../SHAPE/Zonizzazione.dbf").to_crs({"init": "epsg:4326"})
#origins, destinations, od = getODmatrix("torino", "car2go", gdf1, 2017, 1, 8, 7)
