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
import pytz 
import pandas as pd
import numpy as np
 
import googlemaps
 
from DataSource_without_Thread import DataGatherer
from DataBaseProxy import DataBaseProxy
dbp = DataBaseProxy()

class GoogleDS(DataGatherer):
       
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
#                        'AIzaSyBnUsB3u6Blg23D5uqIQPnM_1Pawkp5VLY',
#                        'AIzaSyBaaQQyMnT7MUI421WdO67g66igzXL2O4A',
#                        'AIzaSyDbPG5qS-g0pROiPRcOT2G-keWi54ie2-M',
#                        'AIzaSyCjy-sVWBCyN9FOjBeNg2_OeULs-uXSmMI',
#                        'AIzaSyAUrnCmaEs7e7izfCiKYm-k7Ap0EwZzYes',
#                        'AIzaSyCeT4Z_Cfabvpnh2FBbf3TCrhBNtwlfVwU',
#                        'AIzaSyAcPVep5aXJLbuBDV7Qn_JaWSpD4o6s30w', 
#                        'AIzaSyBHz8SA5BKIJDOu9mtLJb5JilGvcLnGIiM',
#                        'AIzaSyBqMJcxNQUmciUN8qsI-4JVO9Hh_EJqNfE',
#                        'AIzaSyB9XupnKFaH-zuVg_lBlz7NO8q6QpWFKZk',
#                        'AIzaSyAVpeQaUjVPZznjp1b1sbtUl2iBzHSuGek',
#                        'AIzaSyCoFpO5q5MatCal_1lLaxVCr6LcXePo91M',
#                        'AIzaSyCGfLn4VqFrbV1PFc6duXi7ojPktJb-ta4',
#                        'AIzaSyA6zgFdORCnKRnpp74Ew925aCwbSmzsM9U',
#                        'AIzaSyBSjjou5aXnl-9L3SIaJR05Vc3Zb8j0WpY',
#                        'AIzaSyAKaQDrgawidGlRNkjqTIMngFZs7pOV8Zc',
#                        'AIzaSyCnksllWfpV0D3iDBomyKRFUkqEvEoNtKg',
#                        'AIzaSyB0ggpBGN6wRpsA1cdfAgO2iVtSt6Nj41I',
#                        'AIzaSyDVU9CsZY89DZv7JC7N5u8HTWrppGJNOko',  
#                        'AIzaSyCDdrDzYVj0zwvV3Xhx9IJ6gv-L9PVXYaM',
#                        'AIzaSyC846uXMy_r_Oh0jDBZdt5IzZnm4FuQi4g',
#                        'AIzaSyCgI76-0WngwQVoTjQHwMuV0RoOetOqdaY',
#                        'AIzaSyCDHutrFFMeC_Eabvx3xlPWXBKRbAq3uiY',
#                        'AIzaSyB0s6yNxx5zP8Z6_-fG-8dRTiTBbQnpyRM',
#                        'AIzaSyD1KTSXE5ZI1ZhlLkcHL0Se4of7E-ySF0s',
#                        'AIzaSyCrB9XXWrMQxh2u7MhAe85T3wxGgSub5Wo',
#                        'AIzaSyDVmI2S_fSIiMd2sXxCoUFJAltlSkHue4A',
#                        'AIzaSyAhHK0alplPwl8F1EbBQdg3geZSFsagaEY',
#                        'AIzaSyCO3Lg7nkuXAxPamTxuFrQmxkAYn-DRt2M', 
#                        'AIzaSyAGH6f-iU3mniyU74tPDoYlTv7KfD9GGts',
#                        'AIzaSyDnjsWBJLiu2KeQuB06SI3MX5oNcSxYGpk',
#                        'AIzaSyA02bc_0MCLk9bJ5VQl61friKy_jez-fDg',
#                        'AIzaSyDE1gmIDOwgNqZwtPG4n0cXuAWJC-o6zqs',  
#                        'AIzaSyBHDeDRrHZUWZGLpCYX-lsOCJtpE_iOmxY',  
#                        'AIzaSyDXITzscAk9WiYdSufNbCXMb8S0N6vMKo4',
#                        'AIzaSyD4-UC0o3G5ZGsu-10iAaJk8UbPuoo_8Zs',
#                        'AIzaSyBfJR-CbDlJTP5muitqaPPZpRyG0pwnV8c', 
#                        'AIzaSyDRMVFkibqRU2ZyupJK21K08YdeU4huADI',
#                        'AIzaSyCjgNFAJJgLr_uAETkXR0oBJOfm3waUCEI',
#                        'AIzaSyC0KdkkbI1KkO8SOTg3LAWDvrH31yek14s', 
#                        'AIzaSyBzWqwdMfkFYlMEOHEukfJEQ5UhV-3jRaU',
#                        'AIzaSyDmOL7veIgsgNGBI7mSp6Ae7WKg5xC-M9A', 
#                        'AIzaSyCZ_HyYgD0e5PE_IbcUAm86tgRdqTKIVa4', 
#                        'AIzaSyDINMpddT6_02MXVVh_eZX_loznPYkk9RQ', 
#                        'AIzaSyArjlKz9vAzX6CSCNYXkfjbejybaeCG1tI',
#                        'AIzaSyBTmkpRo_chM1F6EKWL49XpuZThmNLDI1Q',
#                        'AIzaSyBTuu3MBUtqKNh9U0TdLK1cR6RmYFmTSNI',
#                        'AIzaSyAdNcdinGUCkoIuxYrYYmASNMc--yClRGU',
#                        'AIzaSyAjHuNQcgdppxyLzxTZLnebLgQrqHYU9rs',
#                        'AIzaSyAMEAKU2tvWlAD9dTW6caHQz7MOpY5sEts',
#                        'AIzaSyDQtEe-SCGTzBdvzICGB0xDQhW1Fwes1IM',
#                        'AIzaSyAsD334lOk1j3kcxJsukjxCU7gYiyhCwEw',
#                        'AIzaSyAgZ0CVty4csyFOahjJ6qLt45SkvGkLNws',
#                        'AIzaSyBV0Pt5zrM3FfQZthXNVcnk-LGlEX-VJM8',
#                        'AIzaSyD27GZgUF9EvBm9FnnxtYvITr2T1DoXbgs',
#                        'AIzaSyBuB0z38UKKpRr2Q-yE2cYb_G0fzK35l58',
#                        'AIzaSyBiOBLKT6Lhqe1S6Snr6kXjm8k1omlk84E',
#                        'AIzaSyCiO7Mq1126rVOhB7GviIn9RHmi-WPMdMI',
#                        'AIzaSyAqkZFyTXCZ0uw9kLlQqk0SoCGJTROwFOU',
#                        'AIzaSyCj185lSh8Jmy_yuFY5WUGzDXLSVGaFfl8',
#                        'AIzaSyDW2f8E8jbPAPOc5HkrV6FxpAlN2CC6SnY',
#                        'AIzaSyCCykwZbKA6HP37jMaqBMeNF-vd_I5IClU',
#                        'AIzaSyCzyusNzfAXGt_I6llVedB3XgHnrnRSguc',
#                        'AIzaSyCNAPVUGE009Jwt-HFcJzkICgip-Vthrqo',
#                        'AIzaSyBNjWRFmiMG6nrLgM3yl4OjDzqk5WUaK3g',
#                        'AIzaSyCxueXvh-KigSV57C_xU2s4IqsfncuODNQ',
#                        'AIzaSyCLhyRuqK4ToyKpXRq9Bj3EwGGVu5DqP3Y',
#                        'AIzaSyDY-vxkPbJ-fbpKvKrrAB87PU_MgsdPvys'
#                        'AIzaSyBWpLux2H4qWJ83hYboLZzj_MW20FKgu38',
                        'AIzaSyA9cuVnYlm1_lAv2pZdpic4lPdWQeTnSTQ',
                        'AIzaSyAe8X4tnMrNC8VgAzvyNCxyzMla5zTDfLs',
                        'AIzaSyAKZRcJtQCY-3zRLKPO0fbLuRmZ-VNCS20',
                        'AIzaSyBWLEjpvkaMVE3_VMWJdfDhlhqVVXRYALI',
                        'AIzaSyAj0HTPsaEybv8UmeHcXcTAFiB1ACQ1beY'
                        
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
        print self.keys.iloc[self.current_key]
        try:
            self.gmaps = googlemaps.Client(key=self.keys.iloc[self.current_key])
            self.session_start_time = datetime.datetime.now()
            message = self.log_message("session","success")
            print "successfully cocnnected"
        except:
            message = self.log_message("session","error")
        logging.debug(message)
       
    def get_feed(self, books_df):
        self.books_df = books_df
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
            print self.keys.iloc[self.current_key]
            self.gmaps = None
            self.gmaps = googlemaps.Client(key=self.keys.iloc[self.current_key])
           
        def manage_key(self, row, mode):
            
            scheduled_start = next_weekday(datetime.datetime.now(), row['start'])
            
            try:
                directions_result = self.gmaps.directions([row['start_lat'], row['start_lon']],
                                                          [row['end_lat'], row['end_lon']],
                                                          mode=mode,
                                                          departure_time = scheduled_start)
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
                                                              departure_time = scheduled_start)
                    count = count + 1
                if err.resp.status in [403]:
                    print "Error in retrieving" + mode + "information"
                    message = self.log_message("direction_" + mode,"error")
#                    time.sleep(10)
            logging.debug(message)
            return directions_result, scheduled_start
 
 
#        books_df = dbp.query_books_df_ok(self.provider, self.city, self.start, self.end)
        print len(books_df)
       
        for i in range(len(books_df)):
            print "book: " + str(i)

            row = books_df.iloc[i]
            print row['provider']
            print row['_id']
           
            feed = {
                        'distance_driving' : np.NaN,
                        'duration_driving' : np.NaN,
                        'duration_in_traffic_google' : np.NaN,                                  
                        'fare_google_transit' : np.NaN,
                        'duration_google_transit' : np.NaN,
                        'tot_duration_google_transit':np.NaN,
                        'arrival_time_google_transit' : np.NaN,
                        'distance_google_transit' : np.NaN,
                        'departure_time_google' : np.NaN
                    }
         
            if ('distance_driving' in row) and row.isnull()['distance_driving'] == False:
                continue
            else:
                if ((row['start_lat'] == row['end_lat']) and (row['start_lon'] == row['end_lon'])):
                    self.current_feed = feed
                    self.to_DB(row['_id'])
                    continue
                directions_result, scheduled_start = manage_key(self, row, 'transit')
                feed['departure_time_google'] = scheduled_start
                try:
                    results_bus = directions_result[0]["legs"][0]
                except:
                    pass
                if not directions_result:
                    continue
 
                
                directions_result_driving, scheduled_start = manage_key(self, row, 'driving')
                results_car = directions_result_driving[0]["legs"][0]
                if not directions_result_driving:
                    continue
               
                time.sleep(0.3)
                   
                if results_car["steps"][0]['travel_mode'] == 'DRIVING':
                    feed['distance_driving'] = results_car["distance"]["value"] / 1000.0
                    feed['duration_driving'] = results_car["duration"]["value"] / 60.0
                    if 'duration_in_traffic' in results_car:
                        feed['duration_in_traffic_google'] = results_car["duration_in_traffic"]["value"] / 60.0
                else:
                    print "NO DRIVING INFO"
               
               
                if 'fare' in directions_result[0]:
                    feed['fare_google_transit'] = directions_result[0]["fare"]["value"]
                    feed['distance_google_transit'] = results_bus["distance"]["value"] / 1000.0
                    feed['duration_google_transit'] = results_bus["duration"]["value"] / 60.0
                    if "arrival_time" in results_bus:
                        if  type(results_bus["arrival_time"]["value"]) == int:
                            arrival_time = datetime.datetime.fromtimestamp(results_bus["arrival_time"]["value"], pytz.utc)\
                                            + datetime.timedelta(hours = 1)
                            arrival_time = arrival_time.replace(tzinfo=None)
                        else:
                            arrival_time = results_bus["arrival_time"]["value"]
                        feed['arrival_time_google_transit'] = arrival_time
                        time_difference = arrival_time - scheduled_start
                        feed['tot_duration_google_transit'] = time_difference.total_seconds() / 60
                    else:
                        print "ArrivalTime missing"
                        print row['_id']
                else:
                    print "Fare missing"
                    print row['_id']  
                print row['_id']
                print row['provider'], self.current_key
                print i, len(books_df)
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
        
###        
##year =  2017
##month = 1
####
#year =  2017
#month = 1
##
##for day in range(20, 31, 1): 
##    print ('Inizio ' +str(day))
##    start = datetime.datetime(year, month, day, 0, 0, 0)
##    end = datetime.datetime(year, month, day, 23, 59, 59)
##       
##    books_df = dbp.query_books_df_ok('car2go','torino',  start, end)
##    ##
##    googlecar2go = GoogleDS('car2go', 'torino', 'timestamp', start, end)
##    googlecar2go.start_session()
##    feed = googlecar2go.get_feed(books_df)
##    print ('Fine ' + str(day))
#
####
##
#
#
#for day in range(25, 31, 1): 
#
#   print ('Inizio ' +str(day))
#   start = datetime.datetime(year, month, day, 0, 0, 0)
#   end = datetime.datetime(year, month, day, 23, 59, 59)
#       
#   books_df_ = dbp.query_books_df_ok('enjoy','torino',  start, end)
#   googleenjoy = GoogleDS('enjoy', 'torino', 'timestamp', start, end)
#   googleenjoy.start_session()
#   feed2 = googleenjoy.get_feed(books_df_)
#   print ('Fine ' + str(day))