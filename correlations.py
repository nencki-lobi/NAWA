#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 10:01:55 2023

@author: paweljakuszyk
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import scipy.stats as stats

# Set float_format to display up to 3 decimal places
pd.options.display.float_format = '{:.3f}'.format

path_to_write='/Volumes/ms/seropositive_project/'
# Set the folder name
folder_name = 'figures/'

# Create the folder if it doesn't exist
if not os.path.exists(path_to_write+folder_name):
    os.makedirs(path_to_write+folder_name)

#read in the data
df = pd.read_csv("/Volumes/ms/PJ_gRatio/Stata/data_ready.csv", sep=',')

# subset the dataframe based on the value in the 'group' column
group_MS = df[df['diagnosis'] == 'RRMS'].reset_index()
group_NMOSD = df[df['diagnosis'] == 'NMOSD'].reset_index()

###NMOSD

#subset data for correlation
NMOSD_LIT = group_NMOSD.loc[:,'lit_af':'lit_slf']

NMOSD_LD = group_NMOSD.loc[:,'ld_af':'ld_slf']

NMOSD_focal = group_NMOSD.loc[:,'ld_af_focal':'ld_slf_focal']

#make additional subsets of data with all tracts values pooled as total
NMOSD_LIT_total = NMOSD_LIT.mean(axis=1).to_frame(name='LIT_total')

NMOSD_LD_total = NMOSD_LD.mean(axis=1).to_frame(name='LD_total')

NMOSD_focal_total = NMOSD_focal.mean(axis=1).to_frame(name='focal_total')

##EDSS

NMOSD_edss = group_NMOSD.get(['edss'])

##disease duration in years

NMOSD_dduration = group_NMOSD.get(['disease_duration'])/12

#make correlations for pooled-total data
#EDSS LIT
# Calculate the Spearman correlation and its p-value
corr, p_value = stats.spearmanr(NMOSD_edss, NMOSD_LIT_total, nan_policy='omit')
# Print the results in ADF format
print(f"Spearman correlation coefficient NMOSD, EDSS, LIT (r) = {corr:.4f}, p-value = {p_value:.4f}")
#EDSS LD
# Calculate the Spearman correlation and its p-value
corr, p_value = stats.spearmanr(NMOSD_edss, NMOSD_LD_total, nan_policy='omit')
# Print the results in ADF format
print(f"Spearman correlation coefficient NMOSD, EDSS, LD (r) = {corr:.4f}, p-value = {p_value:.4f}")
#EDSS focal
# Calculate the Spearman correlation and its p-value
corr, p_value = stats.spearmanr(NMOSD_edss, NMOSD_focal_total, nan_policy='omit')
# Print the results in ADF format
print(f"Spearman correlation coefficient NMOSD, EDSS, focal (r) = {corr:.4f}, p-value = {p_value:.4f}")

#DD LIT
# Calculate the Spearman correlation and its p-value
corr, p_value = stats.spearmanr(NMOSD_dduration, NMOSD_LIT_total, nan_policy='omit')
# Print the results in ADF format
print(f"Spearman correlation coefficient NMOSD, DD, LIT (r) = {corr:.4f}, p-value = {p_value:.4f}")
#DD LD
# Calculate the Spearman correlation and its p-value
corr, p_value = stats.spearmanr(NMOSD_dduration, NMOSD_LD_total, nan_policy='omit')
# Print the results in ADF format
print(f"Spearman correlation coefficient NMOSD, DD, LD (r) = {corr:.4f}, p-value = {p_value:.4f}")
#DD focal
# Calculate the Spearman correlation and its p-value
corr, p_value = stats.spearmanr(NMOSD_dduration, NMOSD_focal_total, nan_policy='omit')
# Print the results in ADF format
print(f"Spearman correlation coefficient NMOSD, DD, focal (r) = {corr:.4f}, p-value = {p_value:.4f}")

#create scatterplots

#####EDSS#####

#edss LIT
# create a 3x7 grid of subplots
fig, axes = plt.subplots(nrows=3, ncols=7, figsize=(20, 10))
# Flatten the axs array for easier indexing
axes = axes.flatten()
# iterate over each variable in each group and plot its correlation
for i, tract in enumerate(NMOSD_LIT.columns):
    sns.regplot(x=NMOSD_LIT[tract], y=NMOSD_edss['edss'], ax=axes[i], color='green')
    axes[i].set_xlabel(tract) 
# Add a main title to the figure
fig.suptitle('Correlations of lesion-independent NDI values with EDSS - NMOSD')
# Adjust spacing between subplots
fig.tight_layout()
#save figure
plt.savefig(path_to_write + folder_name + 'NMOSD_edss_LIT_correlation_plots.png')

#edss LD
# create a 3x7 grid of subplots
fig, axes = plt.subplots(nrows=3, ncols=7, figsize=(20, 10))
# Flatten the axs array for easier indexing
axes = axes.flatten()
# iterate over each variable in each group and plot its correlation
for i, tract in enumerate(NMOSD_LD.columns):
    sns.regplot(x=NMOSD_LD[tract], y=NMOSD_edss['edss'], ax=axes[i], color='green')
    axes[i].set_xlabel(tract) 
# Add a main title to the figure
fig.suptitle('Correlations of lesion-dependent NDI values with EDSS - NMOSD')
# Adjust spacing between subplots
fig.tight_layout()
#save figure
plt.savefig(path_to_write + folder_name + 'NMOSD_edss_LD_correlation_plots.png')

#edss focal
# create a 3x7 grid of subplots
fig, axes = plt.subplots(nrows=3, ncols=7, figsize=(20, 10))
# Flatten the axs array for easier indexing
axes = axes.flatten()
# iterate over each variable in each group and plot its correlation
for i, tract in enumerate(NMOSD_focal.columns):
    sns.regplot(x=NMOSD_focal[tract], y=NMOSD_edss['edss'], ax=axes[i], color='green')
    axes[i].set_xlabel(tract) 
# Add a main title to the figure
fig.suptitle('Correlations of NDI values within lesions with EDSS - NMOSD')
# Adjust spacing between subplots
fig.tight_layout()
#save figure
plt.savefig(path_to_write + folder_name + 'NMOSD_edss_focal_correlation_plots.png')

#####DIESEASE DURATION#####

#dd LIT
# create a 3x7 grid of subplots
fig, axes = plt.subplots(nrows=3, ncols=7, figsize=(20, 10))
# Flatten the axs array for easier indexing
axes = axes.flatten()
# iterate over each variable in each group and plot its correlation
for i, tract in enumerate(NMOSD_LIT.columns):
    sns.regplot(x=NMOSD_LIT[tract], y=NMOSD_dduration['disease_duration'], ax=axes[i], color='green')
    axes[i].set_xlabel(tract) 
# Add a main title to the figure
fig.suptitle('Correlations of lesion-independent NDI values with disease duration - NMOSD')
# Adjust spacing between subplots
fig.tight_layout()
#save figure
plt.savefig(path_to_write + folder_name + 'NMOSD_DD_LIT_correlation_plots.png')

#dd LD
# create a 3x7 grid of subplots
fig, axes = plt.subplots(nrows=3, ncols=7, figsize=(20, 10))
# Flatten the axs array for easier indexing
axes = axes.flatten()
# iterate over each variable in each group and plot its correlation
for i, tract in enumerate(NMOSD_LD.columns):
    sns.regplot(x=NMOSD_LD[tract], y=NMOSD_dduration['disease_duration'], ax=axes[i], color='green')
    axes[i].set_xlabel(tract) 
# Add a main title to the figure
fig.suptitle('Correlations of lesion-dependent NDI values with disease duration - NMOSD')
# Adjust spacing between subplots
fig.tight_layout()
#save figure
plt.savefig(path_to_write + folder_name + 'NMOSD_DD_LD_correlation_plots.png')

#dd focal
# create a 3x7 grid of subplots
fig, axes = plt.subplots(nrows=3, ncols=7, figsize=(20, 10))
# Flatten the axs array for easier indexing
axes = axes.flatten()
# iterate over each variable in each group and plot its correlation
for i, tract in enumerate(NMOSD_focal.columns):
    sns.regplot(x=NMOSD_focal[tract], y=NMOSD_dduration['disease_duration'], ax=axes[i], color='green')
    axes[i].set_xlabel(tract) 
# Add a main title to the figure
fig.suptitle('Correlations of NDI values within lesions with disease duration - NMOSD')
# Adjust spacing between subplots
fig.tight_layout()
#save figure
plt.savefig(path_to_write + folder_name + 'NMOSD_DD_focal_correlation_plots.png')

###POOLED TOTAL DATA

# create a 3x2 grid of subplots
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(20, 10))
# Flatten the axs array for easier indexing
axes = axes.flatten()
# make subplots
#EDSS
sns.regplot(x=NMOSD_LIT_total['LIT_total'], y=NMOSD_edss['edss'], ax=axes[0], color='green')

sns.regplot(x=NMOSD_LD_total['LD_total'], y=NMOSD_edss['edss'], ax=axes[1], color='green')

sns.regplot(x=NMOSD_focal_total['focal_total'], y=NMOSD_edss['edss'], ax=axes[2], color='green')
##DD
sns.regplot(x=NMOSD_LIT_total['LIT_total'], y=NMOSD_dduration['disease_duration'], ax=axes[3], color='green')

sns.regplot(x=NMOSD_LD_total['LD_total'], y=NMOSD_dduration['disease_duration'], ax=axes[4], color='green')

sns.regplot(x=NMOSD_focal_total['focal_total'], y=NMOSD_dduration['disease_duration'], ax=axes[5], color='green')

# Add a main title to the figure
fig.suptitle('Correlations of total NDI values - NMOSD')
# Adjust spacing between subplots
fig.tight_layout()
#save figure
plt.savefig(path_to_write + folder_name + 'NMOSD_total_correlation_plots.png')


###MS

#subset data for correlation
MS_LIT = group_MS.loc[:,'lit_af':'lit_slf']

MS_LD = group_MS.loc[:,'ld_af':'ld_slf']

MS_focal = group_MS.loc[:,'ld_af_focal':'ld_slf_focal']

#make additional subsets of data with all tracts values pooled as total
MS_LIT_total = MS_LIT.mean(axis=1).to_frame(name='LIT_total')

MS_LD_total = MS_LD.mean(axis=1).to_frame(name='LD_total')

MS_focal_total = MS_focal.mean(axis=1).to_frame(name='focal_total')

##EDSS

MS_edss = group_MS.get(['edss'])

##disease duration in years

MS_dduration = group_MS.get(['disease_duration'])/12

#make correlations for pooled-total data
#EDSS LIT
# Calculate the Spearman correlation and its p-value
corr, p_value = stats.spearmanr( MS_edss,  MS_LIT_total, nan_policy='omit')
# Print the results in ADF format
print(f"Spearman correlation coefficient  MS, EDSS, LIT (r) = {corr:.4f}, p-value = {p_value:.4f}")
#EDSS LD
# Calculate the Spearman correlation and its p-value
corr, p_value = stats.spearmanr( MS_edss,  MS_LD_total, nan_policy='omit')
# Print the results in ADF format
print(f"Spearman correlation coefficient  MS, EDSS, LD (r) = {corr:.4f}, p-value = {p_value:.4f}")
#EDSS focal
# Calculate the Spearman correlation and its p-value
corr, p_value = stats.spearmanr( MS_edss,  MS_focal_total, nan_policy='omit')
# Print the results in ADF format
print(f"Spearman correlation coefficient  MS, EDSS, focal (r) = {corr:.4f}, p-value = {p_value:.4f}")

#DD LIT
# Calculate the Spearman correlation and its p-value
corr, p_value = stats.spearmanr( MS_dduration,  MS_LIT_total, nan_policy='omit')
# Print the results in ADF format
print(f"Spearman correlation coefficient  MS, DD, LIT (r) = {corr:.4f}, p-value = {p_value:.4f}")
#DD LD
# Calculate the Spearman correlation and its p-value
corr, p_value = stats.spearmanr( MS_dduration,  MS_LD_total, nan_policy='omit')
# Print the results in ADF format
print(f"Spearman correlation coefficient  MS, DD, LD (r) = {corr:.4f}, p-value = {p_value:.4f}")
#DD focal
# Calculate the Spearman correlation and its p-value
corr, p_value = stats.spearmanr( MS_dduration,  MS_focal_total, nan_policy='omit')
# Print the results in ADF format
print(f"Spearman correlation coefficient  MS, DD, focal (r) = {corr:.4f}, p-value = {p_value:.4f}")

#create scatterplots

#####EDSS#####

#edss LIT
# create a 3x7 grid of subplots
fig, axes = plt.subplots(nrows=3, ncols=7, figsize=(20, 10))
# Flatten the axs array for easier indexing
axes = axes.flatten()
# iterate over each variable in each group and plot its correlation
for i, tract in enumerate(MS_LIT.columns):
    sns.regplot(x=MS_LIT[tract], y=MS_edss['edss'], ax=axes[i])
    axes[i].set_xlabel(tract) 
# Add a main title to the figure
fig.suptitle('Correlations of lesion-independent NDI values with EDSS - MS')
# Adjust spacing between subplots
fig.tight_layout()
#save figure
plt.savefig(path_to_write + folder_name + 'MS_edss_LIT_correlation_plots.png')

#edss LD
# create a 3x7 grid of subplots
fig, axes = plt.subplots(nrows=3, ncols=7, figsize=(20, 10))
# Flatten the axs array for easier indexing
axes = axes.flatten()
# iterate over each variable in each group and plot its correlation
for i, tract in enumerate(MS_LD.columns):
    sns.regplot(x=MS_LD[tract], y=MS_edss['edss'], ax=axes[i])
    axes[i].set_xlabel(tract) 
# Add a main title to the figure
fig.suptitle('Correlations of lesion-dependent NDI values with EDSS - MS')
# Adjust spacing between subplots
fig.tight_layout()
#save figure
plt.savefig(path_to_write + folder_name + 'MS_edss_LD_correlation_plots.png')

#edss focal
# create a 3x7 grid of subplots
fig, axes = plt.subplots(nrows=3, ncols=7, figsize=(20, 10))
# Flatten the axs array for easier indexing
axes = axes.flatten()
# iterate over each variable in each group and plot its correlation
for i, tract in enumerate(MS_focal.columns):
    sns.regplot(x=MS_focal[tract], y=MS_edss['edss'], ax=axes[i])
    axes[i].set_xlabel(tract) 
# Add a main title to the figure
fig.suptitle('Correlations of NDI values within lesions with EDSS - MS')
# Adjust spacing between subplots
fig.tight_layout()
#save figure
plt.savefig(path_to_write + folder_name + 'MS_edss_focal_correlation_plots.png')

#####DIESEASE DURATION#####

#dd LIT
# create a 3x7 grid of subplots
fig, axes = plt.subplots(nrows=3, ncols=7, figsize=(20, 10))
# Flatten the axs array for easier indexing
axes = axes.flatten()
# iterate over each variable in each group and plot its correlation
for i, tract in enumerate(MS_LIT.columns):
    sns.regplot(x=MS_LIT[tract], y=MS_dduration['disease_duration'], ax=axes[i])
    axes[i].set_xlabel(tract) 
# Add a main title to the figure
fig.suptitle('Correlations of lesion-independent NDI values with disease duration - MS')
# Adjust spacing between subplots
fig.tight_layout()
#save figure
plt.savefig(path_to_write + folder_name + 'MS_DD_LIT_correlation_plots.png')

#dd LD
# create a 3x7 grid of subplots
fig, axes = plt.subplots(nrows=3, ncols=7, figsize=(20, 10))
# Flatten the axs array for easier indexing
axes = axes.flatten()
# iterate over each variable in each group and plot its correlation
for i, tract in enumerate(MS_LD.columns):
    sns.regplot(x=MS_LD[tract], y=MS_dduration['disease_duration'], ax=axes[i])
    axes[i].set_xlabel(tract) 
# Add a main title to the figure
fig.suptitle('Correlations of lesion-dependent NDI values with disease duration - MS')
# Adjust spacing between subplots
fig.tight_layout()
#save figure
plt.savefig(path_to_write + folder_name + 'MS_DD_LD_correlation_plots.png')

#dd focal
# create a 3x7 grid of subplots
fig, axes = plt.subplots(nrows=3, ncols=7, figsize=(20, 10))
# Flatten the axs array for easier indexing
axes = axes.flatten()
# iterate over each variable in each group and plot its correlation
for i, tract in enumerate(MS_focal.columns):
    sns.regplot(x=MS_focal[tract], y=MS_dduration['disease_duration'], ax=axes[i])
    axes[i].set_xlabel(tract) 
# Add a main title to the figure
fig.suptitle('Correlations of NDI values within lesions with disease duration - MS')
# Adjust spacing between subplots
fig.tight_layout()
#save figure
plt.savefig(path_to_write + folder_name + 'MS_DD_focal_correlation_plots.png')

###POOLED TOTAL DATA

# create a 3x2 grid of subplots
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(20, 10))
# Flatten the axs array for easier indexing
axes = axes.flatten()
# make subplots
#EDSS
sns.regplot(x=MS_LIT_total['LIT_total'], y=MS_edss['edss'], ax=axes[0] )

sns.regplot(x=MS_LD_total['LD_total'], y=MS_edss['edss'], ax=axes[1] )

sns.regplot(x=MS_focal_total['focal_total'], y=MS_edss['edss'], ax=axes[2] )
##DD
sns.regplot(x=MS_LIT_total['LIT_total'], y=MS_dduration['disease_duration'], ax=axes[3] )

sns.regplot(x=MS_LD_total['LD_total'], y=MS_dduration['disease_duration'], ax=axes[4] )

sns.regplot(x=MS_focal_total['focal_total'], y=MS_dduration['disease_duration'], ax=axes[5] )

# Add a main title to the figure
fig.suptitle('Correlations of total NDI values - MS')
# Adjust spacing between subplots
fig.tight_layout()
#save figure
plt.savefig(path_to_write + folder_name + 'MS_total_correlation_plots.png')







