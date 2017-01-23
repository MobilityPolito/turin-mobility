import json
import datetime

from Car2GoProvider import Car2Go
from EnjoyProvider import Enjoy

from DataBaseProxy import DataBaseProxy

dbp = DataBaseProxy()
#dbp.compress()

#city = "torino"
#for provider in ["car2go", "enjoy"]:
#    start = datetime.datetime(2016, 12, 5, 0, 0, 0)
#    end = datetime.datetime(2016, 12, 10, 0, 0, 0)    
#    cursor = dbp.query_raw_by_time(provider, city, start, end)
#    for doc in cursor:        
#        dbp.db["snapshots"].update_one({"_id":  doc["_id"]},
#                                  {"$set": {"city":"torino"}},
#                                  upsert = True)

#city = "torino"
#provider = "car2go"
#start = datetime.datetime(2016, 12, 5, 0, 0, 0)
#end = datetime.datetime(2016, 12, 10, 0, 0, 0)    
#cursor = dbp.query_raw_by_time(provider, city, start, end)
#for doc in cursor:
#    print doc["_id"]

#city = "torino"
#provider = "enjoy"
#start = datetime.datetime(2016, 12, 5, 0, 0, 0)
#end = datetime.datetime(2016, 12, 10, 0, 0, 0)    
#cursor = dbp.query_raw_by_time(provider, city, start, end)
#for doc in cursor:
#    print doc["_id"]

#city = "torino"
#provider = "enjoy"
#start = datetime.datetime(2016, 12, 5, 0, 0, 0)
#end = datetime.datetime(2016, 12, 10, 0, 0, 0)    
#enjoy_parks_df = dbp.query_parks_df(provider, city, start, end)

city = "torino"
provider = "enjoy"
start = datetime.datetime(2016, 12, 7, 0, 0, 0)
end = datetime.datetime(2016, 12, 10, 0, 0, 0)    
enjoy_parks_df = dbp.query_parks_df_filtered(provider, city, start, end, "holiday")
