import datetime
import pandas as pd
#import pprint

from Provider import Provider
from DataBaseProxy import dbp

        
class TObike(Provider):
    
    def __init__(self):
        self.name = "tobike"     
                
    def select_data(self,city,start,end):
        self.cursor =  dbp.query_time(self.name, city, start,end)

        
    def get_fields(self):
        sample_columns = pd.DataFrame(self.cursor.next()["state"]).columns
        for doc in self.cursor:
            columns = pd.DataFrame(doc["state"]).columns
            if len(columns.difference(sample_columns)): 
                print "Warning: different fields for the same provider"
        self.fields = columns

    def get_stations(self):
        self.cursor.rewind()
        doc = self.cursor.next()
        df = pd.DataFrame(doc["state"])
        stations = pd.Index(df['id'].values)
        self.stations = stations
        return self.stations
        
    #get histograms
    
tobike = TObike()
end = datetime.datetime(2016, 12, 19, 16, 0, 0)
start = end - datetime.timedelta(hours = 1)
tobike.select_data("torino", start, end)
tobike.get_fields()
stations = list( tobike.get_stations())