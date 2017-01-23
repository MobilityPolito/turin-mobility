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
    
def get_parks_day (city, provider, year, month, day):
    
    end = datetime.datetime(year, month, day, 23, 59, 59)
    start = end - datetime.timedelta(days = 1)
    
    parks_df = dbp.get_parks(provider, city, start, end)
    parks_df["durations"] = (parks_df["end"] - parks_df["start"])/np.timedelta64(1, 'm')
    
    parks_df["geometry"] = parks_df.apply\
        (lambda row: Point(row["lon"], row["lat"]), axis=1)
    parks_df = gpd.GeoDataFrame(parks_df, geometry="geometry")
    parks_df.crs = {"init": "epsg:4326"}

    return parks_df
    
parks_df = get_parks_day("torino", "car2go", 2016, 12, 10)

parks_points = parks_df["geometry"]    
zones = gpd.read_file("../../SHAPE/Zonizzazione.dbf")\
        .to_crs({"init": "epsg:4326"})
zones["nparks"] = 0.0

for point in parks_points.values:
    intersect = zones.contains(point)
#    print intersect[intersect == True]
    z = intersect[intersect == True].index.values[0]
    zones.ix[z, "nparks"] += 1

def heatmap(d, bins=(100,100), smoothing=1.3, cmap='jet'):

    def getx(pt):
        return pt.coords[0][0]
    def gety(pt):
        return pt.coords[0][1]

    x = list(d.geometry.apply(getx))
    y = list(d.geometry.apply(gety))
    heatmap, xedges, yedges = np.histogram2d(y, x, bins=bins)
    extent = [yedges[0], yedges[-1], xedges[-1], xedges[0]]

    logheatmap = np.log(heatmap)
    logheatmap[np.isneginf(logheatmap)] = 0
    logheatmap = ndimage.filters.gaussian_filter(logheatmap, smoothing, mode='nearest')
    
    plt.imshow(logheatmap, cmap=cmap, extent=extent)
    plt.colorbar()
    plt.gca().invert_yaxis()
    plt.savefig("car2go_logheatmap.png")    

    return ax

#fig, ax = plt.subplots(1, 1, figsize=(10,10))
#ax = zones.plot(color="white", ax=ax)
#heatmap(parks_df, bins=20, smoothing=1.2)
#plt.show()

    
#ztl = gpd.read_file("./DataSource/geoportale/dati_torino/ztl_geo.dbf")\
#            .to_crs({"init": "epsg:4326"})
#ztl["nparks"] = 0.0
#
#for point in parks_points.values:
#    intersect = ztl.contains(point)
#    ztl.ix[intersect[intersect == True].index.values[0], "nparks"] += 1
            
#fig, ax = plt.subplots(1, 1, figsize=(10,10))
#
#ax = zones.plot(color="white", ax=ax)
#ax.set_xlim([7.6, 7.8])
#ax.set_ylim([45.0,45.15])

#ax = ztl.plot(ax=ax)
#ax.set_xlim([7.66, 7.72])
#ax.set_ylim([45.05,45.10])

#plt.show()

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

#from pandas.tools.plotting import andrews_curves
#fig = plt.figure(figsize=(25,25))
#andrews_curves(df[["country"] + scores_cols].iloc[:200].dropna(), "country")
#plt.savefig("andrews_curves.png")
#
#from pandas.tools.plotting import radviz
#fig = plt.figure(figsize=(25,25))
#radviz(df[["country"] + scores_cols].iloc[:200].dropna(), "country")
#plt.savefig("radviz.png")