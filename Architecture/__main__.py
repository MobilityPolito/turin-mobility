import json
import datetime

import pandas as pd
import numpy as np

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

#city = "torino"
#provider = "enjoy"
#start = datetime.datetime(2016, 12, 5, 0, 0, 0)
#end = datetime.datetime(2016, 12, 12, 0, 0, 0)    
#enjoy_parks_df = dbp.query_parks_df(provider, city, start, end)

#city = "torino"
#provider = "enjoy"
#start = datetime.datetime(2016, 12, 5, 0, 0, 0)
#end = datetime.datetime(2016, 12, 12, 0, 0, 0)    
#enjoy_parks_df = dbp.query_parks_df_filtered(provider, city, start, end, "business")

city = "torino"
provider = "car2go"
start = datetime.datetime(2016, 12, 5, 0, 0, 0)
end = datetime.datetime(2016, 12, 8, 0, 0, 0)
car2go_books_df = dbp.query_books_df(provider, city, start, end)

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