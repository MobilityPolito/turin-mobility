import datetime

import numpy as np
import pandas as pd

#import geopandas as gpd
#from shapely.geometry import Point
#from shapely.geometry import LineString

#from Car2GoProvider import Car2Go
#from EnjoyProvider import Enjoy

from DataBaseProxy import DataBaseProxy
dbp = DataBaseProxy()

def day_analysis (parks_df, year, month, day):

    day_stats = pd.DataFrame()
    start = datetime.datetime(year, month, day, 0, 0, 0)
    end = datetime.datetime(year, month, day, 23, 59, 0)
    provider = parks_df["provider"].unique()[0]
    city = parks_df["city"].unique()[0]
    fleet_size = float(len(dbp.query_fleet_by_day(provider, city, start, end)[0]["fleet"]))

    for hour in range(0, 24, 1):
        sup_datetime = datetime.datetime(year, month, day, hour, 59, 59)
        inf_datetime = datetime.datetime(year, month, day, hour, 0, 0)

        day_stats.loc[sup_datetime, "n"] = \
            float(len(parks_df[inf_datetime:sup_datetime]))
            
        day_stats.loc[sup_datetime, "n_norm"] = \
            float(len(parks_df[inf_datetime:sup_datetime]))/fleet_size

        day_stats.loc[sup_datetime, "avg_duration"] = \
            parks_df[inf_datetime:sup_datetime]["duration"].mean()
            
        day_stats.loc[sup_datetime, "med_duration"] = \
            parks_df[inf_datetime:sup_datetime]["duration"].median()
        
    return day_stats

def get_hours_stats (parks_df):

    parks_df["start_"] = parks_df["start"]
    parks_df = parks_df.set_index("start_").sort_index()
    parks_df["date"] = parks_df["start"].apply(lambda x: x.date())
    
    stats = pd.DataFrame()
    for date, group in parks_df.groupby("date"):
        stats = pd.concat([stats, day_analysis(group, date.year, date.month, date.day)])
    stats["time"] = pd.Series(stats.index.values).apply(lambda x: x.time()).values

    return parks_df, stats.groupby("time").aggregate(np.mean)

def group_parks_by_hour (parks_df):

    parks_df["start_"] = parks_df["start"]
    parks_df = parks_df.set_index("start_").sort_index()
    parks_df["hour"] = parks_df["start"].apply(lambda x: x.hour)
    
    return parks_df
    
start = datetime.datetime(2016, 12, 5, 0, 0, 0)
end = datetime.datetime.now()

#car2go_parks = dbp.query_parks_df_filtered("car2go", "torino", start, end, "weekend")
#enjoy_parks = dbp.query_parks_df_filtered("enjoy", "torino", start, end, "weekend")

car2go_parks_modified, car2go_parks_stats = get_hours_stats(car2go_parks)
enjoy_parks_modified, enjoy_parks_stats = get_hours_stats(enjoy_parks)

car2go_parks_hour = group_parks_by_hour(car2go_parks)
enjoy_parks_hour = group_parks_by_hour(enjoy_parks)
