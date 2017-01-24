import datetime
import pandas as pd

from ServiceProvider import ServiceProvider

from DataBaseProxy import DataBaseProxy
dbp = DataBaseProxy()
            
class Enjoy(ServiceProvider):
    
    def __init__ (self):
        self.name = "enjoy"
        self.city = "torino"
    
    def select_data (self, city, by, *args):
        
        if by == "timestamp" and len(args) == 2:
            self.start, self.end = args
            self.cursor = dbp.query_raw_by_time(self.name, self.city, self.start, self.end)

        if by == "full":
            self.cursor = dbp.query_raw(self.city, self.name)

        print "Data selected!"
            
        
    def get_fields(self):
        
        doc = self.cursor.next()
        return list(pd.DataFrame(doc["state"]).columns)
        
    def get_fleet(self):

        print "Acquiring fleet ..."

        self.cursor.rewind()        
        doc = self.cursor.next()
        current_fleet = pd.Index(pd.DataFrame(doc["state"])\
                                 .loc[:, "car_plate"].values)
        self.fleet = current_fleet
        for doc in self.cursor:
            current_fleet = pd.Index(pd.DataFrame(doc["state"])\
                                     .loc[:, "car_plate"].values)
            self.fleet = self.fleet.union(current_fleet)
            
        print "Fleet acquired!"
            
        return self.fleet

    def get_fleet_from_db (self):
        
        print "Acquiring fleet ..."
        query = dbp.query_fleet(self.name, self.city)
        self.fleet = pd.Index(query.next()['fleet'])
        print "Fleet acquired!"
        return self.fleet

    def update_cars_status (self, doc, cars_status, cars_lat, cars_lon, cars_fuel):
        
        df = pd.DataFrame(doc["state"])

        parked = df[["car_plate", "lat", "lon", "fuel_level"]]
        booked = self.fleet.difference(df["car_plate"])

        cars_status.loc[parked["car_plate"].values, doc["timestamp"]] = \
            "parked"            
        cars_status.loc[booked.values, doc["timestamp"]] = \
            "booked"

        cars_lat.loc[parked["car_plate"].values, doc["timestamp"]] = \
            pd.Series(data=df["lat"].values,
                      index=parked["car_plate"].values)                
        cars_lon.loc[parked["car_plate"].values, doc["timestamp"]] = \
            pd.Series(data=df["lon"].values,
                      index=parked["car_plate"].values)            
        cars_fuel.loc[parked["car_plate"].values, doc["timestamp"]] = \
            pd.Series(data=df["fuel_level"].values,
                      index=parked["car_plate"].values)        
        
    def get_parks_and_books (self):
        
        self.cursor.rewind()
        doc = self.cursor.next()

        cars_status = pd.DataFrame(index = self.fleet.values)
        cars_lat = pd.DataFrame(index = self.fleet.values)
        cars_lon = pd.DataFrame(index = self.fleet.values)
        cars_fuel = pd.DataFrame(index = self.fleet.values)
                
        for doc in self.cursor:
            self.update_cars_status(doc, cars_status, cars_lat, cars_lon, cars_fuel)
            
        cars_status = cars_status.T
        cars_lat = cars_lat.T
        cars_lon = cars_lon.T
        cars_fuel = cars_fuel.T

        cars = {}

        for car in cars_status:
            
            print car

            car_status = cars_status[car]
            car_status = car_status.loc[car_status.shift(1) != car_status]

            car_lats = cars_lat[car]
            car_lats = car_lats.loc[car_status.index]

            car_lons = cars_lon[car]
            car_lons = car_lons.loc[car_status.index]

            car_fuels = cars_fuel[car]
            car_fuels = car_fuels.loc[car_status.index]
                                
            car_df = pd.DataFrame()
            car_df["status"] = car_status.values
            car_df["start"] = car_status.index
            car_df["lat"] = car_lats.values
            car_df["lon"] = car_lons.values
            car_df["fuel"] = car_fuels.values
            car_df["start_lat"] = car_df["lat"].shift(1)
            car_df["start_lon"] = car_df["lon"].shift(1)
            car_df["end_lat"] = car_df["lat"].shift(-1)
            car_df["end_lon"] = car_df["lon"].shift(-1)
            car_df["start_fuel"] = car_df["fuel"].shift(1)
            car_df["end_fuel"] = car_df["fuel"].shift(-1)
            car_df["end"] = car_df["start"].shift(-1)
            car_df.loc[:,"end"].iloc[-1] = self.end

            cars[car] = car_df

            parks = car_df[car_df.status == "parked"]
            if len(parks):
                parks = parks.dropna(axis=1, how="all")
                parks = parks.drop("status", axis=1)
                for park in parks.T.to_dict().values():
                    park["plate"] = car
                    park["provider"] = self.name
                    park["city"] = self.city
                    dbp.insert_park(self.name, self.city, park)

            books = car_df[car_df.status == "booked"]
            if len(books):
                books = books.dropna(axis=1, how="all")
                books = books.drop("status", axis=1)                
                for book in books.T.to_dict().values():
                    book["plate"] = car
                    book["provider"] = self.name
                    book["city"] = self.city
                    dbp.insert_book(self.name, self.city, book)            
                
        return cars_status, cars