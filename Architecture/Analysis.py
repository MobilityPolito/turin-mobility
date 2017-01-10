import datetime

import pandas as pd

from DataBaseProxy import DataBaseProxy
dbp = DataBaseProxy()

# Parks durations

def get_parks (provider, city, start, end):
    
    parks_cursor = dbp.query_park_by_time(provider, city, start, end)
    
    parks_df = pd.DataFrame(columns = pd.Series(parks_cursor.next()).index)
    for doc in parks_cursor:
        s = pd.Series(doc)
        parks_df = pd.concat([parks_df, pd.DataFrame(s).T], ignore_index=True)

    return parks_df
    
# Books durations

def get_books (provider, city, start, end):

    books_cursor = dbp.query_book_by_time(provider, city, start, end)
    
    books_df = pd.DataFrame(columns = pd.Series(books_cursor.next()).index)
    for doc in books_cursor:
        s = pd.Series(doc)
        books_df = pd.concat([books_df, pd.DataFrame(s).T], ignore_index=True)    

    return books_df
    
import geopandas as gpd
from geopandas.geoseries import *
import matplotlib.pyplot as plt

gdf = gpd.read_file("../../SHAPE/Zonizzazione.dbf")

#gs = gdf["geometry"]
#gs.plot()
#plt.show()

end = datetime.datetime(2016, 11, 25, 0, 0, 0)
start = end - datetime.timedelta(days = 1)

parks_df = get_parks("car2go","torino", start, end)

import utm

points = gpd.GeoSeries(parks_df[["lat","lon"]].apply\
                   (lambda row: Point(row["lat"], row["lon"]), axis=1), name = "geometry")

#from shapely.geometry import *
#    
#for zone_id in list(gdf.index):
#
#    poly = gpd.GeoSeries(gdf.ix[zone_id, "geometry"])
#
#    for p in list(points.values):
#        print(poly.intersects(p))
#    
##    mask = points.intersects(poly.ix[0])
##    print mask[mask == True]