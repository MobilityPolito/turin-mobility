#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 09:15:02 2017

@author: Flavia
"""

import time
import datetime
import logging
import urllib2

import pandas as pd

import googlemaps

from DataSource import RTDS
from chiavi_df import series_keys
from DataBaseProxy import DataBaseProxy
dbp = DataBaseProxy()

class GoogleDS(RTDS):
        
    def __init__ (self, provider, city, by, *args):
        
        if by == "timestamp" and len(args) == 2:
            self.start, self.end = args     
        
        self.provider = provider
        self.city = city
        self.log_filename = self.provider + "_google.log"
        logging.basicConfig(filename=self.log_filename, level=logging.DEBUG)   
#        self.keys = series_keys
        self.keys = pd.Series([
                        'AIzaSyD3PdBLQxWMDsaJ1tdHOs02QNBuIEqLSiQ', 
                        'AIzaSyBnUsB3u6Blg23D5uqIQPnM_1Pawkp5VLY', 
                        'AIzaSyBaaQQyMnT7MUI421WdO67g66igzXL2O4A',
                        'AIzaSyDbPG5qS-g0pROiPRcOT2G-keWi54ie2-M',
                        'AIzaSyCjy-sVWBCyN9FOjBeNg2_OeULs-uXSmMI',
                        'AIzaSyAUrnCmaEs7e7izfCiKYm-k7Ap0EwZzYes',
                        'AIzaSyCeT4Z_Cfabvpnh2FBbf3TCrhBNtwlfVwU',
                        'AIzaSyAcPVep5aXJLbuBDV7Qn_JaWSpD4o6s30w',
                        'AIzaSyBHz8SA5BKIJDOu9mtLJb5JilGvcLnGIiM',
                        'AIzaSyBqMJcxNQUmciUN8qsI-4JVO9Hh_EJqNfE',
                        'AIzaSyB9XupnKFaH-zuVg_lBlz7NO8q6QpWFKZk',
                        'AIzaSyAVpeQaUjVPZznjp1b1sbtUl2iBzHSuGek',
                        'AIzaSyCoFpO5q5MatCal_1lLaxVCr6LcXePo91M',
                        'AIzaSyCGfLn4VqFrbV1PFc6duXi7ojPktJb-ta4',
                        'AIzaSyA6zgFdORCnKRnpp74Ew925aCwbSmzsM9U',
                        'AIzaSyBSjjou5aXnl-9L3SIaJR05Vc3Zb8j0WpY',
                        'AIzaSyAKaQDrgawidGlRNkjqTIMngFZs7pOV8Zc',
                        'AIzaSyCnksllWfpV0D3iDBomyKRFUkqEvEoNtKg',
                        'AIzaSyB0ggpBGN6wRpsA1cdfAgO2iVtSt6Nj41I'
                    ])

        self.current_key = 0
        self.start_session()
        
    def log_message(self, scope, status):
        return '[{}] -> {} {}: {} {}'\
                    .format(datetime.datetime.now(),\
                            self.provider,\
                            self.city,\
                            scope,\
                            status)  
    
    def start_session (self):
        try:
            self.gmaps = googlemaps.Client(key=self.keys.iloc[self.current_key])
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
            
        def change_key(self):
            self.current_key = (self.current_key + 1)  % len(self.keys)
            self.gmaps = googlemaps.Client(key=self.keys.iloc[self.current_key])
            
        books_df = dbp.get_books(self.provider, self.city, self.start, self.end)
        
        for i in range(len(books_df)):
            print i 

            row = books_df.iloc[i]
            google_day = next_weekday(datetime.datetime.now(), row['start'])
            
            try:
                directions_result = self.gmaps.directions([row['start_lat'], row['start_lon']], 
                                                          [row['end_lat'], row['end_lon']], 
                                                          mode="transit", 
                                                          departure_time = google_day)
                time.sleep(5)
                
            except urllib2.HTTPError, err:
                if err.resp.status in [403]: # key limits exceeded
                    change_key()
                    directions_result = self.gmaps.directions([row['start_lat'], row['start_lon']], 
                                                              [row['end_lat'], row['end_lon']], 
                                                              mode="transit", 
                                                              departure_time = google_day)
                    time.sleep(5)

                else: 
                    print "Error in retrieving transit information"
                    
            try:
                directions_result_driving = self.gmaps.directions([row['start_lat'], row['start_lon']], 
                                                              [row['end_lat'], row['end_lon']], 
                                                              departure_time = google_day)
                time.sleep(5)

            except urllib2.HTTPError, err:
                if err.resp.status in [403]: # key limits exceeded
                    change_key()
                    directions_result = self.gmaps.directions([row['start_lat'], row['start_lon']], 
                                                              [row['end_lat'], row['end_lon']], 
                                                              departure_time = google_day)
                    time.sleep(5)

                else: 
                    print "Error in retrieving driving information"
                    
            departure_time = datetime.datetime.utcfromtimestamp\
                (directions_result[0]["legs"][0]["departure_time"]["value"])\
                + datetime.timedelta(hours = 1)
            arrival_time = datetime.datetime.utcfromtimestamp\
                (directions_result[0]["legs"][0]["arrival_time"]["value"])\
                + datetime.timedelta(hours = 1)
                
            feed = {
                        'departure_time_google': departure_time,
                        'arrival_time_google_transit': arrival_time,
                        'distance_google_transit': directions_result[0]["legs"][0]["distance"]["value"] / 1000.0,
                        'duration_google_transit': directions_result[0]["legs"][0]["duration"]["value"] / 60.0,
                        'fare_google_transit': directions_result[0]["fare"]["value"],
                        'distance_driving' : directions_result_driving[0]["legs"][0]["distance"]["value"] / 1000.0,
                        'duration_driving' : directions_result_driving[0]["legs"][0]["duration"]["value"] / 60.0
                    }
                    
            self.current_directions_result = directions_result
            self.current_feed = feed
            try:        
                self.to_DB(row['_id'])
            except:
                print "Error in updating in DB"


        return feed        
    
    def check_feed(self):
        """
        Check data stream correctness and consistency
        """
        pass

    def to_DB(self, object_id):
        
        dbp.update_bookings(self.city, self.current_feed, object_id)
         
    def run(self):

        self.start_session()
        self.get_feed()

end = datetime.datetime(2016, 12, 10, 0, 0, 0)
start = end - datetime.timedelta(hours = 1)
googlecar2go = GoogleDS('car2go', 'torino', 'timestamp', start, end)
googlecar2go.start_session()
feed = googlecar2go.get_feed()
directions = googlecar2go.current_directions_result

