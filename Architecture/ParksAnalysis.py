from math import radians, cos, sin, asin, sqrt

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
    
provider = "car2go"
end = datetime.datetime(2016, 12, 10, 0, 0, 0)
start = end - datetime.timedelta(days = 1)

parks_df = dbp.get_parks_df(provider, "torino", start, end)
parks_df["durations"] = (parks_df["end"] - parks_df["start"])/np.timedelta64(1, 'm')
parks_df["geometry"] = parks_df.apply\
    (lambda row: Point(row["lat"], row["lon"]), axis=1)
parks_df = gpd.GeoDataFrame(parks_df, geometry="geometry")
parks_df.crs = {"init": "epsg:4326"}
parks_points = parks_df["geometry"]

zones = gpd.read_file("../../SHAPE/Zonizzazione.dbf")\
        .to_crs({"init": "epsg:4326"})
zones["nparks"] = 0.0

for point in parks_points.values:
    intersect = zones.contains(point)
    z = intersect[intersect == True].index.values[0]
    zones.ix[z, "nparks"] += 1

#ztl = gpd.read_file("./DataSource/geoportale/dati_torino/ztl_geo.dbf")\
#            .to_crs({"init": "epsg:4326"})
#ztl["nparks"] = 0.0
#
#for point in parks_points.values:
#    intersect = ztl.contains(point)
#    ztl.ix[intersect[intersect == True].index.values[0], "nparks"] += 1
            
fig, ax = plt.subplots(1, 1, figsize=(10,10))

ax = zones.plot(color="white", ax=ax)
#ax.set_xlim([7.6, 7.8])
#ax.set_ylim([45.0,45.15])
ax = zones.plot(ax=ax)

#ax = ztl.plot(ax=ax)
#ax.set_xlim([7.66, 7.72])
#ax.set_ylim([45.05,45.10])
#ax = ztl.plot(ax=ax)

plt.show()

#fig, ax = plt.subplots(1,1,figsize=(10,10))
#ax = parks_df["durations"].hist(figsize=(10,10))
#plt.savefig(provider + "_parks_durations_hist.png")
#

#fig, ax = plt.subplots(1,1,figsize=(10,10))
#ax = scatter_matrix(parks_df[["lat","lon","durations"]].astype("float64"), 
#               figsize=(10, 10), diagonal='kde')
#plt.savefig(provider + "_parks_scatter_matrix.png")

#zones_geo = zones["geometry"]
#fig, ax = plt.subplots(1,1,figsize=(10,10))
#ax = zones_geo.plot(color="white", ax=ax)
#ax.set_xlim([7.6, 7.8])
#ax.set_ylim([45.0,45.15])
#ax = parks_df.plot(ax=ax)
#fig.savefig(provider + "_parks_distribution.png")

#import seaborn as sns
#
#Index= ['aaa', 'bbb', 'ccc', 'ddd', 'eee']
#Cols = ['A', 'B', 'C', 'D']
#df = DataFrame(abs(np.random.randn(5, 4)), index=Index, columns=Cols)
#
#sns.heatmap(df)


#from pandas.tools.plotting import andrews_curves
#fig = plt.figure(figsize=(25,25))
#andrews_curves(df[["country"] + scores_cols].iloc[:200].dropna(), "country")
#plt.savefig("andrews_curves.png")
#
#from pandas.tools.plotting import radviz
#fig = plt.figure(figsize=(25,25))
#radviz(df[["country"] + scores_cols].iloc[:200].dropna(), "country")
#plt.savefig("radviz.png")
