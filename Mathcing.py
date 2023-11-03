#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 09:59:14 2023

@author: paweljakuszyk
"""

import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np
import os
from psmpy import PsmPy
from psmpy.functions import cohenD
from psmpy.plotting import *

# Set float_format to display up to 3 decimal places
pd.options.display.float_format = '{:.3f}'.format

path_to_write='/Volumes/ms/seropositive_project/'
# Set the folder name
folder_name = 'Analysis/Matching/'

# Create the folder if it doesn't exist
if not os.path.exists(path_to_write+folder_name):
    os.makedirs(path_to_write+folder_name)

#read in the data
df = pd.read_csv("/Volumes/ms/PJ_gRatio/Stata/data_ready.csv", sep=',')

# subset the dataframe based on the value in the 'group' column
groups_disease = df[df['diagnosis'] != 'HC'].reset_index()

# Create a mapping of each unique category to a unique numeric value
mapping = {
    'RRMS': 1,
    'NMOSD': 0,
    }
# Use the map function to replace each category with its corresponding numeric value
groups_disease['diagnosis'] = groups_disease['diagnosis'].map(mapping)

groups_to_match = groups_disease[['record_id', 'age', 'edss','diagnosis']]

# Split the dataframe into two groups
group1 = groups_to_match[groups_to_match['diagnosis'] == 1]
group2 = groups_to_match[groups_to_match['diagnosis'] == 0]

# Select the variables used for matching
match_vars = ['age', 'edss']

# Fit a nearest-neighbor model on group 1
nbrs = NearestNeighbors(n_neighbors=1, algorithm='auto').fit(group1[match_vars])

# Find the closest match in group 1 for each observation in group 2
distances, indices = nbrs.kneighbors(group2[match_vars])

# Add the indices of the closest matches to group 2
group2['matched_index'] = indices

# Merge the matched observations back together
matched = pd.merge(group1, group2, left_index=True, right_on='matched_index', suffixes=('_1', '_2'))

# Print the resulting dataframe
print(matched)
