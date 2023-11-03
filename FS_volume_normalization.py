#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 13:22:48 2023

@author: paweljakuszyk
"""


import numpy as np
import pandas as pd
import os


# Set float_format to display up to 3 decimal places
pd.options.display.float_format = '{:.3f}'.format

path_to_write='/Volumes/pjakuszyk/freesurfer_output/'

# Create the folder if it doesn't exist
if not os.path.exists(path_to_write):
    os.makedirs(path_to_write)

#read in the data
df = pd.read_csv("/Volumes/pjakuszyk/freesurfer_output/aseg_stats.csv", sep=',')

# Delete the columns based on the column names
df = df.loc[:, ~df.columns.isin(df.loc[:, 'MaskVol':'SurfaceHoles'].columns)]

# Delete the columns based on the column names
df = df.loc[:, ~df.columns.isin(df.loc[:, '5th-Ventricle':'Right-non-WM-hypointensities'].columns)]

#Normalize volumes by Etiv

# Iterate over the columns (except the first column)
for col in df.columns[1:]:
    df[col] = (df[col] / df['EstimatedTotalIntraCranialVol'])*100
    
df.to_csv(path_to_write+'volumes_nomrlized_to_ETIV.csv', index=False)
