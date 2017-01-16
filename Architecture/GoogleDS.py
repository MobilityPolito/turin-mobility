#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 09:15:02 2017

@author: Flavia
"""

import googlemaps
import datetime
import logging

import time

import pandas as pd
from DataSource import RTDS
from DataBaseProxy import DataBaseProxy


class GoogleDS(RTDS):
        
    def __init__ (self, provider, city, by, *args):
        if by == "timestamp" and len(args) == 2:
            self.start, self.end = args     
        self.provider = provider
        self.city = city
        self.log_filename = self.provider + "_google.log"
        logging.basicConfig(filename=self.log_filename, level=logging.DEBUG)        
        self.keys = pd.Series(['AIzaSyD3PdBLQxWMDsaJ1tdHOs02QNBuIEqLSiQ', 'AIzaSyBnUsB3u6Blg23D5uqIQPnM_1Pawkp5VLY', 'AIzaSyBaaQQyMnT7MUI421WdO67g66igzXL2O4A'])

    def log_message(self, scope, status):
        return '[{}] -> {} {}: {} {}'\
                    .format(datetime.datetime.now(),\
                            self.provider,\
                            self.city,\
                            scope,\
                            status)  
    
    def start_session (self):
        try:
            self.gmaps = googlemaps.Client(key='AIzaSyD3PdBLQxWMDsaJ1tdHOs02QNBuIEqLSiQ')
            self.session_start_time = datetime.datetime.now()
            message = self.log_message("session","success")
        except:
            message = self.log_message("session","error")
        logging.debug(message)
        
    def get_feed(self):
        
        def next_weekday(now, rental_time):
            days_ahead = rental_time.weekday() - now.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            nextday = now + datetime.timedelta(days_ahead)
            return nextday.replace(hour = rental_time.hour, 
                                   minute = rental_time.minute, 
                                   second = rental_time.second)

        books_df = self.dbp.get_books(self.provider, self.city, self.start, self.end)
        
        for row in books_df.iterrows:
            google_day = next_weekday(datetime.datetime.now(), row['start'])
            directions_result = self.gmaps.directions([row['start_lat'], row['start_lon']], 
                                                      [row['end_lat'], row['end_lon']], 
                                                      mode="transit", 
                                                      departure_time = google_day)
            try:
                feed = {'provider': self.provider,
                        'car' : row['car_id'],
                        'start_lat':row['start_lat'],
                        'start_lon' :row['start_lon'],
                        'end_lat' :row['end_lat'], 
                        'end_lon': row['end_lon'],
                        'departure_time': directions_result[0]["legs"][0]["departure_time"]["value"],
                        'arrival_time': directions_result[0]["legs"][0]["arrival_time"]["value"],
                        'distance': directions_result[0]["legs"][0]["distance"]["value"],
                        'duration': directions_result[0]["legs"][0]["duration"]["value"],
                        'fare': directions_result[0]["fare"]["value"]
                        }
                self.to_DB(self.provider, self.city, feed)
                message = self.log_message("feed","success")
            except:
                feed = {}
                message = self.log_message("feed","error")
            logging.debug(message)
            return feed        
    
    def check_feed(self):
        """
        Check data stream correctness and consistency
        """
        pass

    def to_DB(self):
        
        self.dbp.insert_direction_transit(self.provider, self.city, self.current_feed)
         
    def run(self):
        self.dbp = DataBaseProxy()

        self.start_session()
        self.get_feed()

        time.sleep(5)

end = datetime.datetime(2016, 12, 10, 0, 0, 0)
start = end - datetime.timedelta(days = 1)
googlecar2go = GoogleDS('car2go', 'torino', 'timestamp', start, end)
googlecar2go.run()