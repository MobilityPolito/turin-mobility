#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 12:27:28 2017

@author: anr.putina
"""

import sys
import datetime
import pandas as pd
sys.path.append('../Architecture')

from DataBaseProxy import DataBaseProxy
from EnjoyProvider import Enjoy
from Car2GoProvider import Car2Go

city = 'torino'
dbp = DataBaseProxy()

car_sharing = Enjoy()
#car_sharing = Car2Go()


year = 2017
month = 01


for day in range (1, 11, 1):
    
    print day 
    
    start = datetime.datetime(year, month, day, 0, 0, 0)
    end = datetime.datetime(year, month, day, 23, 59, 0)
    
    car_sharing.select_data(city, 'timestamp', start, end)
    car_sharing.get_fleet()

    day_insertion = datetime.datetime(year, month, day, 12, 0, 0)
    
    dbp.insert_fleet_day(day_insertion, car_sharing.name, car_sharing.city, list(car_sharing.fleet))