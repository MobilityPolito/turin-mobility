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
            start, end = args
            self.cursor = dbp.query_raw_by_time(self.name, city, start, end)

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
        return self.fleet

    def get_parks(self, car_plate):

        def get_car_status (doc):
            df = pd.DataFrame(doc["state"]["placemarks"])
            car = df[df["name"] == car_plate]
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
                df = pd.DataFrame(doc["state"]["placemarks"])
                car_state = df[df["name"] == car_plate]
                park_lat = list(car_state["coordinates"].values)[0][1]
                park_lon = list(car_state["coordinates"].values)[0][0]
            except:
                print df.describe()
        elif last_car_status == "booked":
            try:
                book_start = doc["timestamp"]
                df = pd.DataFrame(doc["state"]["placemarks"])
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

                        df = pd.DataFrame(doc["state"]["placemarks"])
                        park_lat = list(df[df["name"] == car_plate]["coordinates"].values)[0][1]
                        park_lon = list(df[df["name"] == car_plate]["coordinates"].values)[0][0]
                        park_start = doc["timestamp"]

                        book_lat_end = park_lat
                        book_lon_end = park_lon
                        book_end = doc["timestamp"]
                        dbp.insert_book(self.name, 
                                        self.city, 
                                        car_plate, 
                                        book_lat_start, book_lon_start, 
                                        book_lat_end, book_lon_end,
                                        book_start, book_end)                                                
                    
            except:
                print doc["_id"]

def test():

    car2go = Car2Go()

    end = datetime.datetime(2016, 11, 25, 0, 0, 0)
    start = end - datetime.timedelta(days = 1)
    
    car2go.select_data("torino","timestamp", start, end)    
    car2go.get_fields()
    car2go.get_fleet()
    
    for car in list(car2go.fleet):
        car2go.get_parks(car)

    return car2go

car2go = test()