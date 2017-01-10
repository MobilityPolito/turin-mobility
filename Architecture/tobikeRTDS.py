import threading
import logging
import requests
import datetime
import time
import json
import re

import pandas as pd

from DataSource import RTDS
from DataBaseProxy import dbp

stop_tobike = False

class TObikeRTDS(RTDS):
    
     def __init__ (self,city):
        threading.Thread.__init__(self)        
        self.name = "tobike"
        self.log_filename = "tobike.log"
        logging.basicConfig(filename=self.log_filename, level=logging.DEBUG)        
        
        self.city = city
        self.url_home = "http://www.tobike.it/frmLeStazioni.aspx"
        
     def log_message  (self, scope, status):
        
        return '[{}] -> {} {}: {} {}'\
                    .format(datetime.datetime.now(),\
                            self.name,\
                            self.city,\
                            scope,\
                            status)  
     def start_session (self):
        
        try:
            self.session = requests.get(self.url_home)
            self.session.raise_for_status()
            self.session_start_time = datetime.datetime.now()
            message = self.log_message("session","success")
        except:
            message = self.log_message("session","error")
        logging.debug(message)
        
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
        
     def get_feed(self):
        if (datetime.datetime.now() - self.session_start_time).total_seconds() > 2400:
            self.session = self.session.close()
            self.start_session()
            self.session_start_time = datetime.datetime.now()  
         
        #REGEX expression to scrape the data
        try:
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
            feed=[]
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
                feed.insert(i,d)
                d={}
            message = self.log_message("feed","success")
        except:
            feed = []
            message = self.log_message("feed","error")
        logging.debug(message)
#        print json.dumps(feed)
        return feed
        
     def check_feed(self):
        last_feed_df = pd.DataFrame(self.last_feed)
        current_feed_df = pd.DataFrame(self.current_feed)
        print last_feed_df.equals(current_feed_df)
        
        print current_feed_df.index
        print current_feed_df.columns
        
        for col in current_feed_df.columns:
            s = current_feed_df[col]
            print str(s.dtype)
        
     def to_DB(self):
        dbp.insert(self.name, self.city, self.current_feed)
    
     def run(self):    
        self.start_session()
        self.last_feed = self.get_feed()

        while stop_tobike is False:
            self.current_feed = self.get_feed()
            self.check_feed()
            self.to_DB()
            self.last_feed = self.current_feed
            time.sleep(60)
        else:
            return

tobikeRTDS = TObikeRTDS("torino")
tobikeRTDS.run()