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

from DataBaseProxy import DataBaseProxy
dbp = DataBaseProxy()

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

#enjoy_books_df = dbp.query_books_df_filtered("enjoy", "torino", start, end)
#car2go_books_df = dbp.query_books_df_filtered("car2go", "torino", start, end)

enjoy_improved = dbp.filter_books_df_outliers(enjoy_books_df)
car2go_improved = dbp.filter_books_df_outliers(car2go_books_df)

plt.figure()
plt.title("Duration")
enjoy_books_df.duration.plot(figsize=(13,6), marker='o', label="Enjoy")
car2go_books_df.duration.plot(figsize=(13,6), marker='o', label="Car2Go")

plt.figure()
plt.title("Duration without outliers")
#enjoy_reservations, enjoy_with_ride, enjoy_with_ride_filtered = dbp.filter_books_df_outliers(enjoy_books_df)
#enjoy_with_ride_filtered.duration.plot(figsize=(13,6), marker='o', label="Enjoy", color="red")
#enjoy_with_ride_filtered.duration.plot(figsize=(13,6), marker='o', label="Enjoy", color="red")
enjoy_improved[(enjoy_improved['ride'] == True) & \
                         (enjoy_improved['short_trips'] == True)].duration\
                         .plot(figsize=(13,6), marker='o', label="enjoy", color="red")

#
plt.figure()
plt.title("Duration without outliers")
#car2go_reservations, car2go_with_ride, car2go_with_ride_filtered = dbp.filter_books_df_outliers(car2go_books_df)
#car2go_with_ride_filtered.duration.plot(figsize=(13,6), marker='o', label="Car2Go", color="blue")
#car2go_with_ride_filtered.duration.plot(figsize=(13,6), marker='o', label="Car2Go", color="blue")
car2go_improved[(car2go_improved['ride'] == True) & \
                         (car2go_improved['short_trips'] == True)].duration\
                         .plot(figsize=(13,6), marker='o', label="car2go", color="blue")

# HIST OLD
#plt.figure()
#enjoy_with_ride_filtered.duration.hist(bins=100, figsize=(13,6))
#plt.figure()
#car2go_with_ride_filtered.duration.hist(bins=100, figsize=(13,6))
#plt.figure()
#enjoy_with_ride_filtered.duration.hist(bins=100, figsize=(13,6), cumulative=True)
#plt.figure()
#car2go_with_ride_filtered.duration.hist(bins=100, figsize=(13,6), cumulative=True)
# END HIST OLD 


### HISTS ###
plt.figure()
enjoy_improved[(enjoy_improved['ride'] == True) & \
                         (enjoy_improved['short_trips'] == True)].duration\
                         .hist(figsize=(13,6), label="enjoy", color="red", bins=100)
plt.figure()
car2go_improved[(car2go_improved['ride'] == True) & \
                         (car2go_improved['short_trips'] == True)].duration\
                         .hist(figsize=(13,6), label="car2go", color="blue", bins=100)

plt.figure()
enjoy_improved[(enjoy_improved['ride'] == True) & \
                         (enjoy_improved['short_trips'] == True)].duration\
                         .hist(figsize=(13,6), label="enjoy", color="red", bins=100, cumulative=True)

plt.figure()
car2go_improved[(car2go_improved['ride'] == True) & \
                         (car2go_improved['short_trips'] == True)].duration\
                         .hist(figsize=(13,6), label="car2go", color="blue", bins=100, cumulative=True)

#plt.figure()
#plt.title("Duration aggregated by 30 min")
#enjoy_with_ride_filtered.set_index("start").resample("30Min").duration.mean()\
#    .plot(figsize=(13,6), marker='o', label="Enjoy")
#car2go_with_ride_filtered.set_index("start").resample("30Min").duration.mean()\
#    .plot(figsize=(13,6), marker='o', label="Car2Go")
#plt.legend()
#

### Duration aggregated 30 min NEW ###
plt.figure()
plt.title('Duration aggregated by 30 min')
enjoy_improved[(enjoy_improved['ride'] == True)\
             & (enjoy_improved['short_trips'] == True)]\
                         .set_index("start")\
                         .resample("30Min").duration.mean()\
                         .plot(figsize=(13,6), marker='o', label="Enjoy")

car2go_improved[(car2go_improved['ride'] == True)\
             & (car2go_improved['short_trips'] == True)]\
                         .set_index("start")\
                         .resample("30Min").duration.mean()\
                         .plot(figsize=(13,6), marker='o', label="car2go")
plt.legend()


#plt.figure()
#plt.title("Number of bookings aggregated by 30 min")
#enjoy_with_ride_filtered.set_index("start").resample("30Min")._id.count()\
#    .plot(figsize=(13,6), marker='o', label="Enjoy")
#car2go_with_ride_filtered.set_index("start").resample("30Min")._id.count()\
#    .plot(figsize=(13,6), marker='o', label="Car2Go")
#plt.legend()
#

plt.figure()
plt.title("Number of bookings aggregated by 30 min")
enjoy_improved[(enjoy_improved['ride'] == True)\
             & (enjoy_improved['short_trips'] == True)]\
                         .set_index("start")\
                         .resample("30Min")._id.count()\
                         .plot(figsize=(13,6), marker='o', label="Enjoy")

car2go_improved[(car2go_improved['ride'] == True)\
             & (car2go_improved['short_trips'] == True)]\
                         .set_index("start")\
                         .resample("30Min")._id.count()\
                         .plot(figsize=(13,6), marker='o', label="car2go")
plt.legend()

### MEAN number books old ###
#plt.figure()
#plt.title("Mean daily Number of bookings aggregated by hour")
#enjoy_nbooks = enjoy_with_ride_filtered.set_index("start").resample("30Min")._id.count()
#enjoy_nbooks.groupby(enjoy_nbooks.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Enjoy N books", color="red")
#car2go_nbooks = car2go_with_ride_filtered.set_index("start").resample("30Min")._id.count()
#car2go_nbooks.groupby(car2go_nbooks.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Car2Go N books", color="blue")
#plt.legend()
#

plt.figure()
plt.title("Mean daily Number of bookings aggregated by hour")
enjoy_nbooks = enjoy_improved[(enjoy_improved['ride'] == True)\
                     & (enjoy_improved['short_trips'] == True)]\
                         .set_index("start")\
                         .resample("30Min")._id.count()
enjoy_nbooks.groupby(enjoy_nbooks.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Enjoy N books", color="red")
car2go_nbooks = car2go_improved[(car2go_improved['ride'] == True)\
                     & (car2go_improved['short_trips'] == True)]\
                         .set_index("start")\
                         .resample("30Min")._id.count()
car2go_nbooks.groupby(car2go_nbooks.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Car2Go N books", color="blue")
plt.legend()


### MEAN DURATION OLD ###
#plt.figure()
#plt.title("Mean daily duration aggregated by hour")
#enjoy_duration = enjoy_with_ride_filtered.set_index("start").resample("30Min").duration.mean()
#enjoy_duration.groupby(enjoy_duration.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Enjoy duration", color="red")
#car2go_duration = car2go_with_ride_filtered.set_index("start").resample("30Min").duration.mean()
#car2go_duration.groupby(car2go_duration.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Car2Go duration", color="blue")
#plt.legend()
#

plt.figure()
plt.title("Mean daily duration aggregated by hour")
enjoy_duration = enjoy_improved[(enjoy_improved['ride'] == True)\
                     & (enjoy_improved['short_trips'] == True)]\
                         .set_index("start")\
                         .resample("30Min")\
                         .duration.mean()
enjoy_duration.groupby(enjoy_duration.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Enjoy duration", color="red")
car2go_duration = car2go_improved[(car2go_improved['ride'] == True)\
                     & (car2go_improved['short_trips'] == True)]\
                         .set_index("start")\
                         .resample("30Min")\
                         .duration.mean()
car2go_duration.groupby(car2go_duration.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Car2Go duration", color="blue")
plt.legend()


#plt.figure()
#plt.title("Daily min bill aggregated by 30 min")
#enjoy_with_ride_filtered.set_index("start").resample("30Min").min_bill.sum()\
#    .plot(figsize=(13,6), marker='o', label="Enjoy")
#car2go_with_ride_filtered.set_index("start").resample("30Min").min_bill.sum()\
#    .plot(figsize=(13,6), marker='o', label="Car2Go")
#plt.legend()
#


plt.figure()
plt.title("Daily min bill aggregated by 30 min")
enjoy_improved[(enjoy_improved['ride'] == True)\
                     & (enjoy_improved['short_trips'] == True)]\
                         .set_index("start")\
                         .resample("30Min")\
                         .min_bill.sum()\
                         .plot(figsize=(13,6), marker='o', label="Enjoy")
car2go_improved[(car2go_improved['ride'] == True)\
                     & (car2go_improved['short_trips'] == True)]\
                         .set_index("start")\
                         .resample("30Min")\
                         .min_bill.sum()\
                         .plot(figsize=(13,6), marker='o', label="car2go")
plt.legend()


#plt.figure()
#plt.title("Daily max bill aggregated by 30 min")
#enjoy_with_ride_filtered.set_index("start").resample("30Min").max_bill.sum()\
#    .plot(figsize=(13,6), marker='o', label="Enjoy")
#car2go_with_ride_filtered.set_index("start").resample("30Min").max_bill.sum()\
#    .plot(figsize=(13,6), marker='o', label="Car2Go")
#plt.legend()
#

plt.figure()
plt.title("Daily max bill aggregated by 30 min")
enjoy_improved[(enjoy_improved['ride'] == True)\
                     & (enjoy_improved['short_trips'] == True)]\
                         .set_index("start")\
                         .resample("30Min")\
                         .max_bill.sum()\
                         .plot(figsize=(13,6), marker='o', label="Enjoy")
car2go_improved[(car2go_improved['ride'] == True)\
                     & (car2go_improved['short_trips'] == True)]\
                         .set_index("start")\
                         .resample("30Min")\
                         .max_bill.sum()\
                         .plot(figsize=(13,6), marker='o', label="car2go")
plt.legend()


#plt.figure()
#plt.title("Mean daily bills aggregated by hour")    
#enjoy_min = enjoy_with_ride_filtered.set_index("start").resample("30Min").min_bill.sum()
#enjoy_min.groupby(enjoy_min.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Enjoy min", color="red")
#enjoy_max = enjoy_with_ride_filtered.set_index("start").resample("30Min").max_bill.sum()
#enjoy_max.groupby(enjoy_min.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Enjoy max", color="red")
#car2go_min = car2go_with_ride_filtered.set_index("start").resample("30Min").min_bill.sum()
#car2go_min.groupby(enjoy_min.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Car2Go min", color="blue")
#car2go_max = car2go_with_ride_filtered.set_index("start").resample("30Min").max_bill.sum()
#car2go_max.groupby(enjoy_min.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Car2Go max", color="blue")
#plt.legend()

plt.figure()
plt.title("Mean daily bills aggregated by hour")
enjoy_min = enjoy_improved[(enjoy_improved['ride'] == True)\
                     & (enjoy_improved['short_trips'] == True)]\
                     .set_index("start")\
                     .resample("30Min").min_bill.sum()
enjoy_min.groupby(enjoy_min.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Enjoy min", color="red")
enjoy_max = enjoy_improved[(enjoy_improved['ride'] == True)\
                     & (enjoy_improved['short_trips'] == True)]\
                     .set_index("start")\
                     .resample("30Min").max_bill.sum()
enjoy_max.groupby(enjoy_min.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="Enjoy max", color="red")
car2go_min = car2go_improved[(car2go_improved['ride'] == True)\
                     & (car2go_improved['short_trips'] == True)]\
                     .set_index("start")\
                     .resample("30Min").min_bill.sum()
car2go_min.groupby(car2go_min.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="car2go min", color="blue")
car2go_max = car2go_improved[(car2go_improved['ride'] == True)\
                     & (car2go_improved['short_trips'] == True)]\
                     .set_index("start")\
                     .resample("30Min").max_bill.sum()
car2go_max.groupby(car2go_min.index.map(lambda t: t.hour)).mean().plot(figsize=(13,6), marker='o', label="car2go max", color="blue")
plt.legend()

### CDF WEEKS ###
plt.figure()
plt.title('CDF by weeks duration')
weeks_number = enjoy_improved['week'].unique()

for week in weeks_number:
    enjoy_improved[(enjoy_improved['ride'] == True)\
                     & (enjoy_improved['short_trips'] == True)\
                     & (enjoy_improved['week']==week)].duration.hist(bins=10000, normed=1, cumulative=True, histtype='step')

# enjoy_improved[(enjoy_improved['ride'] == True)\
#                      & (enjoy_improved['short_trips'] == True)\
#                      & (enjoy_improved['week']==1) & (enjoy_improved['quantile'])].duration.hist(bins=10000, normed=1, cumulative=True, histtype='step')
# enjoy_improved[(enjoy_improved['ride'] == True)\
#                      & (enjoy_improved['short_trips'] == True)\
#                      & (enjoy_improved['week']==2)& (enjoy_improved['quantile'])].duration.hist(bins=10000, normed=1, cumulative=True, histtype='step')
# enjoy_improved[(enjoy_improved['ride'] == True)\
#                      & (enjoy_improved['short_trips'] == True)\
#                      & (enjoy_improved['week']==52)& (enjoy_improved['quantile'])].duration.hist(bins=10000, normed=1, cumulative=True, histtype='step')

for week in weeks_number:
    car2go_improved[(car2go_improved['ride'] == True)\
                     & (car2go_improved['short_trips'] == True)\
                     & (car2go_improved['week']==week)].duration.hist(bins=10000, normed=1, cumulative=True, histtype='step')
plt.legend()

plt.figure()
plt.title('CDF : weeks distance')
weeks_number = enjoy_improved['week'].unique()

for week in weeks_number:
    enjoy_improved[(enjoy_improved['ride'] == True)\
                     & (enjoy_improved['short_trips'] == True)\
                     & (enjoy_improved['week']==week)].distance_driving\
                     .hist(bins=100, normed=1, label='enjoy '+str(week), cumulative=True, histtype='step')

for week in weeks_number:
   car2go_improved[(car2go_improved['ride'] == True)\
                    & (car2go_improved['short_trips'] == True)\
                    & (car2go_improved['week']==week)].distance_driving\
                    .hist(bins=100, normed=1, label='car2go '+str(week), cumulative=True, histtype='step')
                    
plt.ylabel('p')
plt.xlabel('distance [km]')
plt.axis([0, 20, 0, 1.1])
plt.legend(loc=4)

print "s - ***********************************************"

'''CDF bd vs we enjoy'''
fig, ax = plt.subplots(figsize=(13, 6))
plt.title("Enjoy - Business days vs Weekend days duration CDF")
bd_df = enjoy_improved[(enjoy_improved['business'] == True) & \
                       (enjoy_improved['ride'] == True) &\
                       (enjoy_improved['quantile'] == True) 
                       ]
n, bins, patches = ax.hist(bd_df.duration, 1000, histtype='step',
                           cumulative=True, label="Business day",
                           rwidth=2.0, color='red')

we_df = enjoy_improved[(enjoy_improved['weekend'] == True) & \
                       (enjoy_improved['ride'] == True) &\
                       (enjoy_improved['quantile'] == True) 
                       ]
n, bins, patches = ax.hist(we_df.duration, 1000, histtype='step',
                           cumulative=True, label="Week end", linestyle="--",
                           rwidth=2.0,color='red')
ax.legend(loc=4)
ax.set_xlabel('Durations')
ax.set_ylabel('CDF probability')
plt.show()

'''CDF bd vs we c2g'''
fig, ax = plt.subplots(figsize=(13, 6))
plt.title("Car2go - Business days vs Weekend days duration CDF")
bd_df = car2go_improved[(car2go_improved['business'] == True) & \
                       (car2go_improved['ride'] == True) &\
                       (car2go_improved['quantile'] == True) 
                       ]
n, bins, patches = ax.hist(bd_df.duration, 1000, histtype='step',
                           cumulative=True, label="Business day",
                           rwidth=2.0, color='blue', normed = True)

we_df = car2go_improved[(car2go_improved['weekend'] == True) & \
                       (car2go_improved['ride'] == True) &\
                       (car2go_improved['quantile'] == True) 
                       ]
n, bins, patches = ax.hist(we_df.duration, 1000, histtype='step',
                           cumulative=True, label="Week end", linestyle="--",
                           rwidth=2.0, color='blue', normed = True)
ax.legend(loc=4)
ax.set_xlabel('Durations')
ax.set_ylabel('CDF probability')
plt.show()


''' ENJ RENTS PER BD VS WE'''
df1 = enjoy_improved[(enjoy_improved['business'] == True) & \
                       (enjoy_improved['ride'] == True) &\
                       (enjoy_improved['quantile'] == True) 
                       ]
df1 = df1.set_index("start").resample("60Min")._id.count().replace({0:np.NaN}).dropna()
df1 = df1.groupby(df1.index.map(lambda t: t.hour)).mean()

df2 = enjoy_improved[(enjoy_improved['weekend'] == True) & \
                       (enjoy_improved['ride'] == True) &\
                       (enjoy_improved['quantile'] == True) 
                       ]
df2 = df2.set_index("start").resample("60Min")._id.count().replace({0:np.NaN}).dropna()
df2 = df2.groupby(df2.index.map(lambda t: t.hour)).mean()

fig, ax = plt.subplots(figsize=(13, 6))
plt.title ("Enjoy rents in business day and week-ends")
ax.set_xlabel('Time')
ax.set_ylabel('Rents')

plt_date = range(0,24)
ax.plot(df1,linewidth=2.0, label= "Business days", color= "red")
ax.plot(df2,linewidth=2.0, linestyle='--', label= "weekends", color= "red")
plt.show()

''' C2G RENTS PER BD VS WE'''
df1 = car2go_improved[(car2go_improved['business'] == True) & \
                      (car2go_improved['ride'] == True) &\
                      (car2go_improved['quantile'] == True) 
                       ]
df1 = df1.set_index("start").resample("60Min")._id.count().replace({0:np.NaN}).dropna()
df1 = df1.groupby(df1.index.map(lambda t: t.hour)).mean()

df2 = car2go_improved[(car2go_improved['weekend'] == True) & \
                      (car2go_improved['ride'] == True) &\
                      (car2go_improved['quantile'] == True) 
                       ]
df2 = df2.set_index("start").resample("60Min")._id.count().replace({0:np.NaN}).dropna()
df2 = df2.groupby(df2.index.map(lambda t: t.hour)).mean()

fig, ax = plt.subplots(figsize=(13, 6))
plt.title ("Car2go rents in business day and week-ends")
ax.set_xlabel('Time')
ax.set_ylabel('Rents')

plt_date = range(0,24)
ax.plot(df1,linewidth=2.0, label= "Business days", color= "blue")
ax.plot(df2,linewidth=2.0, linestyle='--', label= "weekends", color= "blue")
plt.show()

'''Enj Tcar vs Tgoogle'''
enj = enjoy_improved[(enjoy_improved['ride'] == True) &\
                     (enjoy_improved['quantile'] == True) 
                       ]
bis_y = bis_x = range(1,int(enj.duration.max()))

fig, ax = plt.subplots(figsize=(13, 6))
plt.title ("Enjoy - Duration vs Google forecast time")
ax.set_xlabel('Duration')
ax.set_ylabel('Gogole Duration')

plt_date = range(0,24)
ax.scatter(enj['duration_driving'],enj['duration'],
           s=0.5, label= "Trips", color= "red")
ax.plot(bis_x,bis_y,linewidth=1.0, linestyle='--', 
        label= "Equal time bisector", color= "black")
ax.set_xlabel("Google Forecast")
ax.set_ylabel("Measuerd Duratiion")
plt.legend(loc=4)
plt.show()

'''c2g Tcar vs Tgoogle'''
c2g = car2go_improved[(car2go_improved['ride'] == True) &\
                      (car2go_improved['quantile'] == True) 
                       ]
bis_y = bis_x = range(1,int(enj.duration.max()))

fig, ax = plt.subplots(figsize=(13, 6))
plt.title ("Car2go - Duration vs Google forecast time")
ax.set_xlabel('Duration')
ax.set_ylabel('Gogole Duration')

plt_date = range(0,24)
ax.scatter(c2g['duration_driving'],c2g['duration'],
           s=1.0, label= "Trips", color= "blue")
ax.plot(bis_x,bis_y,linewidth=1.0, linestyle='--',
        label= "Equal time bisector", color= "black")
ax.set_xlabel("Google Forecast")
ax.set_ylabel("Measuerd Duratiion")
plt.legend(loc=4)
plt.show()

print "E - ***********************************************"
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
