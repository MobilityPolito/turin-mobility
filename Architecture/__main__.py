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
matplotlib.style.use('ggplot')

#from pandas.tools.plotting import scatter_matrix

from Car2GoProvider import Car2Go
from EnjoyProvider import Enjoy

from DataBaseProxy import DataBaseProxy
dbp = DataBaseProxy()

enjoy = Enjoy()
car2go = Car2Go()

"""
Fleet
"""

enjoy_fleetsize_series = enjoy.get_fleetsize_info()
car2go_fleetsize_series = car2go.get_fleetsize_info()

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
end = datetime.datetime(2017, 1, 15, 0, 0, 0)

enjoy_books_df = dbp.query_books_df_filtered("enjoy", "torino", start, end)
car2go_books_df = dbp.query_books_df_filtered("car2go", "torino", start, end)

plt.figure()
plt.title("Duration")
enjoy_books_df.duration.plot(figsize=(13,6), marker='o', label="Enjoy")
car2go_books_df.duration.plot(figsize=(13,6), marker='o', label="Car2Go")

plt.figure()
plt.title("Duration without outliers")
enjoy_reservations, enjoy_with_ride, enjoy_with_ride_filtered = dbp.filter_books_df_outliers(enjoy_books_df)
enjoy_with_ride_filtered.duration.plot(figsize=(13,6), marker='o', label="Enjoy", color="red")
enjoy_with_ride_filtered.duration.plot(figsize=(13,6), marker='o', label="Enjoy", color="red")

plt.figure()
plt.title("Duration without outliers")
car2go_reservations, car2go_with_ride, car2go_with_ride_filtered = dbp.filter_books_df_outliers(car2go_books_df)
car2go_with_ride_filtered.duration.plot(figsize=(13,6), marker='o', label="Car2Go", color="blue")
car2go_with_ride_filtered.duration.plot(figsize=(13,6), marker='o', label="Car2Go", color="blue")

plt.figure()
enjoy_with_ride_filtered.duration.hist(bins=100, figsize=(13,6))
plt.figure()
car2go_with_ride_filtered.duration.hist(bins=100, figsize=(13,6))
plt.figure()
enjoy_with_ride_filtered.duration.hist(bins=100, figsize=(13,6), cumulative=True)
plt.figure()
car2go_with_ride_filtered.duration.hist(bins=100, figsize=(13,6), cumulative=True)

plt.figure()
plt.title("Duration aggregated by 30 min")
enjoy_with_ride_filtered.set_index("start").resample("30Min").duration.mean()\
    .plot(figsize=(13,6), marker='o', label="Enjoy")
car2go_with_ride_filtered.set_index("start").resample("30Min").duration.mean()\
    .plot(figsize=(13,6), marker='o', label="Car2Go")
plt.legend()

plt.figure()
plt.title("Number of bookings aggregated by 30 min")
enjoy_with_ride_filtered.set_index("start").resample("30Min")._id.count()\
    .plot(figsize=(13,6), marker='o', label="Enjoy")
car2go_with_ride_filtered.set_index("start").resample("30Min")._id.count()\
    .plot(figsize=(13,6), marker='o', label="Car2Go")
plt.legend()

plt.figure()
plt.title("Mean daily Number of bookings aggregated by hour")
enjoy_nbooks = enjoy_with_ride_filtered.set_index("start").resample("30Min")._id.count()
enjoy_nbooks.groupby(enjoy_nbooks.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Enjoy N books", color="red")
car2go_nbooks = car2go_with_ride_filtered.set_index("start").resample("30Min")._id.count()
car2go_nbooks.groupby(car2go_nbooks.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Car2Go N books", color="blue")
plt.legend()

plt.figure()
plt.title("Mean daily duration aggregated by hour")
enjoy_duration = enjoy_with_ride_filtered.set_index("start").resample("30Min").duration.mean()
enjoy_duration.groupby(enjoy_duration.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Enjoy duration", color="red")
car2go_duration = car2go_with_ride_filtered.set_index("start").resample("30Min").duration.mean()
car2go_duration.groupby(car2go_duration.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Car2Go duration", color="blue")
plt.legend()

plt.figure()
plt.title("Daily min bill aggregated by 30 min")
enjoy_with_ride_filtered.set_index("start").resample("30Min").min_bill.sum()\
    .plot(figsize=(13,6), marker='o', label="Enjoy")
car2go_with_ride_filtered.set_index("start").resample("30Min").min_bill.sum()\
    .plot(figsize=(13,6), marker='o', label="Car2Go")
plt.legend()

plt.figure()
plt.title("Daily max bill aggregated by 30 min")
enjoy_with_ride_filtered.set_index("start").resample("30Min").max_bill.sum()\
    .plot(figsize=(13,6), marker='o', label="Enjoy")
car2go_with_ride_filtered.set_index("start").resample("30Min").max_bill.sum()\
    .plot(figsize=(13,6), marker='o', label="Car2Go")
plt.legend()

plt.figure()
plt.title("Mean daily bills aggregated by hour")    
enjoy_min = enjoy_with_ride_filtered.set_index("start").resample("30Min").min_bill.sum()
enjoy_min.groupby(enjoy_min.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Enjoy min", color="red")
enjoy_max = enjoy_with_ride_filtered.set_index("start").resample("30Min").max_bill.sum()
enjoy_max.groupby(enjoy_min.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Enjoy max", color="red")
car2go_min = car2go_with_ride_filtered.set_index("start").resample("30Min").min_bill.sum()
car2go_min.groupby(enjoy_min.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Car2Go min", color="blue")
car2go_max = car2go_with_ride_filtered.set_index("start").resample("30Min").max_bill.sum()
car2go_max.groupby(enjoy_min.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Car2Go max", color="blue")
plt.legend()

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
#enjoy_start_lats = enjoy_books_df.set_index("start").start_lat
#enjoy_start_lons = enjoy_books_df.set_index("start").start_lon
#
#enjoy_books_df["hour"] = enjoy_books_df["start"].apply(lambda d: d.hour)
#grouped = enjoy_books_df.groupby("hour")
#for hour in range(24):
#    plt.title(str(hour))
#    heatmap(grouped.get_group(hour).start_lat.values, 
#            grouped.get_group(hour).start_lon.values)
#import imageio
#images = []
#for filename in filenames:
#    images.append(imageio.imread(filename))
#imageio.mimsave('/path/to/movie.gif', images)