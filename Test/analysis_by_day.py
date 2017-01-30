#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 18:41:28 2017

@author: anr.putina
"""

import sys
sys.path.append('../Architecture')

import json
import datetime

import pandas as pd
import geopandas as gpd

#from Car2GoProvider import Car2Go
#from EnjoyProvider import Enjoy
#from Analysis import day_analysis, getODmatrix

from DataBaseProxy import DataBaseProxy

from Analysis import *
from BooksAnalysis import get_books_hours_stats


#enjoy = Enjoy()
#enjoy_fleet = enjoy.get_fleet_from_db()
dbp = DataBaseProxy()

##################################################
##################DATA ANALYSIS###################
##################################################

provider = 'enjoy'
city = 'torino'

year = 2016
month = 12

zones = gpd.read_file("../../SHAPE/Zonizzazione.dbf").to_crs({"init": "epsg:4326"})

#zones = gpd.read_file("../../../SHAPE/Zones_limit.dbf").to_crs({"init": "epsg:4326"})

for day in range(10, 11, 1):

	print ('day:'+str(day))

	start = datetime.datetime(year, month, 5, 0, 0, 0)
	end = datetime.datetime(year, month, 15, 23, 59, 59)

#	fleet_size = len(dbp.query_fleet_by_day(provider, city, start, end)[0]['fleet'])
 
#	provider_books = dbp.query_books_df_filtered_v2(provider, city, start, end, "full")
#	books_df, stats = get_books_hours_stats(provider_books)

	dataframeOD, origins, destinations, od = getODmatrix(city, provider, zones, start, end)

	#books_df_car2go, parks_d_car2go, day_stats_car2go = \
	#    day_analysis(city, provider, start, end, fleet_size)
#	zones, origins, destinations, od = getODmatrix(city, provider, year, month, day)

	# day_db = datetime.datetime(year, month, day, 12, 00)
	# dbp.insert_day_analysis(day_db, city, provider, list(stats.T.to_dict().values()), json.loads(od.T.to_json()).values())