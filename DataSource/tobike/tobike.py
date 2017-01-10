import requests
from pymongo import MongoClient

import datetime
import time

import re
import json


MONGO_HOME = 'mongodb://localhost:27017/'
DB_NAME = 'CSMS'
LOG_PATH = "/home/mc/Scrivania/tobike/"
tobike_url = "http://www.tobike.it/frmLeStazioni.aspx"

client = MongoClient(MONGO_HOME)
db = client.CSMS
#db.authenticate('csms', '1234')

client = MongoClient(MONGO_HOME)
db = client[DB_NAME]


def write_log (message):
    with open(LOG_PATH+"tobike.log", "a+") as f:
        timestamp = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        f.write("[" + timestamp + "] -> " + message + "\n")

        
def DB_insert(provider,city, current_state):
    collection = db[city]
    record = {
         "timestamp": str(datetime.datetime.now()),
         "provider": provider,
         "city" : city,
         "state": current_state
         }
#    with open("tobike.log", "a+") as f:
#         f.write(json.dumps(record) + "\n")
     
##    return record
    try:
        collection.insert_one(record)
        write_log(TB.provider + " " + TB.city + ": record inserted")
    except:
        write_log(TB.provider + " " + TB.city + ": Invalid data coding!")
        
class TObike():
    
    def __init__(self,provider,city):
        self.provider = provider
        self.city = city
        self.last_state = None
        self.session= None
        self.obj = None
    
    #class counting the bikes' status for station 
    def tobike_bikes(self,bikes):
        assert len(bikes) == 30
    
        empty_places = bikes.count('0')
        available_bikes =  bikes.count('4')
        broken_bikes = bikes.count('1') + bikes.count('5')
        filler = bikes.count('x')
    
        assert empty_places + available_bikes + broken_bikes + filler == 30
    
        return {
            'empty_places': empty_places,
            'available_bikes': available_bikes,
            'broken_bikes': broken_bikes,
        }
        
    def get_session(self,url):
        try:
            self.session = requests.get(url)
            self.session.raise_for_status()
            write_log(self.provider + " " + self.city + ": session successfully started")
        except requests.exceptions.RequestException as err:  # This is the correct syntax
            write_log(TB.provider + " " + TB.city + ": HTTP error:("+str(err)+")")
                
    def get_data(self):
        #REGEX expression to scrape the data
        RE = r"{RefreshMap\((?P<data>.*)\)}"
        result = re.search(RE, self.session.text, re.UNICODE).group("data")
        
        row = result.split("','")
    
        ids = row[0].split("|")
        num_votes = row[1].split("|")
        votes = row[2].split("|")
        lats = row[3].split("|")
        lngs = row[4].split("|")
        names = row[5].split("|")
        bikes = row[6].split("|")
        addresses = row[7].split("|")
        statuses = row[8].split("|")
    
        num_points = len(ids)
        assert num_points == len(num_votes)
        assert num_points == len(votes)
        assert num_points == len(lats)
        assert num_points == len(lngs)
        assert num_points == len(names)
        assert num_points == len(bikes)
        assert num_points == len(addresses)
        assert num_points == len(statuses)
    
        string = ids[0].split("'")
        ids[0] = string[1]
        l=[]
        d={}
        #print "++++"+ids[0]
        for i in range (num_points) :
            d["id"]=ids[i]
            d["num_votes"]=num_votes[i]
            d["votes"]=votes[i]
            d["lat"]=lats[i]
            d["lng"]=lngs[i]
            d["name"]=names[i]
            d["bikes"]=self.tobike_bikes(bikes[i])
            d["address"]=addresses[i]
            d["status"]=statuses[i]
            l.insert(i,d)
            d={}
        
        return json.dumps(l)
        
    def close_connection(self):
        self.session.close()

if __name__ == "__main__":
    TB = TObike("tobike","torino")
    f=True
    while (f):
        try:
            TB.get_session(tobike_url)
            current_state = TB.get_data()
            DB_insert(TB.provider,TB.city,current_state)
            write_log(TB.provider + " " + TB.city + ": state successfully loaded\n")
            print "Data taken. "
        except:
            write_log(TB.provider + " " + TB.city + ": any operation has been done!\n")

        #f=False
        time.sleep(60)
    print "Scrarper terminated."
#    f.close()
#    f= open("/home/mc/Scrivania/tobike/tobike.log","r")
#    s = f.read()
#    readRecord = json.loads(s)
#    listOfBikes = json.loads(readRecord["state"])