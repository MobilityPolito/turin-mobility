import threading
import logging
import requests
import datetime
import time
import json

import pandas as pd

from DataSource_without_Thread import DataGatherer
from DataBaseProxy import dbp

stop_enjoy = False

class EnjoyRTDS(DataGatherer):
    
    def __init__ (self, city):

        threading.Thread.__init__(self)        
        self.name = "enjoy"
        self.log_filename = "rtds.log"
        logging.basicConfig(filename=self.log_filename, level=logging.DEBUG)        
        
        self.city = city
        self.url_home = 'https://enjoy.eni.com/it/' + self.city + '/map/'
        self.url_data = 'https://enjoy.eni.com/ajax/retrieve_vehicles'

    def log_message (self, scope, status):
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
            
    def get_feed (self):
        
        if (datetime.datetime.now() - self.session_start_time).total_seconds() > 2400:
            self.session = self.session.close()
            self.start_session()
            self.session_start_time = datetime.datetime.now()

        try:
            feed = json.loads(self.session.get(self.url_data).text)
            message = self.log_message("feed","success")
        except:
            feed = {}
            message = self.log_message("feed","error")
        logging.debug(message)

        return feed
        
#    def check_feed (self, feed):
#        
#        last_feed_df = pd.DataFrame(self.last_feed)
#        current_feed_df = pd.DataFrame(self.current_feed)
#        for col in current_feed_df.columns:
#            s = current_feed_df[col]

    def to_DB (self):
    
        dbp.insert_snapshot(self.name, self.city, self.current_feed)
        
    def run(self):

        self.start_session()
        
        self.last_feed = self.get_feed()
        
        while stop_enjoy is False:
            self.current_feed = self.get_feed()
            self.check_feed()
            self.to_DB()
            self.last_feed = self.current_feed
            time.sleep(10)
        else:
            return

#enjoy_rtds = EnjoyRTDS("torino")
#enjoy_rtds.start()
