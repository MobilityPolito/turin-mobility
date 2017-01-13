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

        print "Acquiring fleet ..."
        
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

    def get_parks_and_books_v2 (self):
        
        self.cursor.rewind()
        doc = self.cursor.next()

        cars_status = pd.DataFrame(index = self.fleet.values)
        cars_lat = pd.DataFrame(index = self.fleet.values)
        cars_lon = pd.DataFrame(index = self.fleet.values)
        cars_fuel = pd.DataFrame(index = self.fleet.values)
        
        def update_cars_status ():

            df = pd.DataFrame(doc["state"]["placemarks"])

            parked = df[["name", "coordinates"]]
            booked = self.fleet.difference(df["name"])

            cars_status.loc[parked["name"].values, doc["timestamp"]] = \
                "parked"
            cars_status.loc[booked.values, doc["timestamp"]] = \
                "booked"

            cars_lat.loc[parked["name"].values, doc["timestamp"]] = \
                pd.Series(data=[v[1] for v in parked["coordinates"].values],
                          index=parked["name"].values)
            cars_lon.loc[parked["name"].values, doc["timestamp"]] = \
                pd.Series(data=[v[0] for v in parked["coordinates"].values],
                          index=parked["name"].values)
            cars_fuel.loc[parked["name"].values, doc["timestamp"]] = \
                pd.Series(data=df["fuel"].values,
                          index=parked["name"].values)
        
        for doc in self.cursor:
            update_cars_status()
            
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
                    park["provider"] = self.name
                    park["city"] = self.city
                    dbp.insert_park_v2(self.city, park)

            books = car_df[car_df.status == "booked"]
            if len(books):
                books = books.dropna(axis=1, how="all")
                books = books.drop("status", axis=1)

#                if car_df.ix[car_df.head(1).index,"status"] == "booked":
#                    books = books.drop(books.head(1).index)
#                if car_df.ix[car_df.tail(1).index,"status"] == "booked":
#                    books = books.drop(books.tail(1).index)
                
                for book in books.T.to_dict().values():
                    book["provider"] = self.name
                    book["city"] = self.city
                    dbp.insert_book_v2(self.city, book)            
                
        return cars_status, cars


