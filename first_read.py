#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 15:07:56 2016

@author: alecioc
"""

import os
import pandas as pd

static_data_path = "./StaticData/"

raw_data_path = "./Raw/"
clean_data_path = "./Clean/"
if not os.path.exists(static_data_path + clean_data_path):
    os.makedirs(static_data_path + clean_data_path)

datasource_dirs = ["torino_it", "torino-it-archiver_20160404_0207"]
datasource_dict = { k:[] for k in datasource_dirs }    
    
def clean_static_files (raw_data_path, clean_data_path):
    for ds_dir in datasource_dirs:
    
        input_dir = raw_data_path + ds_dir + "/"
        output_dir = clean_data_path + ds_dir + "/"
    
        if ds_dir == "torino_it":
            for filename in sorted(os.listdir(input_dir)):
                if filename.endswith(".txt"):
                    datasource_dict[ds_dir].append(filename)
                    df = pd.read_csv(input_dir + filename)\
                        .dropna(axis=1, how='all')
                    with open(output_dir + filename, 'w+') as output_file:
                        df.to_csv(output_file)
                
def load (datasource, filename):
    return pd.read_csv(clean_data_path + datasource + "/" + filename)
    
#clean_static_files()
shapes_df = pd.read_csv(static_data_path + clean_data_path + "torino_it/" + "shapes.txt", \
                  index_col = 0)
