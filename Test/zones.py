#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 13:28:43 2017

@author: anr.putina
"""
import pandas as pd
import geopandas as gpd
from area_enjoy import create_zones_enjoy
from area_car2go import create_zones_car2go

zones_enjoy = create_zones_enjoy()
zones_car2go = create_zones_car2go('zones')
zones_car2go_airport = create_zones_car2go('airport')
zones_car2go_ikea = create_zones_car2go('ikea')

frames = [zones_enjoy, zones_car2go, zones_car2go_airport, zones_car2go_ikea]

zones = gpd.GeoDataFrame(pd.concat(frames))