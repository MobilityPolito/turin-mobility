import threading

import requests
from pymongo import MongoClient

import json

import datetime
import time

import pybikes

MONGO_HOME = 'mongodb://localhost:27017/'
DB_NAME = 'MobilityDataLake'

client = MongoClient(MONGO_HOME)
db = client[DB_NAME]

def write_log (message):
    with open("enjoy.log", "a+") as f:
        timestamp = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        f.write("[" + timestamp + "] -> " + message + "\n")

def DBinsert (provider, city, current_state):

    collection = db[city]
    record = {\
         "timestamp": datetime.datetime.now(),\
         "provider": "enjoy",\
         "state": current_state\
         }
     
    try:
        collection.insert_one(record)
    except:
        print "Invalid data coding!"
        
class CityThread (threading.Thread):
    
    def __init__(self, provider, city):

        threading.Thread.__init__(self)
        self.provider = provider
        self.city = city
        self.last_state = None
        
    def start_session(self, url):
        self.session = requests.Session()
        self.session.get(url)
        #session.post(URL_COOKIE, data=json.dumps(self.city))
        write_log(self.provider + " " + self.city + ": session successfully started")        

    def get_data (self):
        if self.provider in ["enjoy","car2go"]:
            request = self.session.get(self.url_data)
            current_state = json.loads(request.text)
            self.last_state = current_state
        elif self.provider in ["tobike"]:
            self.toBike = pybikes.get('to-bike')
            self.toBike.update()            
            l = {}
            stations_dict={}
            for i in range(len(self.toBike.stations)):
                l["name"] = self.toBike.stations[i].name
                l["extra"] = self.toBike.stations[i].extra
                l["timestamp"] = str(self.toBike.stations[i].timestamp)
                l["free"] = self.toBike.stations[i].free
                l["bikes"] = self.toBike.stations[i].bikes
                l["longitude"] = self.toBike.stations[i].longitude
                l["latitude"] = self.toBike.stations[i].latitude
                stations_dict[i] = l
                l={}
            self.last_state = json.dumps(stations_dict)

    def run(self):
        
        print threading.current_thread()
    
        try:
            if self.provider == "enjoy":
                self.url_home = 'https://enjoy.eni.com/it/' + self.city + '/map/'
                self.start_session(self.url_home)
                self.url_data = 'https://enjoy.eni.com/ajax/retrieve_vehicles'
            elif self.provider == "car2go":
                self.url = 'https://www.car2go.com/api/v2.1/vehicles?oauth_consumer_key=car2gowebsite&format=json&loc='\
                    + self.city
                self.start_session(self.url)
            elif self.provider == "tobike":
                self.toBike = pybikes.get('to-bike')
                self.toBike.update()
        except:
            print "Session error!"
            
        while(True):
        
            try:
                self.get_data()
                write_log(self.provider + " " + self.city + ": state successfully loaded")
            except:
                write_log(self.provider + " " + self.city + ": HTTP error!")
                
            try:
                DBinsert(self.city, self.last_state)
                write_log(self.provider + " " + self.city + ": state successfully inserted")                
            except:
                write_log(self.provider + " " + self.city + ": Database error!")

            try:
                with open (self.city + "_last_state.json", "w+") as outfile:
                    outfile.write(json.dumps(self.last_state))
                write_log(self.provider + " " + self.city + ": state successfully written")                    
            except:
                write_log(self.provider + " " + self.city + ": File write error!")
                
            time.sleep(300)
                
if __name__ == "__main__":
        
    enjoy_cities = ['torino',\
                   'milano',\
                   'catania',\
                   'roma',\
                   'firenze']
               
    car2go_cities = ['torino',\
                   'milano',\
                   'newyorkcity',\
                   'roma',\
                   'firenze']
                   
    bike_cities = ['torino']
    
    for city in enjoy_cities:
        print city
        thread = CityThread("enjoy", city)
        thread.start()
        
    for city in car2go_cities:
        print city
        thread = CityThread("car2go", city)
        thread.start()

    for city in bike_cities:
        print city
        thread = CityThread("tobike", city)
        thread.start()
        
    thread.join()
