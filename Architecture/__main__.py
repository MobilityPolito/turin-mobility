#import json
import datetime
#
import numpy as np

from scipy import ndimage
#
#import pandas as pd
#
#import statsmodels.api as sm
#import statsmodels.formula.api as smf

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as md
matplotlib.style.use('ggplot')

#from pandas.tools.plotting import scatter_matrix

from Car2GoProvider import Car2Go
from EnjoyProvider import Enjoy

from Graphics import Graphics
from DataBaseProxy import DataBaseProxy
dbp = DataBaseProxy()
g = Graphics()
enjoy = Enjoy()
car2go = Car2Go()

"""
Fleet
"""

enjoy_fleetsize_series = enjoy.get_fleetsize_info().dropna()
car2go_fleetsize_series = car2go.get_fleetsize_info().dropna()

fig, axs = plt.subplots(1,1)
enjoy_fleetsize_series.plot(figsize=(13,6), marker='o', ax=axs, label="Enjoy")
car2go_fleetsize_series.plot(figsize=(13,6), marker='o', ax=axs, label="Car2Go")
plt.legend()
plt.title("Fleet size evolution")

plt.show()

"""
Sketch
"""

start = datetime.datetime(2017, 1, 1, 0, 0, 0)
end = datetime.datetime(2017, 1, 8, 0, 0, 0)

enjoy_books_df = dbp.query_books_df_filtered("enjoy", "torino", start, end)
car2go_books_df = dbp.query_books_df_filtered("car2go", "torino", start, end)
enjoy_improved = dbp.filter_books_df_outliers(enjoy_books_df)
car2go_improved = dbp.filter_books_df_outliers(car2go_books_df)

### DURATION FULL ##
g.duration_all(enjoy_books_df, car2go_books_df)

### DURATION WITHOUT OUTLIERS ###
g.duration(enjoy_improved)
g.duration(car2go_improved)

### HISTS ###
g.hist(enjoy_improved, cumulative=False)
g.hist(car2go_improved, cumulative=False)
g.hist(enjoy_improved, cumulative=True)
g.hist(car2go_improved, cumulative=True)

### AGGREGATED 30 MIIN ###

g.duration_aggregated(enjoy_improved, car2go_improved)
g.bookings_aggregated(enjoy_improved, car2go_improved)

### MEAN ###
g.mean_bookings_aggregated(enjoy_improved, car2go_improved)
g.mean_daily_duration(enjoy_improved, car2go_improved)


### BILL ###
g.daily_min_bill_aggregated(enjoy_improved, car2go_improved)
g.daily_max_bill_aggregated(enjoy_improved, car2go_improved)
g.daily_bills_aggregated(enjoy_improved, car2go_improved)


### CDF WEEKS ###
g.cdf_weeks_duration(enjoy_improved, car2go_improved)
g.cdf_weeks_distance(enjoy_improved, car2go_improved)

### CDF BUSINESS VS WEEKEND ###
g.cdf_business_weekend(enjoy_improved)
g.cdf_business_weekend(car2go_improved)

### BOOKS NUMBER MEAN BUSINESS VS WEEKEND ###
g.number_books_aggregated(enjoy_improved)
g.number_books_aggregated(car2go_improved)

### REAL DURATION VS GOOGLE ###
g.car_vs_google(enjoy_improved)
g.car_vs_google(car2go_improved)
g.car_vs_google_comparison(enjoy_improved, car2go_improved)

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
#["hour"] = car2go_with_ride_filtered["start"].apply(lambda d: d.hour)
#grouped = car2go_with_ride_filtered.groupby("hour")
#for hour in range(24):
#    plt.title(str(hour) + ":00")
#    plt.xlim((7.61, 7.73))
#    heatmap(grouped.get_group(hour).start_lat.values, 
#            grouped.get_group(hour).start_lon.values,
#            bins=100)
    
#import imageio
#images = []
#for filename in filenames:
#    images.append(imageio.imread(filename))
#imageio.mimsave('/path/to/movie.gif', images)
