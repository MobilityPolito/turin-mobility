#import json
import datetime

from shapely.geometry import Point
#from shapely.geometry import LineString
    
import numpy as np

from scipy import ndimage

import pandas as pd
import geopandas as gpd

import statsmodels.api as sm
import statsmodels.formula.api as smf

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

from pandas.tools.plotting import scatter_matrix

from Graphics import Graphics
g = Graphics()

from DataBaseProxy import DataBaseProxy
dbp = DataBaseProxy()

from EnjoyProvider import Enjoy
enjoy = Enjoy()

from Car2GoProvider import Car2Go
car2go = Car2Go()

from area_enjoy import create_zones_enjoy
from area_car2go import create_zones_car2go

"""
Load data structure
"""

start = datetime.datetime(2016, 12, 12, 0, 0, 0)
end = datetime.datetime(2016, 12, 13, 23, 59, 59)

enjoy_df = dbp.query_books_df_filtered_v3("enjoy", "torino", start, end)
car2go_df = dbp.query_books_df_filtered_v3("car2go", "torino", start, end)
##
##zones = gpd.read_file("../../SHAPE/Zonizzazione.dbf").to_crs({"init": "epsg:4326"})\
##                     .sort_values("Denom_GTT").reset_index().drop("index", axis=1)
##
##centroids = gpd.read_file("../../SHAPE/Centroidi.dbf").to_crs({"init": "epsg:4326"})\
##                     .sort_values("Denom_GTT").reset_index().drop("index", axis=1)
##
##demography = gpd.read_file("../../dati_torino/zonestat_popolazione_residente_2015_geo.dbf").to_crs({"init": "epsg:4326"})
##
##enjoy_operational_zones = create_zones_enjoy()
##car2go_operational_zones = create_zones_car2go('zones')
##car2go_airport = create_zones_car2go('airport')
##car2go_ikea = create_zones_car2go('ikea')
##
##frames = [enjoy_operational_zones, 
##          car2go_operational_zones, 
##          car2go_airport, 
##          car2go_ikea]
##
##operational_zones = gpd.GeoDataFrame(pd.concat(frames))
#
##"""
##Fleet
##"""
##
##enjoy_fleetsize_series = enjoy.get_fleetsize_info().dropna()
##car2go_fleetsize_series = car2go.get_fleetsize_info().dropna()
##
##fig, axs = plt.subplots(1,1)
##enjoy_fleetsize_series.plot(figsize=(13,6), marker='o', ax=axs, label="Enjoy")
##car2go_fleetsize_series.plot(figsize=(13,6), marker='o', ax=axs, label="Car2Go")
##plt.legend()
##plt.title("Fleet size evolution")
##
##plt.show()
##
##"""
##Sketch
##"""
### * SAMPLES *
##
##filter_name = "ride"
##col = "distance"
###col = "tot_duration_in_traffic"
###col = "riding_time"
###col = "duration"
##
##plt.figure()
##g.plot_samples(car2go_df, col, filter_name, "car2go")
##plt.figure()
##g.plot_samples(car2go_df, col, filter_name, "car2go", quantile=0.01)
##plt.figure()
##g.plot_samples(car2go_df, col, filter_name, "car2go", quantile=0.05)
##
##plt.figure()
##g.plot_samples(enjoy_df, col, filter_name, "enjoy")
##plt.figure()
##g.plot_samples(enjoy_df, col, filter_name, "enjoy", quantile=0.01)
##plt.figure()
##g.plot_samples(enjoy_df, col, filter_name, "enjoy", quantile=0.05)
##
##
##g.plot_samples_vs(enjoy_df, car2go_df, col, filter_name)
##g.plot_samples_vs(enjoy_df, car2go_df, col, filter_name, quantile=0.01)
##g.plot_samples_vs(enjoy_df, car2go_df, col, filter_name, quantile=0.05)
##
### HISTOGRAMS 
##col = "duration"
##g.hist(enjoy_df, col, filter_name, "Enjoy", "red")
##g.hist(enjoy_df, col, filter_name, "Enjoy", "red", quantile=0.05)
##g.hist(enjoy_df, col, filter_name, "Enjoy", "red", quantile=0.05, cumulative= True)
##
##g.hist(car2go_df, col, filter_name, "Car2Go", "blue")
##g.hist(car2go_df, col, filter_name, "Car2Go", "blue", quantile=0.05)
##g.hist(car2go_df, col, filter_name, "Car2Go", "blue", quantile=0.05, cumulative= True)
##
###### CDF WEEKS ###
##g.cdf_weeks_duration(enjoy_df, car2go_df)
##g.cdf_weeks_distance(enjoy_df, car2go_df)
###
###### CDF BUSINESS VS WEEKEND ###
##g.cdf_business_weekend(enjoy_df)
##g.cdf_business_weekend(car2go_df)
#
### AGGREGATED PLOTS
##col = "distance"
##g.plot_aggregated_count_vs(enjoy_df, car2go_df, col, filter_name, quantile=0.01)
##g.plot_aggregated_mean_vs(enjoy_df, car2go_df, col, "all")
##g.plot_aggregated_mean_vs(enjoy_df, car2go_df, col, "all", quantile=0.01)
##
### DAILY
##
##g.plot_daily_count_vs(enjoy_df, car2go_df, col, filter_name, quantile=0.01)
##g.plot_daily_mean_vs(enjoy_df, car2go_df, col, filter_name, quantile=0.01)
#
#
#"""
# * GOOGLE RESULTS *
#"""
#
##g.car_vs_google(enjoy_df)
##g.car_vs_google(car2go_df)
##g.car_vs_google_comparison(enjoy_df, car2go_df)
#
##g.car_vs_transit(enjoy_df)
##g.car_vs_transit(car2go_df)
#
##g.car_vs_transit_bar(enjoy_df)
##g.car_vs_transit_bar(car2go_df)
###
###
##g.car_vs_transit_resampled(enjoy_df)
##g.car_vs_transit_resampled(car2go_df)
##
##g.faster_PT_hours(enjoy_df)
###  night problem
##g.faster_PT_hours(car2go_df)
##
##g.faster_car_hours(enjoy_df)
##g.faster_car_hours(car2go_df)
###
##g.faster_car_PTtime_hours(enjoy_df)
##g.faster_car_PTtime_hours(car2go_df)
##
##
##g.car_pt(enjoy_df)
##g.car_pt(car2go_df)
##
##g.car_pt_vs(enjoy_df,car2go_df)
###
##
###
##
##pos_piazzaVittorio = [45.0650653, 7.6936148]
##pos_PortaNuova = [45.0620829, 7.6762908]
##g.isocrono(enjoy_df, pos_piazzaVittorio)
##g.isocost(enjoy_df, pos_piazzaVittorio)
#
#"""
#Bills
#"""
#
##g.plot_aggregated_sum_vs(enjoy_df, car2go_df, "min_bill", "ride", quantile=0.01)
##g.plot_aggregated_sum_vs(enjoy_df, car2go_df, "max_bill", "ride", quantile=0.01)
##
##g.plot_daily_sum_vs(enjoy_df, car2go_df, "min_bill", "ride", quantile=0.01)
##g.plot_daily_sum_vs(enjoy_df, car2go_df, "max_bill", "ride", quantile=0.01)
#
#"""
#Isocronous / Isocost
#"""
#
#
#"""
#Heatmap
#"""
#
##g.heatmaps_per_hour(car2go_df)
##g.heatmaps_per_hour(enjoy_df)
#
#"""
#OD matrix
#"""
#
#def getODmatrix (books_df, zones):
#    
#    origins = books_df[["start_lat","start_lon"]]
#    origins.loc[:,"geometry"] = origins.apply\
#        (lambda row: Point(row.loc["start_lon"], row.loc["start_lat"]), 
#         axis=1)    
#
#    destinations = books_df[["end_lat","end_lon"]]
#    destinations.loc[:,"geometry"] = destinations.apply\
#        (lambda row: Point(row.loc["end_lon"], row.loc["end_lat"]), 
#         axis=1)    
#
#    OD = pd.DataFrame(0.0, index = zones.index, columns = zones.index)
#
#    for i in range(len(books_df)):
#        try:
#            if i%10000 == 0:
#                print i
#            o = origins.ix[i, "geometry"]
#            d = destinations.ix[i, "geometry"]
#            intersect_o = zones.contains(o)
#            intersect_d = zones.contains(d)
#            zo = intersect_o[intersect_o == True].index.values[0]
#            zd = intersect_d[intersect_d == True].index.values[0]
#            OD.loc[zo, zd] += 1
#        except:
#            "Book" + str(i) + "has points not contained in any zone!"
#
#    return origins, destinations, OD
#    
#def filter_quantile(df, col, filter_col, quantile):
#    
#    s = df.loc[df[filter_col] == True, col].dropna()
#    s = s[(s >= s.quantile(q=quantile)) & (s <= s.quantile(q=1.0-quantile))]
#    return df.loc[s.index]
#
#origins, destinations, car2go_od = getODmatrix\
#    (filter_quantile(car2go_df, "start_lat", "ride", 0.001), zones)
#origins, destinations, enjoy_od = getODmatrix\
#    (filter_quantile(enjoy_df, "start_lat", "ride", 0.001), zones)
#
#def drop_od (od):
#    dropped_od = od
#    for zone in od:
#        zone_as_origin = od.iloc[zone]
#        zone_as_dest = od.iloc[:,zone]
#        if not zone_as_origin.sum() and not zone_as_dest.sum():
#            dropped_od = od.drop(zone, axis=0)
#            dropped_od = od.drop(zone, axis=1)
#    return dropped_od
#
#def standardize (x):
#    return (x-x.mean())/x.std()
#
#def force_positive (x):
#    return x+abs(x.min())
#
#dropped_car2go_od = drop_od(car2go_od)
#dropped_enjoy_od = drop_od(enjoy_od)
#
#zones["car2go_d_tot"] = dropped_car2go_od.sum(axis=1)
#zones["car2go_o_tot"] = dropped_car2go_od.sum(axis=0)
#zones["car2go_tot"] = (zones["car2go_o_tot"]-zones["car2go_d_tot"])*(zones["car2go_o_tot"]+zones["car2go_d_tot"])
#
#zones["enjoy_d_tot"] = dropped_enjoy_od.sum(axis=1)
#zones["enjoy_o_tot"] = dropped_enjoy_od.sum(axis=0)
#zones["enjoy_tot"] = (zones["enjoy_o_tot"]-zones["enjoy_d_tot"])*(zones["enjoy_o_tot"]+zones["enjoy_d_tot"])
#
#fig, axs = plt.subplots(2, 2, figsize=(18,18))
#zones.plot(column='car2go_o_tot', cmap='Blues', ax=axs[0][0])
#zones.plot(column='car2go_d_tot', cmap='Blues', ax=axs[0][1])
#zones.where((zones.car2go_d_tot>0) & (zones.car2go_o_tot>0)).dropna()\
#           .plot(column='car2go_o_tot', cmap='Blues', ax=axs[1][0])
#zones.where((zones.car2go_d_tot>0) & (zones.car2go_o_tot>0)).dropna()\
#           .plot(column='car2go_d_tot', cmap='Blues', ax=axs[1][1])
#
#fig, axs = plt.subplots(2, 2, figsize=(18,18))
#zones.plot(column='enjoy_o_tot', cmap='OrRd', ax=axs[0][0])
#zones.plot(column='enjoy_d_tot', cmap='OrRd', ax=axs[0][1])
#zones.where((zones.enjoy_d_tot>0) & (zones.enjoy_o_tot>0)).dropna()\
#           .plot(column='enjoy_o_tot', cmap='OrRd', ax=axs[1][0])
#zones.where((zones.enjoy_d_tot>0) & (zones.enjoy_o_tot>0)).dropna()\
#           .plot(column='enjoy_d_tot', cmap='OrRd', ax=axs[1][1])
