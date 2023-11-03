#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 11:35:12 2023

@author: paweljakuszyk
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import scipy.stats as stats
import ptitprince as pt

# Set float_format to display up to 3 decimal places
pd.options.display.float_format = '{:.3f}'.format

path_to_write='/Volumes/ms/seropositive_project/figures'

# Create the folder if it doesn't exist
if not os.path.exists(path_to_write):
    os.makedirs(path_to_write)

#read in the data
df = pd.read_csv("/Volumes/ms/PJ_gRatio/Stata/data_ready.csv", sep=',', index_col=0)

#Select columns LIT and LD
columns_LIT = df.loc[:, 'lit_af_left':'lit_uf_right'].columns.tolist()
columns_LD = df.loc[:, 'ld_af_left':'ld_uf_right'].columns.tolist()

# Get list of column names that start with "lit_" and end with "_right"
lit_right_hemi = [col for col in df.columns if col.startswith("lit_") and not col.endswith("_left") and not col.endswith('complete')]
lit_left_hemi = [col for col in df.columns if col.startswith("lit_") and col.endswith("_left")]

ld_right_hemi = [col for col in df.columns if col.startswith("ld_") and not col.endswith("_left") and not col.endswith('complete')]
ld_left_hemi = [col for col in df.columns if col.startswith("ld_") and col.endswith("_left")]

#make values list to create dictionaries

values_right_and_mid = [
    "Arcuate fascicle",
    "Anterior Thalamic Radiation",
    "Rostrum",
    "Genu",
    "Rostral body",
    "Anterior midbody",
    "Posterior midbody",
    "Isthmus",
    "Splenium",
    "Cingulum",
    "Corticospinal tract",
    "Fronto-pontine tract",
    "Inferior cerebellar peduncle",
    "Inferior occipito-frontal fascicle",
    "Inferior longitudinal fascicle",
    "Middle cerebellar peduncle",
    "Optic radiation",
    "Parieto‐occipital pontine",
    "Superior cerebellar peduncle",
    "Superior longitudinal fascicle III",
    "Superior longitudinal fascicle II",
    "Superior longitudinal fascicle I",
    "Superior Thalamic Radiation",
    "Striato-fronto-orbital",
    "Striato-premotor",
    "Thalamo-occipital",
    "Thalamo-parietal",
    "Thalamo-premotor",
    "Uncinate fascicle"
]

values_left = [
    "Arcuate fascicle",
    "Anterior Thalamic Radiation",
    "Cingulum",
    "Corticospinal tract",
    "Fronto-pontine tract",
    "Inferior cerebellar peduncle",
    "Inferior occipito-frontal fascicle",
    "Inferior longitudinal fascicle",
    "Optic radiation",
    "Parieto‐occipital pontine",
    "Superior cerebellar peduncle",
    "Superior longitudinal fascicle III",
    "Superior longitudinal fascicle II",
    "Superior longitudinal fascicle I",
    "Superior Thalamic Radiation",
    "Striato-fronto-orbital",
    "Striato-premotor",
    "Thalamo-occipital",
    "Thalamo-parietal",
    "Thalamo-premotor",
    "Uncinate fascicle"
]

# Create a dictionary from the lists
lit_right_dict = dict(zip(lit_right_hemi, values_right_and_mid))
lit_left_dict = dict(zip(lit_left_hemi, values_left))

ld_right_dict = dict(zip(ld_right_hemi, values_right_and_mid))
ld_left_dict = dict(zip(ld_left_hemi, values_left))

# Filter the DataFrame based on the specified column names
lit_right_and_mid_df = df[lit_right_hemi + ['diagnosis']]
lit_left_df = df[lit_left_hemi + ['diagnosis']]

ld_right_and_mid_df = df[ld_right_hemi + ['diagnosis']]
ld_left_df = df[ld_left_hemi + ['diagnosis']]

#rename those sub dfs to full tract names based on dicts
lit_right_and_mid_df_renamed = lit_right_and_mid_df.rename(columns=lit_right_dict)
lit_left_df_renamed = lit_left_df.rename(columns=lit_left_dict)

ld_right_and_mid_df_renamed = ld_right_and_mid_df.rename(columns=ld_right_dict)
ld_left_df_renamed = ld_left_df.rename(columns=ld_left_dict)

##PLOTS

group_order = ['HC', 'RRMS', 'NMOSD']

##########################
######### LIT right#######
# Create a figure with a 7x3 subplot grid
n_col = 10
n_row = 3
fig, axs = plt.subplots(nrows=3, ncols=10, figsize=(30, 20))

# Flatten the axs array for easier indexing
axs = axs.flatten()

# Iterate over the tracts and plot a boxplot for each tract in each subplot
for i, tract in enumerate(lit_right_and_mid_df_renamed.columns[:-1]):
    
    # Create the boxplot
    pt.half_violinplot(data = lit_right_and_mid_df_renamed, width = .6, palette="Set2", ax=axs[i],x='diagnosis', y=tract, order=group_order)
    sns.stripplot(data = lit_right_and_mid_df_renamed, palette="Set2", ax=axs[i],x='diagnosis', y=tract,order=group_order)
    # plot the mean line
    sns.boxplot(showmeans=True,
                meanline=True,
                meanprops={'color': 'k', 'ls': '--', 'lw': 1.5},
                medianprops={'visible': False},
                whiskerprops={'visible': False},
                data=lit_right_and_mid_df_renamed,
                showfliers=False,
                showbox=False,
                showcaps=False,
                ax=axs[i],x='diagnosis', y=tract,
                order=group_order)
        
    #add horizontal grid lines
    axs[i].yaxis.grid(True)    
    axs[i].set_title(tract, fontsize=10)
    axs[i].set(ylabel='NDI')
    
    # Set x-axis font size using xticks() function
    axs[i].set_xticklabels(axs[i].get_xticklabels(), fontsize=9)  # Change the fontsize as needed
    # Hide the x-axis label ("diagnosis")
    axs[i].set_xlabel('')

# Add a main title to the figure
fig.suptitle('NDI values in tracts not traversing through white matter lesions in right hemisphere, corpus callosum and middle cerebellar peduncle')

# Adjust spacing between subplots
fig.tight_layout()

# Hide any empty subplots if the number of subplots is less than num_rows * num_cols
for i in range(len(lit_right_and_mid_df_renamed.columns[:-1]), n_row * n_col):
    axs[i].axis('off')

# Show the plot
plt.show()

####################################
############# LIT left##############
# Create a figure with a 7x3 subplot grid
n_col = 10
n_row = 3
fig, axs = plt.subplots(nrows=3, ncols=7, figsize=(30, 20))

# Flatten the axs array for easier indexing
axs = axs.flatten()

# Iterate over the tracts and plot a boxplot for each tract in each subplot
for i, tract in enumerate(lit_left_df_renamed.columns[:-1]):
    
    # Create the boxplot
    pt.half_violinplot(data = lit_left_df_renamed, width = .6, palette="Set2", ax=axs[i],x='diagnosis', y=tract, order=group_order)
    sns.stripplot(data = lit_left_df_renamed, palette="Set2", ax=axs[i],x='diagnosis', y=tract,order=group_order)
    # plot the mean line
    sns.boxplot(showmeans=True,
                meanline=True,
                meanprops={'color': 'k', 'ls': '--', 'lw': 1.5},
                medianprops={'visible': False},
                whiskerprops={'visible': False},
                data=lit_left_df_renamed,
                showfliers=False,
                showbox=False,
                showcaps=False,
                ax=axs[i],x='diagnosis', y=tract,
                order=group_order)
        
    #add horizontal grid lines
    axs[i].yaxis.grid(True)    
    axs[i].set_title(tract, fontsize=10)
    axs[i].set(ylabel='NDI')
    
    # Set x-axis font size using xticks() function
    axs[i].set_xticklabels(axs[i].get_xticklabels(), fontsize=9)  # Change the fontsize as needed
    # Hide the x-axis label ("diagnosis")
    axs[i].set_xlabel('')

# Add a main title to the figure
fig.suptitle('NDI values in tracts not traversing through white matter lesions in left hemisphere')

# Adjust spacing between subplots
fig.tight_layout()

# Hide any empty subplots if the number of subplots is less than num_rows * num_cols
for i in range(len(lit_left_df_renamed.columns[:-1]), n_row * n_col):
    axs[i].axis('off')

# Show the plot
plt.show()

##########################
######### LD right#######
# Create a figure with a 7x3 subplot grid
n_col = 10
n_row = 3
fig, axs = plt.subplots(nrows=3, ncols=10, figsize=(30, 20))

# Flatten the axs array for easier indexing
axs = axs.flatten()

# Iterate over the tracts and plot a boxplot for each tract in each subplot
for i, tract in enumerate(ld_right_and_mid_df_renamed.columns[:-1]):
    
    # Create the boxplot
    pt.half_violinplot(data = ld_right_and_mid_df_renamed, width = .6, palette="Set2", ax=axs[i],x='diagnosis', y=tract, order=group_order)
    sns.stripplot(data = ld_right_and_mid_df_renamed, palette="Set2", ax=axs[i],x='diagnosis', y=tract,order=group_order)
    # plot the mean line
    sns.boxplot(showmeans=True,
                meanline=True,
                meanprops={'color': 'k', 'ls': '--', 'lw': 1.5},
                medianprops={'visible': False},
                whiskerprops={'visible': False},
                data=ld_right_and_mid_df_renamed,
                showfliers=False,
                showbox=False,
                showcaps=False,
                ax=axs[i],x='diagnosis', y=tract,
                order=group_order)
        
    #add horizontal grid lines
    axs[i].yaxis.grid(True)    
    axs[i].set_title(tract, fontsize=10)
    axs[i].set(ylabel='NDI')
    
    # Set x-axis font size using xticks() function
    axs[i].set_xticklabels(axs[i].get_xticklabels(), fontsize=9)  # Change the fontsize as needed
    # Hide the x-axis label ("diagnosis")
    axs[i].set_xlabel('')

# Add a main title to the figure
fig.suptitle('NDI values in tracts traversing through white matter lesions in right hemisphere, corpus callosum and middle cerebellar peduncle')

# Adjust spacing between subplots
fig.tight_layout()

# Hide any empty subplots if the number of subplots is less than num_rows * num_cols
for i in range(len(ld_right_and_mid_df_renamed.columns[:-1]), n_row * n_col):
    axs[i].axis('off')

# Show the plot
plt.show()

####################################
############# LD left##############
# Create a figure with a 7x3 subplot grid
n_col = 10
n_row = 3
fig, axs = plt.subplots(nrows=3, ncols=7, figsize=(30, 20))

# Flatten the axs array for easier indexing
axs = axs.flatten()

# Iterate over the tracts and plot a boxplot for each tract in each subplot
for i, tract in enumerate(ld_left_df_renamed.columns[:-1]):
    
    # Create the boxplot
    pt.half_violinplot(data = ld_left_df_renamed, width = .6, palette="Set2", ax=axs[i],x='diagnosis', y=tract, order=group_order)
    sns.stripplot(data = ld_left_df_renamed, palette="Set2", ax=axs[i],x='diagnosis', y=tract,order=group_order)
    # plot the mean line
    sns.boxplot(showmeans=True,
                meanline=True,
                meanprops={'color': 'k', 'ls': '--', 'lw': 1.5},
                medianprops={'visible': False},
                whiskerprops={'visible': False},
                data=ld_left_df_renamed,
                showfliers=False,
                showbox=False,
                showcaps=False,
                ax=axs[i],x='diagnosis', y=tract,
                order=group_order)
        
    #add horizontal grid lines
    axs[i].yaxis.grid(True)    
    axs[i].set_title(tract, fontsize=10)
    axs[i].set(ylabel='NDI')
    
    # Set x-axis font size using xticks() function
    axs[i].set_xticklabels(axs[i].get_xticklabels(), fontsize=9)  # Change the fontsize as needed
    # Hide the x-axis label ("diagnosis")
    axs[i].set_xlabel('')
    

# Add a main title to the figure
fig.suptitle('NDI values in tracts traversing through white matter lesions in left hemisphere')

# Adjust spacing between subplots
fig.tight_layout()

# Hide any empty subplots if the number of subplots is less than num_rows * num_cols
for i in range(len(ld_left_df_renamed.columns[:-1]), n_row * n_col):
    axs[i].axis('off')

# Show the plot
plt.show()