import threading

import random

import datetime
import time

import requests
from pymongo import MongoClient
import json


MONGO_HOME = 'mongodb://localhost:27017/'
DB_NAME = 'CSMS'

client = MongoClient(MONGO_HOME)
db = client.CSMS
db.authenticate('csms', '1234')

def write_log (message):
    with open("log.log", "a+") as f:
        timestamp = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        f.write("[" + timestamp + "] -> " + message + "\n")

def DBinsert (session, provider, city, current_state):

    collection = db[city]
    record = {\
         "timestamp": datetime.datetime.now(),\
         "provider": provider,\
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
        self.start_time = datetime.datetime.now()
        
    def start_session(self, url):
        self.session = requests.Session()
        self.session.get(url)
        write_log(self.provider + " " + self.city + ": session successfully started")        
        
    def get_state (self):
        
        if self.provider in ["enjoy"]:
        
            if (datetime.datetime.now() - self.start_time).total_seconds() > 30:
                self.start_time = datetime.datetime.now()
                self.session = self.session.close()
                self.url_home = 'https://enjoy.eni.com/it/' + self.city + '/map/'
                self.start_session(self.url_home)

            request = self.session.get(self.url_data)
            current_state = json.loads(request.text)
            self.last_state = current_state
        
        if self.provider in ["car2go"]:
            request = self.session.get(self.url)
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
                self.url = 'https://www.car2go.com/api/v2.1/vehicles?oauth_consumer_key=polito&format=json&loc=' + self.city
                self.start_session(self.url)
            elif self.provider == "tobike":
                self.toBike = pybikes.get('to-bike')
                self.toBike.update()
        except:
            print "Session error!"
            
        while(True):
        
            try:
                self.get_state()
                write_log(self.provider + " " + self.city + ": state successfully loaded")
            except:
                write_log(self.provider + " " + self.city + ": HTTP error!")
                
            try:
                DBinsert(self.session, self.provider, self.city, self.last_state)
                write_log(self.provider + " " + self.city + ": state successfully inserted")                
            except:
                write_log(self.provider + " " + self.city + ": Database error!")

            try:
                with open (self.city + "_last_state.json", "w+") as outfile:
                    outfile.write(json.dumps(self.last_state))
                write_log(self.provider + " " + self.city + ": state successfully written")                    
            except:
                write_log(self.provider + " " + self.city + ": File write error!")
                
            time.sleep(60 + random.randint(-30,30))
                
if __name__ == "__main__":
        
    # enjoy_cities = ['torino']
               
    car2go_cities = ['torino']
                   
    # bike_cities = ['torino']
    
    # for city in enjoy_cities:
    #     print "starting thread enjoy for:", city
    #     thread = CityThread("enjoy", city)
    #     thread.start()
        
    for city in car2go_cities:
        print "starting thread car2go for:", city
        thread = CityThread("car2go", city)
        thread.start()

    #for city in bike_cities:
    #    print city
    #    thread = CityThread("tobike", city)
    #    thread.start()
        
    thread.join()