#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 15:32:12 2017

@author: root
"""
import pandas as pd
with open("chiavi.txt") as f: 
    series_keys = pd.Series(f.readlines())