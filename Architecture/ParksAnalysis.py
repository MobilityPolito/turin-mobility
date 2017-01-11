import datetime

import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

from DataBaseProxy import DataBaseProxy
dbp = DataBaseProxy()

# Parks durations

def get_parks_df (provider, city, start, end):
    
    parks_cursor = dbp.query_park_by_time(provider, city, start, end)
    
    parks_df = pd.DataFrame(columns = pd.Series(parks_cursor.next()).index)
    for doc in parks_cursor:
        s = pd.Series(doc)
        parks_df = pd.concat([parks_df, pd.DataFrame(s).T], ignore_index=True)

    return parks_df
    
end = datetime.datetime(2016, 12, 10, 0, 0, 0)
start = end - datetime.timedelta(days = 1)
parks_df = get_parks_df("enjoy", "torino", start, end)
parks_df["durations"] = (parks_df["end"] - parks_df["start"])/np.timedelta64(1, 'm')
parks_df = parks_df[parks_df["durations"] < 200]

from pandas.tools.plotting import scatter_matrix
scatter_matrix(parks_df[["lat","lon","durations"]].astype("float64"), 
               figsize=(25, 25), diagonal='kde')
plt.savefig("scatter_matrix.png")

#from pandas.tools.plotting import andrews_curves
#fig = plt.figure(figsize=(25,25))
#andrews_curves(df[["country"] + scores_cols].iloc[:200].dropna(), "country")
#plt.savefig("andrews_curves.png")
#
#from pandas.tools.plotting import radviz
#fig = plt.figure(figsize=(25,25))
#radviz(df[["country"] + scores_cols].iloc[:200].dropna(), "country")
#plt.savefig("radviz.png")