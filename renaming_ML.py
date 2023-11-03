#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 13:03:32 2023

@author: pawel
"""

import os

data_dir = "/Volumes/ms/ML/LD_data_copy/"

flair_dir = os.path.join(data_dir, 'normalized_FLAIR')
mask_dir = os.path.join(data_dir, 'lesion_masks')

# Create a dictionary for mapping the old names to new names
FLAIR_mapping = {}

lesion_mapping = {}

# Iterate over the files in the folder
for i, file_name in enumerate(sorted(os.listdir(flair_dir)), start=1):
    if file_name.endswith('.nii.gz'):
        old_name = os.path.join(flair_dir, file_name)
        new_name = os.path.join(flair_dir, f"{i}_FLAIR.nii.gz")
        FLAIR_mapping[old_name] = new_name
        
# Iterate over the files in the folder
for i, file_name in enumerate(sorted(os.listdir(mask_dir)), start=0):
    if file_name.endswith('.nii.gz'):
        old_name = os.path.join(mask_dir, file_name)
        new_name = os.path.join(mask_dir, f"{i}_mask.nii.gz")
        lesion_mapping[old_name] = new_name

# Rename the files using the dictionary
for old_name, new_name in FLAIR_mapping.items():
    os.rename(old_name, new_name)
    
# Rename the files using the dictionary
for old_name, new_name in lesion_mapping.items():
    os.rename(old_name, new_name)
    
# Load the names of the files from both folders
folder1_files = sorted(file for file in os.listdir(flair_dir) if file.endswith('.nii.gz'))
folder2_files = sorted(file for file in os.listdir(mask_dir) if file.endswith('.nii.gz'))


# Determine the maximum length of the file names for proper alignment
max_length = max(len(file1) for file1 in folder1_files) + 5

# Print the files side by side
print(f"{'Folder 1':<{max_length}} Folder 2")
print('-' * (max_length + 10))

for file1, file2 in zip(folder1_files, folder2_files):
    print(f"{file1:<{max_length}} {file2}")