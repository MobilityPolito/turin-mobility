import datetime

import numpy as np
import pandas as pd

from scipy import ndimage

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

from pandas.tools.plotting import scatter_matrix

# from ParksAnalysis import car2go_parks
# from ParksAnalysis import enjoy_parks

# fig, ax = plt.subplots(1, 1)
# ax = scatter_matrix(car2go_parks[
#                                     [
#                                      "lat", 
#                                      "lon", 
#                                      "duration", 
#                                     ]
#                                 ].astype("float64"), 
#                                 figsize=(10, 10), diagonal='kde')

# fig, ax = plt.subplots(1, 1)
# ax = scatter_matrix(enjoy_parks[
#                                     [
#                                      "lat", 
#                                      "lon", 
#                                      "duration", 
#                                     ]
#                                 ].astype("float64"), 
#                                 figsize=(10, 10), diagonal='kde')

# from ParksAnalysis import car2go_parks_stats
# from ParksAnalysis import enjoy_parks_stats

# def heatmap(d, bins=(100,100), smoothing=1.3, cmap='jet'):

#     x = d["lon"].astype(np.float).values
#     y = d["lat"].astype(np.float).values
#     heatmap, xedges, yedges = np.histogram2d(y, x, bins=bins)
#     extent = [yedges[0], yedges[-1], xedges[-1], xedges[0]]

#     logheatmap = np.log(heatmap)
#     logheatmap[np.isneginf(logheatmap)] = 0
#     logheatmap = ndimage.filters.gaussian_filter(logheatmap, smoothing, mode='nearest')
    
#     plt.imshow(heatmap, cmap=cmap, extent=extent)
#     plt.colorbar()
#     plt.gca().invert_yaxis()
#     plt.show()
# #    plt.savefig("car2go_logheatmap.png")    

#     return

# heatmap(car2go_parks_hour.groupby("hour").get_group(0), bins=20, smoothing=10)
# plt.show()


class Graphics():

    def __init__(self):
        pass

    def plot_duration_all(self, df):
        plt.figure()
        plt.title("Duration")
        df.duration.plot(figsize=(13,6), marker='o', label="Enjoy")

    def plot_duration(self, df):
        plt.figure()
        plt.title("Duration without outliers")
        #enjoy_reservations, enjoy_with_ride, enjoy_with_ride_filtered = dbp.filter_books_df_outliers(enjoy_books_df)
        #enjoy_with_ride_filtered.duration.plot(figsize=(13,6), marker='o', label="Enjoy", color="red")
        #enjoy_with_ride_filtered.duration.plot(figsize=(13,6), marker='o', label="Enjoy", color="red")
        df[(df['ride'] == True) & \
             (df['short_trips'] == True)].duration\
             .plot(figsize=(13,6), marker='o', label="enjoy", color="red")

    def hist(sefl, df):
        plt.figure()
        df[(df['ride'] == True) & \
                     (df['short_trips'] == True)].duration\
                     .hist(figsize=(13,6), label="enjoy", color="red", bins=100)

    def duration_aggregated(self, df1, df2):
        plt.figure()
        plt.title('Duration aggregated by 30 min')
        df1[(df1['ride'] == True)\
                     & (df1['short_trips'] == True)]\
                                 .set_index("start")\
                                 .resample("30Min").duration.mean()\
                                 .plot(figsize=(13,6), marker='o', label="Enjoy")

        df2[(df2['ride'] == True)\
                     & (df2['short_trips'] == True)]\
                                 .set_index("start")\
                                 .resample("30Min").duration.mean()\
                                 .plot(figsize=(13,6), marker='o', label="car2go")
        plt.legend()

    def bookings_aggregated(self, df1, df2):
        plt.figure()
        plt.title("Number of bookings aggregated by 30 min")
        df1[(df1['ride'] == True)\
                     & (df1['short_trips'] == True)]\
                                 .set_index("start")\
                                 .resample("30Min")._id.count()\
                                 .plot(figsize=(13,6), marker='o', label="Enjoy")

        df2[(df2['ride'] == True)\
                     & (df2['short_trips'] == True)]\
                                 .set_index("start")\
                                 .resample("30Min")._id.count()\
                                 .plot(figsize=(13,6), marker='o', label="car2go")
        plt.legend()

    def mean_bookings_aggregated(self, df1, df2):
        plt.figure()
        plt.title("Mean daily Number of bookings aggregated by hour")
        enjoy_nbooks = df1[(df1['ride'] == True)\
                             & (df1['short_trips'] == True)]\
                                 .set_index("start")\
                                 .resample("30Min")._id.count()
        enjoy_nbooks.groupby(enjoy_nbooks.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Enjoy N books", color="red")
        car2go_nbooks = df2[(df2['ride'] == True)\
                             & (df2['short_trips'] == True)]\
                                 .set_index("start")\
                                 .resample("30Min")._id.count()
        car2go_nbooks.groupby(car2go_nbooks.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Car2Go N books", color="blue")
        plt.legend()

    def mean_daily_duration(self, df1, df2):
        plt.figure()
        plt.title("Mean daily duration aggregated by hour")
        enjoy_duration = df1[(df1['ride'] == True)\
                             & (df1['short_trips'] == True)]\
                                 .set_index("start")\
                                 .resample("30Min")\
                                 .duration.mean()
        enjoy_duration.groupby(enjoy_duration.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Enjoy duration", color="red")
        car2go_duration = df2[(df2['ride'] == True)\
                             & (df2['short_trips'] == True)]\
                                 .set_index("start")\
                                 .resample("30Min")\
                                 .duration.mean()
        car2go_duration.groupby(car2go_duration.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Car2Go duration", color="blue")
        plt.legend()

    def daily_bills_aggregated(self, df1, df2):
        plt.figure()
        plt.title("Mean daily bills aggregated by hour")
        enjoy_min = df1[(df1['ride'] == True)\
                             & (df1['short_trips'] == True)]\
                             .set_index("start")\
                             .resample("30Min").min_bill.sum()
        enjoy_min.groupby(enjoy_min.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Enjoy min", color="red")
        enjoy_max = df1[(df1['ride'] == True)\
                             & (df1['short_trips'] == True)]\
                             .set_index("start")\
                             .resample("30Min").max_bill.sum()
        enjoy_max.groupby(enjoy_min.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Enjoy max", color="red")
        car2go_min = df2[(df2['ride'] == True)\
                             & (df2['short_trips'] == True)]\
                             .set_index("start")\
                             .resample("30Min").min_bill.sum()
        car2go_min.groupby(car2go_min.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="car2go min", color="blue")
        car2go_max = df2[(df2['ride'] == True)\
                             & (df2['short_trips'] == True)]\
                             .set_index("start")\
                             .resample("30Min").max_bill.sum()
        car2go_max.groupby(car2go_min.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="car2go max", color="blue")
        plt.legend()

    def cdf_weeks_duration(self, df1, df2):
        plt.figure()
        plt.title('CDF by weeks duration')
        weeks_number = df1['week'].unique()

        for week in weeks_number:
            df1[(df1['ride'] == True)\
                             & (df1['short_trips'] == True)\
                             & (df1['week']==week)].duration.hist(bins=10000, normed=1, cumulative=True, histtype='step')

        for week in weeks_number:
            df2[(df2['ride'] == True)\
                             & (df2['short_trips'] == True)\
                             & (df2['week']==week)].duration.hist(bins=10000, normed=1, cumulative=True, histtype='step')
        plt.ylabel('p')
        plt.xlabel('duration [m]')
        plt.axis([0, 120, 0, 1.1])
        plt.legend(loc=4)

    def cdf_weeks_distance(self, df1, df2):
        plt.figure()
        plt.title('CDF : weeks distance')
        weeks_number = df1['week'].unique()

        for week in weeks_number:
            df1[(df1['ride'] == True)\
                             & (df1['short_trips'] == True)\
                             & (df1['week']==week)].distance_driving\
                             .hist(bins=100, normed=1, label='enjoy '+str(week), cumulative=True, histtype='step')

        for week in weeks_number:
           df2[(df2['ride'] == True)\
                            & (df2['short_trips'] == True)\
                            & (df2['week']==week)].distance_driving\
                            .hist(bins=100, normed=1, label='car2go '+str(week), cumulative=True, histtype='step')
                            
        plt.ylabel('p')
        plt.xlabel('distance [km]')
        plt.axis([0, 20, 0, 1.1])
        plt.legend(loc=4)