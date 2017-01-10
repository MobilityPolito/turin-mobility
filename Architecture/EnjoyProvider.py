import datetime

import pandas as pd

import geopy

from Provider import Provider

from DataBaseProxy import DataBaseProxy
dbp = DataBaseProxy()
            
class Enjoy(Provider):
    
    def __init__ (self, city):
        self.name = "enjoy"
        self.city = city
    
    def select_data (self, city, by, *args):
        
        if by == "timestamp" and len(args) == 2:
            start, end = args
            self.cursor = dbp.query_raw_by_time(self.name, city, start, end)
#            print self.cursor.count()
        return self.cursor
        
    def get_fields(self):
        
        self.cursor.rewind()
        
        sample_columns = pd.DataFrame(self.cursor.next()["state"]).columns  

        for doc in self.cursor:
            columns = pd.DataFrame(doc["state"]).columns
            if len(columns.difference(sample_columns)):
                print "Warning: different fields for the same provider"
            
        self.fields = columns
        return self.fields
        
    def get_fleet(self):

        self.cursor.rewind()        
        doc = self.cursor.next()
        current_fleet = pd.Index(pd.DataFrame(doc["state"])\
                                 .loc[:, "car_plate"].values)
        self.fleet = current_fleet
        for doc in self.cursor:
            current_fleet = pd.Index(pd.DataFrame(doc["state"])\
                                     .loc[:, "car_plate"].values)
            self.fleet = self.fleet.union(current_fleet)
        return self.fleet
        
    def get_parks(self, car_plate):

        def get_car_status (doc):
            df = pd.DataFrame(doc["state"])
            car = df[df["car_plate"] == car_plate]
            if len(car):
                return "parked"
            else:
                return "booked"
        
        self.cursor.rewind()
        doc = self.cursor.next()
        
        last_car_status = get_car_status(doc)
        
        if last_car_status == "parked":
            try:
                park_start = doc["timestamp"]
                df = pd.DataFrame(doc["state"])
                car_state = df[df["car_plate"] == car_plate]
                park_lat = float(car_state["lat"].values)
                park_lon = float(car_state["lon"].values)
            except:
                print df.describe()
        elif last_car_status == "booked":
            try:
                book_start = doc["timestamp"]
                df = pd.DataFrame(doc["state"])
                book_lat_start = 45.116
                book_lon_start = 7.742
            except:
                print df.describe()

        for doc in self.cursor:
            
            try:
                
                current_car_status = get_car_status(doc)
                
                if last_car_status == "parked":
                    
                    if current_car_status == "parked":
                        pass
                    
                    elif current_car_status == "booked":
                        
                        park_end = doc["timestamp"]
                        dbp.insert_park(self.name, 
                                        self.city, 
                                        car_plate, 
                                        park_lat, park_lon, 
                                        park_start, park_end)
                        
                        book_start = park_end
                        book_lat_start = park_lat
                        book_lon_start = park_lon                        
                        
                        last_car_status = current_car_status
                            
                elif last_car_status == "booked":

                    if current_car_status == "booked":
                        pass
                    
                    elif current_car_status == "parked":

                        last_car_status = current_car_status

                        df = pd.DataFrame(doc["state"])
                        park_lat = float(df[df["car_plate"] == car_plate]["lat"].values)
                        park_lon = float(df[df["car_plate"] == car_plate]["lon"].values)
                        park_start = doc["timestamp"]

                        book_lat_end = park_lat
                        book_lon_end = park_lon
                        book_end = doc["timestamp"]

                        bill = self.get_price(book_start, book_end)
                        dbp.insert_book(self.name, 
                                        self.city, 
                                        car_plate, 
                                        book_lat_start, book_lon_start, 
                                        book_lat_end, book_lon_end,
                                        book_start, book_end,
                                        bill)     
                                            
            except:
                print doc["_id"]

    def get_price(self, start, end):
        #calcolato solo sul tempo, dovrebbe essere fatto anche sui chilometri
        price = 0.25
        m = int((end-start).total_seconds()/60)
        return float(m*price)
        
    def get_emissions(self, book_lat_start, book_lon_start, book_lat_end, book_lon_end):
        emission = 119
        
        

def test():
    
    enjoy = Enjoy("torino")  
    end = datetime.datetime(2016, 12, 10, 23, 59, 0)
    start = end - datetime.timedelta(minutes= 10)
       
    enjoy.select_data("torino","timestamp", start, end)    
    enjoy.get_fields()
    enjoy.get_fleet()
    
    for car in list(enjoy.fleet):
        enjoy.get_parks(car)
        
    return enjoy
    print enjoy.get_price(start,end)
    
enjoy = test()

