import json
import datetime

import numpy as np

import pandas as pd

import statsmodels.api as sm
import statsmodels.formula.api as smf

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

from pandas.tools.plotting import scatter_matrix

from Car2GoProvider import Car2Go
from EnjoyProvider import Enjoy

from DataBaseProxy import DataBaseProxy
dbp = DataBaseProxy()
#dbp.compress()

#start = datetime.datetime(2016, 12, 5, 0, 0, 0)
#end = datetime.datetime(2016, 12, 12, 0, 0, 0)
enjoy = Enjoy()
enjoy_fleet = enjoy.get_fleet_from_db()
#enjoy.select_data("torino", "timestamp", start, end)
#enjoy.get_parks_and_books()
car2go = Car2Go() 
car2go_fleet = car2go.get_fleet_from_db()
#car2go.select_data("torino", "timestamp", start, end)
#car2go.get_parks_and_books()

#city = "torino"
#for provider in ["car2go", "enjoy"]:
#    start = datetime.datetime(2016, 12, 5, 0, 0, 0)
#    end = datetime.datetime(2016, 12, 12, 0, 0, 0)    
#    cursor = dbp.query_raw_by_time(provider, city, start, end)
#    for doc in cursor:        
#        dbp.db["snapshots"].update_one({"_id":  doc["_id"]},
#                                  {"$set": {"city":"torino"}},
#                                  upsert = True)

#city = "torino"
#provider = "car2go"
#start = datetime.datetime(2016, 12, 5, 0, 0, 0)
#end = datetime.datetime(2016, 12, 12, 0, 0, 0)    
#cursor = dbp.query_raw_by_time(provider, city, start, end)
#for doc in cursor:
#    print doc["_id"]

#city = "torino"
#provider = "enjoy"
#start = datetime.datetime(2016, 12, 5, 0, 0, 0)
#end = datetime.datetime(2016, 12, 12, 0, 0, 0)    
#cursor = dbp.query_raw_by_time(provider, city, start, end)
#for doc in cursor:
#    print doc["_id"]

city = "torino"
provider = "enjoy"
start = datetime.datetime(2016, 12, 5, 0, 0, 0)
end = datetime.datetime(2016, 12, 12, 0, 0, 0)    
enjoy_parks_df = dbp.query_parks_df(provider, city, start, end)

#city = "torino"
#provider = "enjoy"
#start = datetime.datetime(2016, 12, 5, 0, 0, 0)
#end = datetime.datetime(2016, 12, 12, 0, 0, 0)    
#enjoy_parks_df = dbp.query_parks_df_filtered(provider, city, start, end, "business")

city = "torino"
provider = "car2go"
start = datetime.datetime(2016, 12, 5, 0, 0, 0)
end = datetime.datetime(2016, 12, 12, 0, 0, 0)
car2go_books_df = dbp.query_books_df(provider, city, start, end)

df = car2go_books_df[car2go_books_df.duration < 120]
df = df[(df.distance > 0.1)]
df = df[(df.distance_driving < 1000)]
df = df[df.fuel_consumption >= 0]

#fig, ax = plt.subplots(1, 1)
#ax = scatter_matrix(df[
#                        [
#                         "distance", 
#                         "duration", 
##                         "fuel_consumption",
##                         "reservation_time",
##                         "riding_time",
#                         "distance_driving",
#                         "duration_driving",
##                         "distance_google_transit",
##                         "duration_google_transit",
##                         "tot_duration_google_transit",
##                         "min_bill",
##                         "max_bill",
##                         "fare_google_transit"
#                        ]
#                       ].astype("float64"), 
#                       figsize=(10, 10), diagonal='kde')

x_google = df["distance_driving"]
y_google = df["duration_driving"]
y_db = df["duration"]

fig, ax = plt.subplots(1, 1)
ax = plt.scatter(x_google, y_db, linestyle='--', marker='.', color='r', alpha=1)
ax = plt.scatter(x_google, y_google, linestyle='--', marker='.', color='b', alpha=0.3)
plt.show()

fig, ax = plt.subplots(1, 1)
ax = plt.scatter(x_google, y_db - y_google, linestyle='--', marker='.', color='black', alpha=1)
ax = plt.scatter(np.arange(0,50,0.1), np.zeros(len(np.arange(0,50,0.1))), linestyle='--', marker='.', color='red', alpha=1)
plt.show()

df_sorted = df.sort_values("distance_driving")
x_google_sorted = df_sorted["distance_driving"]
y_google_sorted = df_sorted["duration_driving"]
y_db_sorted = df_sorted["duration"]

fig, ax = plt.subplots(1, 1)
ax = plt.plot(x_google_sorted, y_db_sorted, linestyle='--', marker='.', color='r', alpha=1)
ax = plt.plot(x_google_sorted, y_google_sorted, linestyle='--', marker='.', color='b', alpha=0.3)
plt.show()

fig, ax = plt.subplots(1, 1)
ax = plt.plot(x_google_sorted, y_db_sorted - y_google_sorted, linestyle='--', marker='.', color='black', alpha=1)
ax = plt.plot(np.arange(0,50,0.1), np.zeros(len(np.arange(0,50,0.1))), linestyle='--', marker='.', color='red', alpha=1)
plt.show()

#plt.savefig(provider + "_books_scatter_matrix.png")

#mod = smf.ols(formula='n_trips_origins ~ tot + area + lons + lats', data=df)
#res = mod.fit()
#print res.summary()
#
#fig, ax = plt.subplots()
#fig = sm.graphics.plot_fit(res, 1, ax=ax)

car2go_books_df.loc[(car2go_books_df.reservation_time < 0), "reservation_time"] = 0.0
false_trips_df = car2go_books_df[(car2go_books_df.distance < 0.1) & (car2go_books_df.fuel_consumption == 0)]

#def day_analysis (books_df, year, month, day, fleet_size):
#
#    day_stats = pd.DataFrame()
#    
#    for hour in range(0, 24, 1):
#        sup_datetime = datetime.datetime(year, month, day, hour, 59, 59)
#        inf_datetime = datetime.datetime(year, month, day, hour)
#
#        day_stats.loc[sup_datetime, "n_books"] = \
#            float(len(books_df[inf_datetime:sup_datetime]))
#        day_stats.loc[sup_datetime, "n_books_norm"] = \
#            float(len(books_df[inf_datetime:sup_datetime])) / fleet_size
#
#        day_stats.loc[sup_datetime, "avg_books_duration"] = \
#            books_df[inf_datetime:sup_datetime]["durations"].mean()
#        day_stats.loc[sup_datetime, "med_books_duration"] = \
#            books_df[inf_datetime:sup_datetime]["durations"].median()
#
#        day_stats.loc[sup_datetime, "avg_books_distance"] = \
#            books_df[inf_datetime:sup_datetime]["distances"].mean()
#        day_stats.loc[sup_datetime, "med_books_distance"] = \
#            books_df[inf_datetime:sup_datetime]["distances"].median()
#        
#        day_stats.loc[sup_datetime, "cum_books_bill"] = \
#            books_df[inf_datetime:sup_datetime]["bill"].sum()
#        
#    return day_stats
#
#def get_hours_stats (city, provider, start, end, fleet_size, day_type):
#
#    books_df = dbp.query_books_df_filtered(provider, city, start, end, day_type)
#    books_df["start_"] = books_df["start"]
#    books_df = books_df.set_index("start_").sort_index()
#    books_df["date"] = books_df["start"].apply(lambda x: x.date())
#    
#    stats = pd.DataFrame()
#    for date, group in books_df.groupby("date"):
#        stats = pd.concat([stats, day_analysis(group, date.year, date.month, date.day, fleet_size)])
#    stats["time"] = pd.Series(stats.index.values).apply(lambda x: x.time()).values
#
#    return books_df, stats.groupby("time").aggregate(np.mean)
#
#city = "torino"
#provider = "car2go"
#start = datetime.datetime(2016, 12, 5, 0, 0, 0)
#end = datetime.datetime(2016, 12, 12, 0, 0, 0)
#books_df, stats = get_hours_stats(city, provider, start, end, len(enjoy_fleet), "business")
#
#import matplotlib
#import matplotlib.pyplot as plt
#matplotlib.style.use('ggplot')
#
#stats["n_books_norm"].plot()
#plt.xticks(rotation=70)
#plt.show()