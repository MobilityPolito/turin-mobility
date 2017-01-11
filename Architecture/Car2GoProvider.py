import datetime
import pandas as pd

from Provider import Provider

from DataBaseProxy import DataBaseProxy
dbp = DataBaseProxy()

class Car2Go(Provider):
    
    def __init__ (self):
        self.name = "car2go"
        self.city = "torino"
    
    def select_data (self, city, by, *args):
        
        if by == "timestamp" and len(args) == 2:
            self.start, self.end = args
            self.cursor = dbp.query_raw_by_time(self.name, city, self.start, self.end)
            print "Data selected!"

    def get_fields(self):
        
        doc = self.cursor.next()
        return list(pd.DataFrame(doc["state"]["placemarks"]).columns)

    def get_fleet(self):

        self.cursor.rewind()        
        doc = self.cursor.next()
        current_fleet = pd.Index(pd.DataFrame(doc["state"]["placemarks"])\
                                 .loc[:,"name"].values)
        self.fleet = current_fleet
        for doc in self.cursor:
            current_fleet = pd.Index(pd.DataFrame(doc["state"]["placemarks"])\
                                     .loc[:,"name"].values)
            self.fleet = self.fleet.union(current_fleet)
            
        print "Fleet acquired!"

        return self.fleet

    def get_parks_v2 (self):
        
        self.cursor.rewind()
        doc = self.cursor.next()

        cars_status = pd.DataFrame(index = self.fleet.values)
        cars_lat = pd.DataFrame(index = self.fleet.values)
        cars_lon = pd.DataFrame(index = self.fleet.values)
        
        def update_cars_status ():
            df = pd.DataFrame(doc["state"]["placemarks"])

            parked = df[["name", "coordinates"]]
            cars_status.loc[parked["name"].values, doc["timestamp"]] = "parked"
            
            cars_lat.loc[parked["name"].values, doc["timestamp"]] = \
                pd.Series(data=[v[0] for v in parked["coordinates"].values],
                          index=parked["name"].values)
                
            cars_lon.loc[parked["name"].values, doc["timestamp"]] = \
                pd.Series(data=[v[1] for v in parked["coordinates"].values],
                          index=parked["name"].values)
            
            booked = self.fleet.difference(df["name"])
            cars_status.loc[booked.values, doc["timestamp"]] = "booked"
        
        for doc in self.cursor:
            update_cars_status()
            
        cars_status = cars_status.T
        cars_lat = cars_lat.T
        cars_lon = cars_lon.T

        global_status = {}

        for car in cars_status:

            car_status = cars_status[car]
            car_status = car_status.loc[car_status.shift(1) != car_status]

            car_lats = cars_lat[car]
            car_lats = car_lats.loc[car_status.index]

            car_lons = cars_lon[car]
            car_lons = car_lons.loc[car_status.index]
                                
            car_df = pd.DataFrame()
            car_df["status"] = car_status.values
            car_df["start"] = car_status.index
            car_df["lat"] = car_lats.values
            car_df["lon"] = car_lons.values
            car_df["start_lat"] = car_df["lat"].shift(1)
            car_df["start_lon"] = car_df["lon"].shift(1)
            car_df["end_lat"] = car_df["lat"].shift(-1)
            car_df["end_lon"] = car_df["lon"].shift(-1)
            
            car_df["end"] = car_df["start"].shift(-1)
            car_df.loc[:,"end"].iloc[-1] = self.end

            global_status[car] = car_df

            parks = car_df[car_df.status == "parked"]
            
            parks = parks.dropna(axis=1, how="all")
            parks = parks.drop("status", axis=1)
            
            for park in parks.T.to_dict().values():
                park["provider"] = self.name
                park["city"] = self.city
                dbp.insert_park_v2(self.city, park)
                
        return cars_status, global_status
            
def test():

    car2go = Car2Go()

    end = datetime.datetime(2016, 12, 10, 0, 0, 0)
    start = end - datetime.timedelta(days = 1)
    
    car2go.select_data("torino","timestamp", start, end)    
    car2go.get_fields()
    car2go.get_fleet()
    
#    for car in list(car2go.fleet):
#        car2go.get_parks(car)

    t = car2go.get_parks_v2()

    return car2go, t

car2go, t = test()

