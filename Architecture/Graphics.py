import datetime

import numpy as np
import pandas as pd

from scipy import ndimage

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

from pandas.tools.plotting import scatter_matrix

from ParksAnalysis import car2go_parks
from ParksAnalysis import enjoy_parks

fig, ax = plt.subplots(1, 1)
ax = scatter_matrix(car2go_parks[
                                    [
                                     "lat", 
                                     "lon", 
                                     "duration", 
                                    ]
                                ].astype("float64"), 
                                figsize=(10, 10), diagonal='kde')

fig, ax = plt.subplots(1, 1)
ax = scatter_matrix(enjoy_parks[
                                    [
                                     "lat", 
                                     "lon", 
                                     "duration", 
                                    ]
                                ].astype("float64"), 
                                figsize=(10, 10), diagonal='kde')

from ParksAnalysis import car2go_parks_stats
from ParksAnalysis import enjoy_parks_stats

def heatmap(d, bins=(100,100), smoothing=1.3, cmap='jet'):

    x = d["lon"].astype(np.float).values
    y = d["lat"].astype(np.float).values
    heatmap, xedges, yedges = np.histogram2d(y, x, bins=bins)
    extent = [yedges[0], yedges[-1], xedges[-1], xedges[0]]

    logheatmap = np.log(heatmap)
    logheatmap[np.isneginf(logheatmap)] = 0
    logheatmap = ndimage.filters.gaussian_filter(logheatmap, smoothing, mode='nearest')
    
    plt.imshow(heatmap, cmap=cmap, extent=extent)
    plt.colorbar()
    plt.gca().invert_yaxis()
    plt.show()
#    plt.savefig("car2go_logheatmap.png")    

    return

heatmap(car2go_parks_hour.groupby("hour").get_group(0), bins=20, smoothing=10)
plt.show()
