#import json
import datetime

from shapely.geometry import Point
#from shapely.geometry import LineString
    
import numpy as np

from scipy import ndimage

import pandas as pd
import geopandas as gpd

#import statsmodels.api as sm
#import statsmodels.formula.api as smf

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

#from pandas.tools.plotting import scatter_matrix

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

start = datetime.datetime(2016, 12, 10, 0, 0, 0)
end = datetime.datetime(2016, 12, 31, 23, 59, 59)

enjoy_df = dbp.query_books_df_filtered_v3("enjoy", "torino", start, end)
car2go_df = dbp.query_books_df_filtered_v3("car2go", "torino", start, end)

zones = gpd.read_file("../../SHAPE/Zonizzazione.dbf").to_crs({"init": "epsg:4326"})
#
#demography = gpd.read_file("../../dati_torino/zonestat_popolazione_residente_2015_geo.dbf")\
#    .to_crs({"init": "epsg:4326"})
#
#enjoy_operational_zones = create_zones_enjoy()
#car2go_operational_zones = create_zones_car2go('zones')
#car2go_airport = create_zones_car2go('airport')
#car2go_ikea = create_zones_car2go('ikea')
#
#frames = [enjoy_operational_zones, 
#          car2go_operational_zones, 
#          car2go_airport, 
#          car2go_ikea]
#
#operational_zones = gpd.GeoDataFrame(pd.concat(frames))

"""
Fleet
"""

#enjoy_fleetsize_series = enjoy.get_fleetsize_info().dropna()
#car2go_fleetsize_series = car2go.get_fleetsize_info().dropna()
#
#fig, axs = plt.subplots(1,1)
#enjoy_fleetsize_series.plot(figsize=(13,6), marker='o', ax=axs, label="Enjoy")
#car2go_fleetsize_series.plot(figsize=(13,6), marker='o', ax=axs, label="Car2Go")
#plt.legend()
#plt.title("Fleet size evolution")
#
#plt.show()

"""
Sketch
"""

#plt.figure()
#df[df.tot_duration_google_transit < df.duration].set_index("start").duration.plot(figsize=(w,h), marker='o', label="enjoy")
#plt.legend()

#plt.figure()
#g.plot_aggregated_count_vs(enjoy_df, car2go_df, "distance", "ride", quantile=0.01)
#
#col = "duration"
#
#g.plot_samples_vs(enjoy_df, car2go_df, col, "ride")
#g.plot_samples_vs(enjoy_df, car2go_df, col, "ride", quantile=0.01)
#g.plot_samples_vs(enjoy_df, car2go_df, col, "ride", quantile=0.05)
#
#plt.figure()
#g.hist(enjoy_df, col, "ride", "Enjoy", "red", quantile=0.01)
#plt.figure()
#g.hist(car2go_df, col, "ride", "Car2Go", "blue", quantile=0.01)
#
#plt.figure()
#g.plot_aggregated_mean_vs(enjoy_df, car2go_df, col, "all")
#plt.figure()
#g.plot_aggregated_mean_vs(enjoy_df, car2go_df, col, "all", quantile=0.01)
#
#plt.figure()
#g.plot_aggregated_sum_vs(enjoy_df, car2go_df, "min_bill", "all", quantile=0.01)
#g.plot_aggregated_sum_vs(enjoy_df, car2go_df, "max_bill", "all", quantile=0.01)
#
#### CDF WEEKS ###
#g.cdf_weeks_duration(enjoy_df, car2go_df)
#g.cdf_weeks_distance(enjoy_df, car2go_df)
#
#### CDF BUSINESS VS WEEKEND ###
#g.cdf_business_weekend(enjoy_df)
#g.cdf_business_weekend(car2go_df)
#
#### REAL DURATION VS GOOGLE ###
#g.car_vs_google(enjoy_df)
#g.car_vs_google(car2go_df)
#g.car_vs_google_comparison(enjoy_df, car2go_df)

"""
 ****** GOOGLE RESULTS ******
"""

#g.plot_samples_vs(enjoy_df, car2go_df, "riding_time", "ride")
#
#g.car_vs_transit(enjoy_df)
#
#g.car_vs_transit(car2go_df)
#
#g.car_vs_transit_bar(enjoy_df)
#g.car_vs_transit_bar(car2go_df)
#
#
#g.car_vs_transit_resampled(enjoy_df)
#g.car_vs_transit_resampled(car2go_df)
#
#g.faster_PT_hours(enjoy_df)
##  night problem
#g.faster_PT_hours(car2go_df)
#g.faster_car_hours(enjoy_df)
#g.faster_car_hours(car2go_df)
#
#g.faster_car_PTtime_hours(enjoy_df)
#g.faster_car_PTtime_hours(car2go_df)
#
#g.car_vs_pt(enjoy_df)
#g.car_vs_pt(car2go_df)
#
#g.cars_vs_pt(enjoy_df,car2go_df)
#

"""
Heatmap origins/destinations
"""

#def heatmap(lats, lons, bins=(100,100), smoothing=1.3, cmap='jet'):
#
#    heatmap, xedges, yedges = np.histogram2d(lats, lons, bins=bins)
#    
#    logheatmap = np.log(heatmap)
#    logheatmap[np.isneginf(logheatmap)] = 0
#    logheatmap = ndimage.filters.gaussian_filter(logheatmap, smoothing, mode='nearest')
#    
#    plt.imshow(heatmap, cmap=cmap, extent=[yedges[0], yedges[-1], xedges[-1], xedges[0]], 
#               aspect='auto')
#    plt.colorbar()
#    plt.gca().invert_yaxis()
#    plt.show()
#
#    return
#
#car2go_df["hour"] = car2go_df["start"].apply(lambda d: d.hour)
#grouped = car2go_df.groupby("hour")
#for hour in range(24):
#    plt.title(str(hour) + ":00")
#    plt.xlim((7.61, 7.73))
#    heatmap(grouped.get_group(hour).start_lat.values, 
#            grouped.get_group(hour).start_lon.values,
#            bins=20)
#
#pos_piazzaVittorio = [45.0650653, 7.6936148]
#pos_PortaNuova = [45.0620829, 7.6762908]
#g.isocrono(enjoy_df, pos_piazzaVittorio)
#g.isocost(enjoy_df, pos_piazzaVittorio)
#

"""
OD matrix
"""

def getODmatrix (books_df, zones):
    
    origins = books_df[["start_lat","start_lon"]]
    origins.loc[:,"geometry"] = origins.apply\
        (lambda row: Point(row.loc["start_lon"], row.loc["start_lat"]), 
         axis=1)    

    destinations = books_df[["end_lat","end_lon"]]
    destinations.loc[:,"geometry"] = destinations.apply\
        (lambda row: Point(row.loc["end_lon"], row.loc["end_lat"]), 
         axis=1)    

    OD = pd.DataFrame(0.0, index = zones.index, columns = zones.index)

    for i in range(len(books_df)):
        try:
            print i
            o = origins.ix[i, "geometry"]
            d = destinations.ix[i, "geometry"]
            intersect_o = zones.contains(o)
            intersect_d = zones.contains(d)
            zo = intersect_o[intersect_o == True].index.values[0]
            zd = intersect_d[intersect_d == True].index.values[0]
            OD.loc[zo, zd] += 1
        except:
            "Book" + str(i) + "has points not contained in any zone!"

    return origins, destinations, OD
    
def filter_quantile(df, col, filter_col, quantile):
    
    s = df.loc[df[filter_col] == True, col].dropna()
    s = s[(s >= s.quantile(q=quantile)) & (s <= s.quantile(q=1.0-quantile))]
    return df.loc[s.index]


origins, destinations, od = getODmatrix\
    (filter_quantile(car2go_df, "start_lat", "ride", 0.001), zones)

dropped_od = od
for zone in od:
    zone_as_origin = od.iloc[zone]
    zone_as_dest = od.iloc[:,zone]
    if not zone_as_origin.sum() and not zone_as_dest.sum():
        dropped_od = dropped_od.drop(zone, axis=0)
        dropped_od = dropped_od.drop(zone, axis=1)

edges = pd.DataFrame(columns = ["o","d","w"])
i = 0
for o in dropped_od:
    for d in dropped_od:
        edges.loc[i, "o"] = o
        edges.loc[i, "d"] = d
        edges.loc[i, "w"] = dropped_od.loc[o,d]
        i += 1

edges = edges.dropna()
edges = edges.sort_values(by="w").head(100)

import networkx as nx
G = nx.DiGraph()
G.add_nodes_from(dropped_od.index.values)
G.add_weighted_edges_from(edges.values)
nx.draw_circular(G)

samples = 100
x = edges["o"].iloc[:samples].values
y = edges["d"].iloc[:samples].values
s = edges["w"].iloc[:samples].astype(int).values
plt.scatter(x, y, s=s)

##dropped_od = (dropped_od - dropped_od.mean())/dropped_od.std()

#dropped_od.plot(legend=False)

#plt.figure()
#dropped_od.max(axis=0).plot(marker='o', label="Enjoy", color="red")
#plt.figure()
#dropped_od.max(axis=1).plot(marker='o', label="Enjoy", color="red")

x = dropped_od.index.values
y = dropped_od.index.values
plt.figure()
plt.imshow(dropped_od, interpolation='nearest', cmap='YlOrRd')
plt.title('pcolor')
plt.axis([x.min(), 70, y.min(), 70])
plt.colorbar()