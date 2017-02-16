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

from Graphics import Graphics
g = Graphics()

from DataBaseProxy import DataBaseProxy
dbp = DataBaseProxy()

from EnjoyProvider import Enjoy
enjoy = Enjoy()

from Car2GoProvider import Car2Go
car2go = Car2Go()

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

start = datetime.datetime(2017, 1, 1, 0, 0, 0)
end = datetime.datetime(2017, 1, 8, 0, 0, 0)

enjoy_df = dbp.query_books_df_filtered("enjoy", "torino", start, end)
car2go_df = dbp.query_books_df_filtered("car2go", "torino", start, end)

enjoy_improved = dbp.filter_books_df_outliers(dbp.query_books_df_filtered_v3("enjoy", "torino", start, end))
car2go_improved = dbp.filter_books_df_outliers(dbp.query_books_df_filtered_v3("car2go", "torino", start, end))

### ******* COUNT
### ******* BILLS

plt.figure()
g.plot_aggregated_count_vs(enjoy_df, car2go_df, "distance", "ride", quantile=0.01)

col = "duration"

g.plot_samples_vs(enjoy_df, car2go_df, col, "ride")
g.plot_samples_vs(enjoy_df, car2go_df, col, "ride", quantile=0.01)

plt.figure()
g.hist(enjoy_df, col, "ride", "Enjoy", "red", quantile=0.01)
plt.figure()
g.hist(car2go_df, col, "ride", "Car2Go", "blue", quantile=0.01)

plt.figure()
g.plot_aggregated_mean_vs(enjoy_df, car2go_df, col, "all")
plt.figure()
g.plot_aggregated_mean_vs(enjoy_df, car2go_df, col, "all", quantile=0.01)

plt.figure()
g.plot_aggregated_sum_vs(enjoy_df, car2go_df, "min_bill", "all", quantile=0.01)
g.plot_aggregated_sum_vs(enjoy_df, car2go_df, "max_bill", "all", quantile=0.01)

### CDF WEEKS ###
g.cdf_weeks_duration(enjoy_df, car2go_df)
g.cdf_weeks_distance(enjoy_df, car2go_df)

### CDF BUSINESS VS WEEKEND ###
g.cdf_business_weekend(enjoy_df)
g.cdf_business_weekend(car2go_df)

### REAL DURATION VS GOOGLE ###
g.car_vs_google(enjoy_df)
g.car_vs_google(car2go_df)
g.car_vs_google_comparison(enjoy_df, car2go_df)

def heatmap(lats, lons, bins=(100,100), smoothing=1.3, cmap='jet'):

    heatmap, xedges, yedges = np.histogram2d(lats, lons, bins=bins)
    
    logheatmap = np.log(heatmap)
    logheatmap[np.isneginf(logheatmap)] = 0
    logheatmap = ndimage.filters.gaussian_filter(logheatmap, smoothing, mode='nearest')
    
    plt.imshow(heatmap, cmap=cmap, extent=[yedges[0], yedges[-1], xedges[-1], xedges[0]], 
               aspect='auto')
    plt.colorbar()
    plt.gca().invert_yaxis()
    plt.show()

    return

car2go_df["hour"] = car2go_df["start"].apply(lambda d: d.hour)
grouped = car2go_df.groupby("hour")
for hour in range(24):
    plt.title(str(hour) + ":00")
    plt.xlim((7.61, 7.73))
    heatmap(grouped.get_group(hour).start_lat.values, 
            grouped.get_group(hour).start_lon.values,
            bins=20)

