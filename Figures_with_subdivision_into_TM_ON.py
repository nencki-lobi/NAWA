#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 10:36:00 2023

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
df = pd.read_csv("/Volumes/ms/PJ_gRatio/Stata/data_ready.csv", sep=',')

full_names = {
    'lit_af': 'Arcuate fascicle',
    'lit_atr': 'Anterior Thalamic Radiation',
    'lit_cc': 'Corpus Callosum',
    'lit_cg': 'Cingulum',
    'lit_cst': 'Corticospinal tract',
    'lit_fpt': 'Fronto-pontine tract',
    'lit_icp': 'Inferior cerebellar peduncle',
    'lit_ifo': 'Inferior occipito-frontal fascicle',
    'lit_ilf': 'Inferior longitudinal fascicle',
    'lit_mcp': 'Middle cerebellar peduncle',
    'lit_or': 'Optic radiation',
    'lit_popt': 'Parieto‐occipital pontine',
    'lit_scp': 'Superior cerebellar peduncle',
    'lit_slf': 'Superior longitudinal fascicle',
    'lit_str': 'Superior Thalamic Radiation',
    'lit_uf': 'Uncinate fascicle',
    'lit_t_prem': 'Thalamo-premotor fibres',
    'lit_t_par': 'Thalamo-parietal fibres',
    'lit_t_occ': 'Thalamo-occipital fibres',
    'lit_st_fo': 'Striato-fronto-orbital fibres',
    'lit_st_prem': 'Striato-premotor fibres',
}

# Rename the columns using the updated dictionary
df = df.rename(columns=full_names)

#####NAWM######

# Define the specific tract names for each sublist
ON_tracts = ['diagnosis','Thalamo-occipital fibres','Optic radiation','Superior longitudinal fascicle', 'Inferior longitudinal fascicle']
TM_tracts = ['diagnosis','Superior Thalamic Radiation', 'Thalamo-premotor fibres', 'Striato-premotor fibres', 'Cingulum',
             'Corticospinal tract', 'Parieto‐occipital pontine','Fronto-pontine tract']
rest_tracts = ['diagnosis','Anterior Thalamic Radiation', 'Thalamo-parietal fibres', 'Striato-fronto-orbital fibres', 'Corpus Callosum', 'Middle cerebellar peduncle',
               'Inferior cerebellar peduncle', 'Superior cerebellar peduncle', 'Inferior occipito-frontal fascicle', 'Uncinate fascicle', 'Arcuate fascicle']
all_tracts = ['diagnosis', 'Arcuate fascicle','Anterior Thalamic Radiation', 'Corpus Callosum', 'Cingulum','Corticospinal tract','Fronto-pontine tract', 'Inferior cerebellar peduncle',
'Inferior occipito-frontal fascicle', 'Inferior longitudinal fascicle','Middle cerebellar peduncle','Optic radiation','Parieto‐occipital pontine', 'Superior cerebellar peduncle',
'Superior longitudinal fascicle','Superior Thalamic Radiation','Uncinate fascicle','Thalamo-premotor fibres','Thalamo-parietal fibres','Thalamo-occipital fibres','Striato-fronto-orbital fibres',
'Striato-premotor fibres']

# Filter the DataFrame based on the specified column names
ON_df = df.filter(ON_tracts)
TM_df = df.filter(TM_tracts)
rest_df = df.filter(rest_tracts)
all_df = df.filter(all_tracts)


group_order = ['HC', 'RRMS', 'NMOSD']
##################
###Plot for ALL####
# Create a figure with a 7x3 subplot grid
fig, axs = plt.subplots(nrows=3, ncols=7, figsize=(30, 20))

# Flatten the axs array for easier indexing
axs = axs.flatten()

# Iterate over the tracts and plot a boxplot for each tract in each subplot
for i, tract in enumerate(all_df.columns[1:]):
    
    # Create the boxplot
    pt.half_violinplot(data = all_df, width = .6, palette="Set2", ax=axs[i],x='diagnosis', y=tract, order=group_order)
    sns.stripplot(data = all_df, palette="Set2", ax=axs[i],x='diagnosis', y=tract,order=group_order)
    # plot the mean line
    sns.boxplot(showmeans=True,
                meanline=True,
                meanprops={'color': 'k', 'ls': '--', 'lw': 1.5},
                medianprops={'visible': False},
                whiskerprops={'visible': False},
                data=all_df,
                showfliers=False,
                showbox=False,
                showcaps=False,
                ax=axs[i],x='diagnosis', y=tract,
                order=group_order)
        
    #add horizontal grid lines
    axs[i].yaxis.grid(True)    
    axs[i].set_title(tract)
    axs[i].set(ylabel='NDI')

# Add a main title to the figure
fig.suptitle('Lesion-independent NDI values in MS, NMOSD and HC')

# Adjust spacing between subplots
fig.tight_layout()

# Show the plot
plt.show()





##################
###Plot for ON####
# Create a figure with a 7x3 subplot grid
fig, axs = plt.subplots(nrows=1, ncols=4, figsize=(30, 20))

# Flatten the axs array for easier indexing
axs = axs.flatten()

# Iterate over the tracts and plot a boxplot for each tract in each subplot
for i, tract in enumerate(ON_df.columns[1:]):
    
    # Create the boxplot
    pt.half_violinplot(data = ON_df, width = .6, palette="Set2", ax=axs[i],x='diagnosis', y=tract,)
    sns.stripplot(data = ON_df, palette="Set2", ax=axs[i],x='diagnosis', y=tract,)
    # plot the mean line
    sns.boxplot(showmeans=True,
                meanline=True,
                meanprops={'color': 'k', 'ls': '--', 'lw': 1.5},
                medianprops={'visible': False},
                whiskerprops={'visible': False},
                data=ON_df,
                showfliers=False,
                showbox=False,
                showcaps=False,
                ax=axs[i],x='diagnosis', y=tract)
        
    #add horizontal grid lines
    axs[i].yaxis.grid(True)    
    axs[i].set_title(tract)
    axs[i].set(ylabel='NDI')

# Add a main title to the figure
fig.suptitle('Lesion-independent NDI values in tracts possibly affected by optic neuritis')

# Adjust spacing between subplots
fig.tight_layout()

# Show the plot
plt.show()

#################
###Plot for TM###
# Create a figure with a 7x3 subplot grid
fig, axs = plt.subplots(nrows=1, ncols=7, figsize=(30, 20))

# Flatten the axs array for easier indexing
axs = axs.flatten()

# Iterate over the tracts and plot a boxplot for each tract in each subplot
for i, tract in enumerate(TM_df.columns[1:]):
    
    # Create the boxplot
    pt.half_violinplot(data = TM_df, width = .6, palette="Set2", ax=axs[i],x='diagnosis', y=tract,)
    sns.stripplot(data = TM_df, palette="Set2", ax=axs[i],x='diagnosis', y=tract,)
    # plot the mean line
    sns.boxplot(showmeans=True,
                meanline=True,
                meanprops={'color': 'k', 'ls': '--', 'lw': 1.5},
                medianprops={'visible': False},
                whiskerprops={'visible': False},
                data=TM_df,
                showfliers=False,
                showbox=False,
                showcaps=False,
                ax=axs[i],x='diagnosis', y=tract)
        
    #add horizontal grid lines
    axs[i].yaxis.grid(True)    
    axs[i].set_title(tract)
    axs[i].set(ylabel='NDI')
    
# Add a main title to the figure
fig.suptitle('Lesion-independent NDI values in tracts possibly affected by transverse myelitis')

# Adjust spacing between subplots
fig.tight_layout()

# Show the plot
plt.show()

###################
###Plot for rest###
# Create a figure with a 7x3 subplot grid
fig, axs = plt.subplots(nrows=2, ncols=5, figsize=(30, 20))

# Flatten the axs array for easier indexing
axs = axs.flatten()

# Iterate over the tracts and plot a boxplot for each tract in each subplot
for i, tract in enumerate(rest_df.columns[1:]):
    # Create the boxplot
    pt.half_violinplot(data = rest_df, width = .6, palette="Set2", ax=axs[i],x='diagnosis', y=tract,)
    sns.stripplot(data = rest_df, palette="Set2", ax=axs[i],x='diagnosis', y=tract,)
    # plot the mean line
    sns.boxplot(showmeans=True,
                meanline=True,
                meanprops={'color': 'k', 'ls': '--', 'lw': 1.5},
                medianprops={'visible': False},
                whiskerprops={'visible': False},
                data=rest_df,
                showfliers=False,
                showbox=False,
                showcaps=False,
                ax=axs[i],x='diagnosis', y=tract)
        
    #add horizontal grid lines
    axs[i].yaxis.grid(True)    
    axs[i].set_title(tract)
    axs[i].set(ylabel='NDI')

# Add a main title to the figure
fig.suptitle('Lesion-independent NDI values in tracts unaffected by optice neuritis or transverse myelitis')

# Adjust spacing between subplots
fig.tight_layout()

# Show the plot
plt.show()