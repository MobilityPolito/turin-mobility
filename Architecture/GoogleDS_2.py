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
#                        'AIzaSyD3PdBLQxWMDsaJ1tdHOs02QNBuIEqLSiQ', 
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
                        'AIzaSyB0ggpBGN6wRpsA1cdfAgO2iVtSt6Nj41I',
                        'AIzaSyDVU9CsZY89DZv7JC7N5u8HTWrppGJNOko', #chiave tano
                        'AIzaSyCDdrDzYVj0zwvV3Xhx9IJ6gv-L9PVXYaM' # sbr
                    ])

        self.current_key = 5
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
            print "chiave: " + str(self.current_key)
            self.gmaps = googlemaps.Client(key=self.keys.iloc[self.current_key])
            
        def manage_key(self, row, mode):
            try:
                directions_result = self.gmaps.directions([row['start_lat'], row['start_lon']], 
                                                          [row['end_lat'], row['end_lon']], 
                                                          mode=mode, 
                                                          departure_time = next_weekday(datetime.datetime.now(), row['start']))
                message = self.log_message("direction_" + mode,"success")
                print "Tutto bene fin qui"
                change_key(self)
            except urllib2.HTTPError, err:
                count = 0
                while (err.resp.status in [403]) and (count<len(self.keys)): # key limits exceeded
                    print "Key limits exceeded"
                    change_key(self)
                    directions_result = self.gmaps.directions([row['start_lat'], row['start_lon']], 
                                                              [row['end_lat'], row['end_lon']], 
                                                              mode=mode, 
                                                              departure_time = next_weekday(datetime.datetime.now(), row['start']))
                    count = count + 1
                if err.resp.status in [403]:
                    print "Error in retrieving" + mode + "information"
                    message = self.log_message("direction_" + mode,"error")
                    time.sleep(60)
            logging.debug(message)
            return directions_result


        books_df = dbp.get_books(self.provider, self.city, self.start, self.end)
        print len(books_df)
                    
        
        for i in range(len(books_df)):
            print "book: " + str(i) 

            row = books_df.iloc[i]
            
            feed = {
                    'distance_driving' : None,
                    'duration_driving' : None,
                    'duration_in_traffic_google' : None,                                   
                    'fare_google_transit' : None,
                    'duration_google_transit' : None,
                    'arrival_time_google_transit' : None,
                    'distance_google_transit' : None,
                    'departure_time_google' : None
                    }
         
            if ('distance_driving' in row.index) and (pd.notnull(row['distance_driving'])):
                continue
            else:
                if ((row['start_lat']==row['end_lat']) and (row['end_lon']==row['end_lon'])):
                    self.current_feed = feed
                    self.to_DB(row['_id'])
                    continue
                directions_result = manage_key(self, row, 'transit')
                if not directions_result:
                    continue
#                try:
#                    directions_result = self.gmaps.directions([row['start_lat'], row['start_lon']], 
#                                                              [row['end_lat'], row['end_lon']], 
#                                                              mode="transit", 
#                                                              departure_time = next_weekday(datetime.datetime.now(), row['start']))
#                    message = self.log_message("direction_transit","success")
#                    if not directions_result:
#                        continue
#                    change_key(self)
#                except urllib2.HTTPError, err:
#                    count = 0
#                    while (err.resp.status in [403]) and (count<len(self.keys)): # key limits exceeded
#                        print "Key limits exceeded"
#                        change_key(self)
#                        directions_result = self.gmaps.directions([row['start_lat'], row['start_lon']], 
#                                                                  [row['end_lat'], row['end_lon']], 
#                                                                  mode="transit", 
#                                                                  departure_time = next_weekday(datetime.datetime.now(), row['start']))
#                        count = count + 1
#                        if not directions_result:
#                            continue
#                    if err.resp.status in [403]:
#                        print "Error in retrieving transit information"
#                        message = self.log_message("direction_transit","error")
#                        time.sleep(60)
#                logging.debug(message)
                time.sleep(1)
                directions_result_driving = manage_key(self, row, 'driving')
                if not directions_result_driving:
                    continue
#                try:
#                    directions_result_driving = self.gmaps.directions([row['start_lat'], row['start_lon']], 
#                                                                  [row['end_lat'], row['end_lon']], 
#                                                                  mode="driving",
#                                                                  departure_time = next_weekday(datetime.datetime.now(), row['start']))
#                    message = self.log_message("direction_transit","success")
#                    if not directions_result_driving:
#                        continue
#                except urllib2.HTTPError, err:
#                    count = 0
#                    while (err.resp.status in [403]) and (count<len(self.keys)): # key limits exceeded
#                        print "Key limits exceeded"
#                        change_key(self)
#                        directions_result_driving = self.gmaps.directions([row['start_lat'], row['start_lon']], 
#                                                                  [row['end_lat'], row['end_lon']],                                                              
#                                                                  mode="driving",
#                                                                  departure_time = next_weekday(datetime.datetime.now(), row['start']))
#                        count = count + 1
#                        if not directions_result_driving:
#                            continue
#                    if err.resp.status in [403]:
#                        print "Error in retrieving driving information"
#                        message = self.log_message("direction_driving","error")
#                        time.sleep(60)
#                logging.debug(message)                
                time.sleep(1) 
                   
                if directions_result_driving[0]["legs"][0]["steps"][0]['travel_mode'] == 'DRIVING':
                    feed['distance_driving'] = directions_result_driving[0]["legs"][0]["distance"]["value"] / 1000.0
                    feed['duration_driving'] = directions_result_driving[0]["legs"][0]["duration"]["value"] / 60.0
                    if 'duration_in_traffic' in directions_result_driving[0]["legs"][0]:
                        feed['duration_in_traffic_google'] = directions_result_driving[0]["legs"][0]["duration_in_traffic"]["value"] / 60.0
                else:
                    print "NO DRIVING INFO"
                try: 
                    if "departure_time" in directions_result[0]["legs"][0]:
                        departure_time = datetime.datetime.utcfromtimestamp\
                        (directions_result[0]["legs"][0]["departure_time"]["value"])\
                        + datetime.timedelta(hours = 1)
                        feed['departure_time_google'] = departure_time
                except:
                        print "DepartureTime missing"
                        print row['_id']
                
                if 'fare' in directions_result[0]:
                    feed['fare_google_transit'] = directions_result[0]["fare"]["value"]
                    feed['distance_google_transit'] = directions_result[0]["legs"][0]["distance"]["value"] / 1000.0
                    feed['duration_google_transit'] = directions_result[0]["legs"][0]["duration"]["value"] / 60.0
                    if "arrival_time" in directions_result[0]["legs"][0]:
                        arrival_time = datetime.datetime.utcfromtimestamp\
                        (directions_result[0]["legs"][0]["arrival_time"]["value"])\
                        + datetime.timedelta(hours = 1)
                        feed['arrival_time_google_transit'] = arrival_time
                    else:
                        print "ArrivalTime missing"
                        print row['_id']
                else:
                    print "Fare missing"
                    print row['_id']  
    
    
                change_key(self)
                self.current_directions_result = directions_result
                self.current_feed = feed
                self.to_DB(row['_id'])
            

        return feed        
    
    def check_feed(self):
        """
        Check data stream correctness and consistency
        """
        pass

    def to_DB(self, object_id):
        try:        
            dbp.update_bookings(self.city, self.current_feed, object_id)
        except:
            print "Error in updating in DB"
         
    def run(self):

        self.start_session()
        self.get_feed()

end = datetime.datetime(2016, 12, 14, 0, 0, 0)
start = end - datetime.timedelta(days = 5)
googlecar2go = GoogleDS('car2go', 'torino', 'timestamp', start, end)
googlecar2go.start_session()
feed = googlecar2go.get_feed()
#directions = googlecar2go.current_directions_result

