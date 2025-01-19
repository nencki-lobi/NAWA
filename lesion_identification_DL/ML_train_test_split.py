#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 12:24:33 2023

@author: pawel
"""

import pandas as pd
from sklearn.model_selection import train_test_split
import os
# Assuming your dataframe is named 'df' with columns 'ids' and 'group'
#read in the data
df = pd.read_csv("/Volumes/ms/PJ_gRatio/Stata/data_ready.csv", sep=',')

selected_columns = ['diagnosis', 'record_id']
new_df = df[selected_columns].copy()

# Splitting the dataframe based on the group column
groups = new_df['diagnosis'].unique()

train_df = pd.DataFrame()
val_df = pd.DataFrame()

for group in groups:
    group_df = new_df[new_df['diagnosis'] == group]
    train_group, val_group = train_test_split(group_df, test_size=0.2, random_state=42)
    train_df = pd.concat([train_df, train_group])
    val_df = pd.concat([val_df, val_group])

# Checking the resulting splits
print("Training Set:")
print(train_df.head())
print("\nValidation Set:")
print(val_df.head())

#save results
# Create the lesion_masks folder if it doesn't exist
split_info_folder = "/Volumes/ms/ML/LD_data/Split_info"
os.makedirs(split_info_folder, exist_ok=True)

train_df.to_csv(split_info_folder+'/train.csv', index=True)
val_df.to_csv(split_info_folder+'/validation.csv', index=True)
