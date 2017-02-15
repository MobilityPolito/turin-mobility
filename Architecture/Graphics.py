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

def color(df):
    if df['provider'][0] == 'car2go':
        return 'blue'
    else:
        return 'red'

class Graphics():

    def __init__(self):
        pass

    def duration_all(self, df1, df2):
        plt.figure()
        plt.title("Duration")
        df1.duration.plot(figsize=(13,6), marker='o', label="Enjoy")
        df2.duration.plot(figsize=(13,6), marker='o', label="car2go")

    def duration(self, df):
        plt.figure()
        plt.title("Duration without outliers " +str(df['provider'][0]))
        df[(df['ride'] == True) & \
             (df['short_trips'] == True)].duration\
             .plot(figsize=(13,6), marker='o', label=str(df['provider'][0]), color=color(df))

    def hist(sefl, df, cumulative):
        if (cumulative):
            plt.figure()
            df[(df['ride'] == True) & \
                 (df['short_trips'] == True)].duration\
                 .hist(figsize=(13,6), label=str(df['provider'][0]), color=color(df), bins=100, cumulative=True)
        else:
            plt.figure()
            df[(df['ride'] == True) & \
                         (df['short_trips'] == True)].duration\
                         .hist(figsize=(13,6), label=str(df['provider'][0]), color=color(df), bins=100)

    def duration_aggregated(self, df1, df2):
        plt.figure()
        plt.title('Duration aggregated by 30 min')
        df1[(df1['ride'] == True)\
                     & (df1['short_trips'] == True)]\
                                 .set_index("start")\
                                 .resample("30Min").duration.mean()\
                                 .plot(figsize=(13,6), marker='o', label=str(df1['provider'][0]))

        df2[(df2['ride'] == True)\
                     & (df2['short_trips'] == True)]\
                                 .set_index("start")\
                                 .resample("30Min").duration.mean()\
                                 .plot(figsize=(13,6), marker='o', label=str(df2['provider'][0]))
        plt.legend()

    def bookings_aggregated(self, df1, df2):
        plt.figure()
        plt.title("Number of bookings aggregated by 30 min")
        df1[(df1['ride'] == True)\
                     & (df1['short_trips'] == True)]\
                                 .set_index("start")\
                                 .resample("30Min")._id.count()\
                                 .plot(figsize=(13,6), marker='o', label=str(df1['provider'][0]))

        df2[(df2['ride'] == True)\
                     & (df2['short_trips'] == True)]\
                                 .set_index("start")\
                                 .resample("30Min")._id.count()\
                                 .plot(figsize=(13,6), marker='o', label=str(df2['provider'][0]))
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

    def daily_min_bill_aggregated(self, df1, df2):
        plt.figure()
        plt.title("Daily min bill aggregated by 30 min")
        df1[(df1['ride'] == True)\
                             & (df1['short_trips'] == True)]\
                                 .set_index("start")\
                                 .resample("30Min")\
                                 .min_bill.sum()\
                                 .plot(figsize=(13,6), marker='o', label="Enjoy")
        df2[(df2['ride'] == True)\
                             & (df2['short_trips'] == True)]\
                                 .set_index("start")\
                                 .resample("30Min")\
                                 .min_bill.sum()\
                                 .plot(figsize=(13,6), marker='o', label="car2go")
        plt.legend()

    def daily_max_bill_aggregated(self, df1, df2):
        plt.figure()
        plt.title("Daily max bill aggregated by 30 min")
        df1[(df1['ride'] == True)\
                             & (df1['short_trips'] == True)]\
                                 .set_index("start")\
                                 .resample("30Min")\
                                 .max_bill.sum()\
                                 .plot(figsize=(13,6), marker='o', label="Enjoy")
        df2[(df2['ride'] == True)\
                             & (df2['short_trips'] == True)]\
                                 .set_index("start")\
                                 .resample("30Min")\
                                 .max_bill.sum()\
                                 .plot(figsize=(13,6), marker='o', label="car2go")
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

    def cdf_business_weekend(self, df):

        fig, ax = plt.subplots(figsize=(13, 6))
        plt.title(str(df['provider'][0]) + " - Business days vs Weekend days duration CDF")
        bd_df = df[(df['business'] == True) & \
                               (df['ride'] == True) &\
                               (df['quantile'] == True) 
                               ]
        n, bins, patches = ax.hist(bd_df.duration, 1000, histtype='step',
                                   cumulative=True, label="Business day",
                                   rwidth=2.0, color=color(df), normed=1)

        we_df = df[(df['weekend'] == True) & \
                               (df['ride'] == True) &\
                               (df['quantile'] == True) 
                               ]
        n, bins, patches = ax.hist(we_df.duration, 1000, histtype='step',
                                   cumulative=True, label="Week end", linestyle="--",
                                   rwidth=2.0, color=color(df), normed=1)
        ax.legend(loc=4)
        ax.set_xlabel('Durations')
        ax.set_ylabel('CDF probability')
        plt.show()

    def number_books_aggregated(self, df):
        df1 = df[(df['business'] == True) & \
                       (df['ride'] == True) &\
                       (df['quantile'] == True) 
                       ]
        df1 = df1.set_index("start").resample("60Min")._id.count().replace({0:np.NaN}).dropna()
        df1 = df1.groupby(df1.index.map(lambda t: t.hour)).mean()

        df2 = df[(df['weekend'] == True) & \
                               (df['ride'] == True) &\
                               (df['quantile'] == True) 
                               ]
        df2 = df2.set_index("start").resample("60Min")._id.count().replace({0:np.NaN}).dropna()
        df2 = df2.groupby(df2.index.map(lambda t: t.hour)).mean()

        fig, ax = plt.subplots(figsize=(13, 6))
        plt.title (str(df['provider'][0])+" rents in business day and week-ends")
        ax.set_xlabel('Time')
        ax.set_ylabel('Rents')

        plt_date = range(0,24)
        ax.plot(df1,linewidth=2.0, label= "Business days", color= color(df))
        ax.plot(df2,linewidth=2.0, linestyle='--', label= "weekends", color= color(df))
        plt.show()

    def car_vs_google(self, df):
        enj = df[(df['ride'] == True) &\
                     (df['short_trips'] == True) ]

        bis_y = bis_x = range(1,int(enj.duration.max()))

        fig, ax = plt.subplots(figsize=(13, 6))
        plt.title (str(df['provider'][0]) + " - Duration vs Google forecast time")
        ax.set_xlabel('Duration')
        ax.set_ylabel('Gogole Duration')

        ax.scatter(enj['duration_driving'],enj['duration'],
                   s=0.5, label= "Trips", color= color(df))
        ax.plot(bis_x,bis_y,linewidth=1.0, linestyle='--', 
                label= "Equal time bisector", color= "black")
        ax.set_xlabel("Google Forecast [m]")
        ax.set_ylabel("Measuerd Duration [m]")
        plt.axis([0, 50, 0, 50])
        plt.legend(loc=4)
        plt.show()

    def car_vs_google_comparison(self, df_provider1, df_provider2):
        df1 = df_provider1[(df_provider1['ride'] == True) &\
                     (df_provider1['short_trips'] == True) ]

        df2 = df_provider2[(df_provider2['ride'] == True) &\
                     (df_provider2['short_trips'] == True) ]

        bis_y = bis_x = range(1,int(df1.duration.max()))
        fig, ax = plt.subplots(figsize=(13, 6))
        plt.title (" - Duration vs Google forecast time")
        ax.set_xlabel('Duration')
        ax.set_ylabel('Gogole Duration')
        ax.scatter(df1['duration_driving'],df1['duration'],
                   s=1, label= "Trips", color= color(df1))
        ax.scatter(df2['duration_driving'],df2['duration'],
                   s=1, label= "Trips", color= color(df2))
        ax.plot(bis_x,bis_y,linewidth=1.0, linestyle='--', 
                label= "Equal time bisector", color= "black")
        ax.set_xlabel("Google Forecast [m]")
        ax.set_ylabel("Measuerd Duration [m]")
        plt.axis([0, 50, 0, 50])
        plt.legend(loc=4)
        plt.show()