#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 17:08:26 2016

@author: Flavia
"""

import threading
import logging
import requests
import datetime
import time
import json

import pandas as pd

from DataSource import RTDS
from DataBaseProxy import dbp

stop_car2go = False

class Car2GoRTDS(RTDS):
        
    def __init__ (self,city):
        threading.Thread.__init__(self)        
        self.name = "car2go"
        self.log_filename = "car2go.log"
        logging.basicConfig(filename=self.log_filename, level=logging.DEBUG)        
        
        self.city = city
        self.url_home = 'https://www.car2go.com/api/v2.1/vehicles?oauth_consumer_key=polito&format=json&loc=' + self.city

    
    def log_message  (self, scope, status):
        
        return '[{}] -> {} {}: {} {}'\
                    .format(datetime.datetime.now(),\
                            self.name,\
                            self.city,\
                            scope,\
                            status)  
                    
    
    def start_session (self):
        
        try:
            self.session = requests.Session()
            self.session.get(self.url_home)
            self.session_start_time = datetime.datetime.now()
            message = self.log_message("session","success")
        except:
            message = self.log_message("session","error")
        logging.debug(message)
        

    def get_feed(self):
        
        if (datetime.datetime.now() - self.session_start_time).total_seconds() > 2400:
            self.session = self.session.close()
            self.start_session()
            self.session_start_time = datetime.datetime.now()            
        
        try:
            feed = json.loads(self.session.get(self.url_home).text)
            message = self.log_message("feed","success")
        except:
            feed = {}
            message = self.log_message("feed","error")
        logging.debug(message)

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
#            if str(s.dtype) != "object":
#                print s.describe()


    def to_DB(self):
        
        dbp.insert(self.name, self.city, self.current_feed)
        
    
    def run(self):

        print threading.current_thread()
    
        self.start_session()
        
        self.last_feed = self.get_feed()
        
        while stop_car2go is False:
            self.current_feed = self.get_feed()
            self.check_feed()
            self.to_DB()
            self.last_feed = self.current_feed
            time.sleep(10)
        else:
            return
