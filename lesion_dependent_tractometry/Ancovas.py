#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 12:44:58 2023

@author: paweljakuszyk
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from PIL import Image


# Set float_format to display up to 3 decimal places
pd.options.display.float_format = '{:.3f}'.format

path_to_write='/Volumes/ms/seropositive_project/'
# Set the folder name
folder_name = 'Analysis/Ancova/'

# Create the folder if it doesn't exist
if not os.path.exists(path_to_write+folder_name):
    os.makedirs(path_to_write+folder_name)

#read in the data
df = pd.read_csv("/Volumes/ms/PJ_gRatio/Stata/data_ready.csv", sep=',')

# subset the dataframe based on the value in the 'group' column
groups_disease = df[df['diagnosis'] != 'HC'].reset_index()

# Create a mapping of each unique category to a unique numeric value
#mapping = {
#    'RRMS': 1,
#    'NMOSD': 2,
#    }
#
# Use the map function to replace each category with its corresponding numeric value
#groups_disease['diagnosis'] = groups_disease['diagnosis'].map(mapping)

#subset data for tract iteration
LIT = groups_disease.loc[:,'lit_af':'lit_slf']

#PLOT ANCOVAS FOR EDSS
# iterate over each variable in each group and plot its correlation
for i, tract in enumerate(LIT.columns):
    # create ANCOVA plot with x as a variable from groups_disease, y as 'diagnosis', and hue as 'edss'
    g = sns.lmplot(x='edss', y=tract, hue='diagnosis',data=groups_disease, legend_out=False, truncate=False)
    # set x-label to tract
    g.set_axis_labels('EDSS',tract)
    # set title of the plot
    g.fig.suptitle('EDSS vs. {}'.format(tract))
    # use tight layout
    plt.tight_layout()
    # save the figure with a specified file path and name
    plt.savefig(path_to_write + folder_name + tract +'_MS_NMOSD_EDSS_ancovas.png')

#COmbine plots into one image
# Set the input folder and output file path
input_folder = "/Volumes/ms/seropositive_project/Analysis/Ancova/"
output_folder = "/Volumes/ms/seropositive_project/Analysis/Ancova/Combined/"

# Create the folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    
# Get the list of image paths in the input folder
image_paths = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.png')]

# Create a new image with the desired size and padding
num_cols = 7
num_rows = 3
padding = 10
# Load one image to get its resolution
img = Image.open(image_paths[0])
# Get the width and height of the image
img_width, img_height = img.size
# Calculate the new size of the image including padding
new_img_width = (img_width + padding) * num_cols - padding
new_img_height = (img_height + padding) * num_rows - padding
new_img = Image.new('RGB', (new_img_width, new_img_height), color=(255, 255, 255))

# Iterate over the image paths and paste each image into the new image
for i, path in enumerate(image_paths):
    # Open the image file and resize it as needed
    img = Image.open(path)
    img = img.resize((img_width, img_height))
    # Create a new padded image and paste the original image onto it
    padded_img = Image.new('RGB', (img_width + padding, img_height + padding), color=(255, 255, 255))
    padded_img.paste(img, (padding // 2, padding // 2))
    # Calculate the coordinates for the top-left corner of the current image
    col = i % num_cols
    row = i // num_cols
    x = col * (img_width + padding)
    y = row * (img_height + padding)
    # Paste the padded image into the new image
    new_img.paste(padded_img, (x, y))

# Save the new image
new_img.save(output_folder+'Ancovas_MS_NMOSD_EDSS_combined.png')

#PLOT ANCOVAS FOR AGE
# iterate over each variable in each group and plot its correlation
for i, tract in enumerate(LIT.columns):
    # create ANCOVA plot with x as a variable from groups_disease, y as 'diagnosis', and hue as 'edss'
    g = sns.lmplot(x='age', y=tract, hue='diagnosis',data=groups_disease, legend_out=False, truncate=False)
    # set x-label to tract
    g.set_axis_labels('Age',tract)
    # set title of the plot
    g.fig.suptitle('Age vs. {}'.format(tract))
    # use tight layout
    plt.tight_layout()
    # save the figure with a specified file path and name
    plt.savefig(path_to_write + folder_name + tract +'_MS_NMOSD_Age_ancovas.png')

#COmbine plots into one image
# Set the input folder and output file path
input_folder = "/Volumes/ms/seropositive_project/Analysis/Ancova/"
output_folder = "/Volumes/ms/seropositive_project/Analysis/Ancova/Combined/"

# Create the folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    
# Get the list of image paths in the input folder
image_paths = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.png')]

# Create a new image with the desired size and padding
num_cols = 7
num_rows = 3
padding = 10
# Load one image to get its resolution
img = Image.open(image_paths[0])
# Get the width and height of the image
img_width, img_height = img.size
# Calculate the new size of the image including padding
new_img_width = (img_width + padding) * num_cols - padding
new_img_height = (img_height + padding) * num_rows - padding
new_img = Image.new('RGB', (new_img_width, new_img_height), color=(255, 255, 255))

# Iterate over the image paths and paste each image into the new image
for i, path in enumerate(image_paths):
    # Open the image file and resize it as needed
    img = Image.open(path)
    img = img.resize((img_width, img_height))
    # Create a new padded image and paste the original image onto it
    padded_img = Image.new('RGB', (img_width + padding, img_height + padding), color=(255, 255, 255))
    padded_img.paste(img, (padding // 2, padding // 2))
    # Calculate the coordinates for the top-left corner of the current image
    col = i % num_cols
    row = i // num_cols
    x = col * (img_width + padding)
    y = row * (img_height + padding)
    # Paste the padded image into the new image
    new_img.paste(padded_img, (x, y))

# Save the new image
new_img.save(output_folder+'Ancovas_MS_NMOSD_Age_combined.png')
