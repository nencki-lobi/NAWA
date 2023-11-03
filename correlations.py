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
import statsmodels.stats.multitest as smm


# Set float_format to display up to 3 decimal places
pd.options.display.float_format = '{:.3f}'.format

path_to_write='/Volumes/ms/seropositive_project/'
# Set the folder name
folder_name = 'figures/'

# Create the folder if it doesn't exist
if not os.path.exists(path_to_write+folder_name):
    os.makedirs(path_to_write+folder_name)

path_to_write_plots='/Volumes/ms/seropositive_project/figures/BOOTSTRAPPING/'

# Create the folder if it doesn't exist
if not os.path.exists(path_to_write_plots):
    os.makedirs(path_to_write_plots)


#read in the data
df = pd.read_csv("/Volumes/ms/PJ_gRatio/Stata/data_ready.csv", sep=',')

# subset the dataframe based on the value in the 'group' column
group_MS = df[df['diagnosis'] == 'RRMS'].reset_index()
group_NMOSD = df[df['diagnosis'] == 'NMOSD'].reset_index()

###NMOSD

#subset data for correlation
NMOSD_LIT = group_NMOSD.loc[:,'lit_af_left':'lit_uf_right']

NMOSD_LD = group_NMOSD.loc[:,'ld_af_left':'ld_uf_right']

NMOSD_RAW = group_NMOSD.loc[:,'raw_af_left':'raw_uf_right']
'''
#make additional subsets of data with all tracts values pooled as total
NMOSD_LIT_total = NMOSD_LIT.mean(axis=1).to_frame(name='LIT_total')

NMOSD_LD_total = NMOSD_LD.mean(axis=1).to_frame(name='LD_total')

NMOSD_focal_total = NMOSD_focal.mean(axis=1).to_frame(name='focal_total')
'''
###Lesion_load_norm
NMOSD_LL = group_NMOSD.get(['lesion_load_norm'])
NMOSD_CL = group_NMOSD.get(['cl_count'])

###LIT
# Calculate the Spearman correlation and its p-value
# Create an empty DataFrame to store correlations
cor_NMOSD_LIT = pd.DataFrame(columns=['Comparison','Variable 1', 'Variable 2', 'Rho', 'P-Value'])

# Loop through each NDI variable in your DataFrame
for column_name in NMOSD_LIT:  # Skip the first column (lesion load)
    rho, p_value = stats.spearmanr(NMOSD_LL, NMOSD_LIT[column_name], nan_policy='omit')
    
    # Append the results to the correlation_df
    cor_NMOSD_LIT = pd.concat([cor_NMOSD_LIT, pd.DataFrame({'Comparison': ['NMOSD_LIT'],
                                                              'Variable 1': ['lesion_load'], 
                                                              'Variable 2': [column_name], 
                                                              'Rho': [rho], 
                                                              'P-Value': [p_value]})], 
                               ignore_index=True)


# Now, correlation_df contains the pairwise Spearman correlations
# between 'lesion_load' and each of the NDI variables

# Reset the index for the final result
cor_NMOSD_LIT.reset_index(drop=True, inplace=True)

##LIT cortical
# Calculate the Spearman correlation and its p-value
# Create an empty DataFrame to store correlations

# Loop through each NDI variable in your DataFrame
for column_name in NMOSD_LIT:  # Skip the first column (lesion load)
    rho, p_value = stats.spearmanr(NMOSD_CL, NMOSD_LIT[column_name], nan_policy='omit')
    
    # Append the results to the correlation_df
    cor_NMOSD_LIT = pd.concat([cor_NMOSD_LIT, pd.DataFrame({'Comparison': ['NMOSD_LIT'],
                                                              'Variable 1': ['cortical_lesion_count'], 
                                                              'Variable 2': [column_name], 
                                                              'Rho': [rho], 
                                                              'P-Value': [p_value]})], 
                               ignore_index=True)


# Now, correlation_df contains the pairwise Spearman correlations
# between 'lesion_load' and each of the NDI variables

# Reset the index for the final result
cor_NMOSD_LIT.reset_index(drop=True, inplace=True)

###RAW
# Calculate the Spearman correlation and its p-value
# Create an empty DataFrame to store correlations
cor_NMOSD_RAW = pd.DataFrame(columns=['Comparison','Variable 1', 'Variable 2', 'Rho', 'P-Value'])

# Loop through each NDI variable in your DataFrame
for column_name in NMOSD_RAW:  # Skip the first column (lesion load)
    rho, p_value = stats.spearmanr(NMOSD_LL, NMOSD_RAW[column_name], nan_policy='omit')
    
    # Append the results to the correlation_df
    cor_NMOSD_RAW = pd.concat([cor_NMOSD_RAW, pd.DataFrame({'Comparison': ['NMOSD_RAW'],
                                                              'Variable 1': ['lesion_load'], 
                                                              'Variable 2': [column_name], 
                                                              'Rho': [rho], 
                                                              'P-Value': [p_value]})], 
                               ignore_index=True)


# Now, correlation_df contains the pairwise Spearman correlations
# between 'lesion_load' and each of the NDI variables

# Reset the index for the final result
cor_NMOSD_RAW.reset_index(drop=True, inplace=True)





'''
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
'''

###MS

#subset data for correlation
MS_LIT = group_MS.loc[:,'lit_af_left':'lit_uf_right']

MS_LD = group_MS.loc[:,'ld_af_left':'ld_af_left']

MS_RAW = group_MS.loc[:,'raw_af_left':'raw_uf_right']
'''
#make additional subsets of data with all tracts values pooled as total
MS_LIT_total = MS_LIT.mean(axis=1).to_frame(name='LIT_total')

MS_LD_total = MS_LD.mean(axis=1).to_frame(name='LD_total')

MS_focal_total = MS_focal.mean(axis=1).to_frame(name='focal_total')
'''
#EDSS

#MS_edss = group_MS.get(['edss'])

##disease duration in years

#MS_dduration = group_MS.get(['disease_duration'])/12

###Lesion_load_norm
MS_LL = group_MS.get(['lesion_load_norm'])
MS_CL = group_MS.get(['cl_count'])

###LIT
# Calculate the Spearman correlation and its p-value
# Create an empty DataFrame to store correlations
cor_MS_LIT = pd.DataFrame(columns=['Comparison','Variable 1', 'Variable 2', 'Rho', 'P-Value'])

# Loop through each NDI variable in your DataFrame
for column_name in MS_LIT:  # Skip the first column (lesion load)
    rho, p_value = stats.spearmanr(MS_LL, MS_LIT[column_name], nan_policy='omit')
    
    # Append the results to the correlation_df
    cor_MS_LIT = pd.concat([cor_MS_LIT, pd.DataFrame({'Comparison': ['MS_LIT'],
                                                              'Variable 1': ['lesion_load'], 
                                                              'Variable 2': [column_name], 
                                                              'Rho': [rho], 
                                                              'P-Value': [p_value]})], 
                               ignore_index=True)


# Now, correlation_df contains the pairwise Spearman correlations
# between 'lesion_load' and each of the NDI variables

# Reset the index for the final result
cor_MS_LIT.reset_index(drop=True, inplace=True)

###LIT cortical lesions
# Calculate the Spearman correlation and its p-value

# Loop through each NDI variable in your DataFrame
for column_name in MS_LIT:  # Skip the first column (lesion load)
    rho, p_value = stats.spearmanr(MS_CL, MS_LIT[column_name], nan_policy='omit')
    
    # Append the results to the correlation_df
    cor_MS_LIT = pd.concat([cor_MS_LIT, pd.DataFrame({'Comparison': ['MS_LIT'],
                                                              'Variable 1': ['cortical_lesion_count'], 
                                                              'Variable 2': [column_name], 
                                                              'Rho': [rho], 
                                                              'P-Value': [p_value]})], 
                               ignore_index=True)


# Now, correlation_df contains the pairwise Spearman correlations
# between 'lesion_load' and each of the NDI variables

# Reset the index for the final result
cor_MS_LIT.reset_index(drop=True, inplace=True)


###RAW
# Calculate the Spearman correlation and its p-value
# Create an empty DataFrame to store correlations
cor_MS_RAW = pd.DataFrame(columns=['Comparison','Variable 1', 'Variable 2', 'Rho', 'P-Value'])

# Loop through each NDI variable in your DataFrame
for column_name in MS_RAW:  # Skip the first column (lesion load)
    rho, p_value = stats.spearmanr(MS_LL, MS_RAW[column_name], nan_policy='omit')
    
    # Append the results to the correlation_df
    cor_MS_RAW = pd.concat([cor_MS_RAW, pd.DataFrame({'Comparison': ['MS_RAW'],
                                                              'Variable 1': ['lesion_load'], 
                                                              'Variable 2': [column_name], 
                                                              'Rho': [rho], 
                                                              'P-Value': [p_value]})], 
                               ignore_index=True)


# Now, correlation_df contains the pairwise Spearman correlations
# between 'lesion_load' and each of the NDI variables

# Reset the index for the final result
cor_MS_RAW.reset_index(drop=True, inplace=True)
'''
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
'''

# Concatenate them vertically (along rows)
corr_df = pd.concat([cor_MS_LIT, cor_MS_RAW, cor_NMOSD_LIT, cor_NMOSD_RAW], axis=0)

# Reset the index of the concatenated DataFrame
corr_df.reset_index(drop=True, inplace=True)

#correct for multiple tests
# Correct for multiple comparisons using the FDR procedure and save results to PDF
p_vals_corr = smm.multipletests(corr_df['P-Value'], alpha=0.05, method='fdr_bh')[1]
#p_vals_corr = smm.multipletests(corr_df['P-Value'], alpha=0.05, method='bonferroni')[1]

corr_df['Corrected P-value'] = p_vals_corr

# Add asterisks to significant results
corr_df['Significance'] = ''
corr_df.loc[corr_df['Corrected P-value'] < 0.001, 'Significance'] = '***'
corr_df.loc[(corr_df['Corrected P-value'] >= 0.001) & (corr_df['Corrected P-value'] < 0.01), 'Significance'] = '**'
corr_df.loc[(corr_df['Corrected P-value'] >= 0.01) & (corr_df['Corrected P-value'] < 0.05), 'Significance'] = '*'


corr_df.to_csv('/Volumes/ms/seropositive_project/csv/Lesion_load_correlation_results_with_cortical.csv', index=False)

'''
###Fisher Z correlation comparison - not aplicable for this data as this is paired data and bootstrapping distribution symulations tests should be used
# Loop through each NDI variable in your DataFrame
for rho in MS_LIT:  # Skip the first column (lesion load)
    rho, p_value = stats.spearmanr(MS_LL, MS_LIT[column_name], nan_policy='omit')
    
    # Append the results to the correlation_df
    cor_MS_LIT = pd.concat([cor_MS_LIT, pd.DataFrame({'Comparison': ['MS_LIT'],
                                                              'Variable 1': ['lesion_load'], 
                                                              'Variable 2': [column_name], 
                                                              'Rho': [rho], 
                                                              'P-Value': [p_value]})], 
                               ignore_index=True)


# Now, correlation_df contains the pairwise Spearman correlations
# between 'lesion_load' and each of the NDI variables

# Reset the index for the final result
cor_MS_LIT.reset_index(drop=True, inplace=True)



# Create an empty list to store the results
results = []

# Iterate through the rows of both DataFrames
for index, row1 in cor_MS_LIT.iterrows():
    rho1 = row1['Rho']  # Replace 'rho' with the actual column name in df1
    rho2 = cor_MS_RAW.loc[index, 'Rho']  # Replace 'rho' with the actual column name in df2

    # Number of data points in each dataset
    N1 = 20  # Number of rows in df1
    N2 = 20  # Number of rows in df2

    # Fisher's z-transformation
    Z1 = 0.5 * (np.log(1 + rho1) - np.log(1 - rho1))
    Z2 = 0.5 * (np.log(1 + rho2) - np.log(1 - rho2))

    Z_diff = (Z1 - Z2) / np.sqrt( (1 / (N1 - 3)) + (1 / (N2 - 3)) )

    # Calculate the two-tailed p-value
    p_value = 2 * (1 - stats.norm.cdf(abs(Z_diff)))

    # Store the results
    results.append({'Row': index, 'Rho1': rho1, 'Rho2': rho2, 'P-Value': p_value})

'''



#####BOOTSTRAPING
# Set random seed for reproducibility
np.random.seed(2020)


###MS

# Define some constants
B = 10000  # Number of bootstrap replicates
n = group_MS.shape[0]  # Total sample size, assuming 'dat' is a DataFrame

bootstrap_df = pd.DataFrame(columns=['Comparison','Variable 1', 'Variable 2', 'deltaRho', 'Significant'])

for raw_column_name, lit_column_name in zip(MS_RAW, MS_LIT):
    # Your analysis or code for this column pair here
    # For example:
    print(f"Analyzing {raw_column_name} and {lit_column_name}")
    
    # Initialize an empty array for bootstrap statistics
    dstar = np.empty(B)
    
    # Run the bootstrap procedure
    for b in range(B):
        indices = np.random.choice(n, size=n, replace=True)
        bootsample = group_MS.iloc[indices]
        rho1 = stats.spearmanr(bootsample['lesion_load_norm'], bootsample[lit_column_name], nan_policy='omit')[0]
        rho2 = stats.spearmanr(bootsample['lesion_load_norm'], bootsample[raw_column_name], nan_policy='omit')[0]
        dstar[b] = rho1 - rho2
        # Debugging print statements
        print(f"Bootstrap Replicate {b+1}: rho1={rho1}, rho2={rho2}, dstar={dstar[b]}")
        
    # Append the results to the correlation_df
    bootstrap_df = pd.concat([bootstrap_df, pd.DataFrame({'Comparison': 'MS_LIT_vs_RAW',
                                                              'Variable 1': [raw_column_name], 
                                                              'Variable 2': [lit_column_name], 
                                                              'deltaRho': [rho1 - rho2]})], 
                                                              ignore_index=True)

    

    # Null hypothesis test statistic (you can modify this based on your hypothesis)
    null_value = 0.0
    
    # Compute empirical confidence intervals
    dstar.sort()
    confidence_interval = np.percentile(dstar, [2.5, 97.5])
 

    # Plot histogram
    plt.hist(dstar, bins=60, color='skyblue', edgecolor='black')
    plt.title(f"Difference in correlation coefficients {raw_column_name} vs {lit_column_name}")
    plt.xlabel("d*")

    # Display confidence interval as vertical lines
    plt.axvline(confidence_interval[0], linestyle='--', color='blue', label='2.5th Percentile')
    plt.axvline(confidence_interval[1], linestyle='--', color='blue', label='97.5th Percentile')

    # Display null value as a vertical line
    plt.axvline(null_value, linestyle='--', color='red', label='Null Value')
    
    # Add tight layout
    plt.tight_layout()

    # Show legend
    plt.legend()

    # Define the custom plot name
    plot_name = f"Correlation_Difference_{raw_column_name}_vs_{lit_column_name}.png"

    # Save the plot to the specified path    
    plt.savefig(path_to_write_plots + plot_name,dpi=300)

    # Close the plot to suppress displaying it
    plt.close()
    
    
    # Check significance by comparing null value to the confidence interval
    if null_value < confidence_interval[0] or null_value > confidence_interval[1]:
        print("Reject the null hypothesis")
        # Update the "Significant" column for the current row
        bootstrap_df.loc[bootstrap_df.index[-1], "Significant"] = "Yes"
    else:
        print("Fail to reject the null hypothesis")
        # Update the "Significant" column for the current row
        bootstrap_df.loc[bootstrap_df.index[-1], "Significant"] = "Nope"
        
bootstrap_df.to_csv('/Volumes/ms/seropositive_project/csv/corr_coefs_difference_MS_RAW_LIT_BOOTSTRAP_ZOU2007.csv', index=False)



###NMOSD

# Define some constants
B = 10000  # Number of bootstrap replicates
n = group_NMOSD.shape[0]  # Total sample size, assuming 'dat' is a DataFrame

bootstrap_df = pd.DataFrame(columns=['Comparison','Variable 1', 'Variable 2', 'deltaRho', 'Significant'])

for raw_column_name, lit_column_name in zip(NMOSD_RAW, NMOSD_LIT):
    # Your analysis or code for this column pair here
    # For example:
    print(f"Analyzing {raw_column_name} and {lit_column_name}")
    
    # Initialize an empty array for bootstrap statistics
    dstar = np.empty(B)
    
    # Run the bootstrap procedure
    for b in range(B):
        indices = np.random.choice(n, size=n, replace=True)
        bootsample = group_NMOSD.iloc[indices]
        rho1 = stats.spearmanr(bootsample['lesion_load_norm'], bootsample[lit_column_name], nan_policy='omit')[0]
        rho2 = stats.spearmanr(bootsample['lesion_load_norm'], bootsample[raw_column_name], nan_policy='omit')[0]
        dstar[b] = rho1 - rho2
        # Debugging print statements
        print(f"Bootstrap Replicate {b+1}: rho1={rho1}, rho2={rho2}, dstar={dstar[b]}")
        
    # Append the results to the correlation_df
    bootstrap_df = pd.concat([bootstrap_df, pd.DataFrame({'Comparison': 'NMOSD_LIT_vs_RAW',
                                                              'Variable 1': [raw_column_name], 
                                                              'Variable 2': [lit_column_name], 
                                                              'deltaRho': [rho1 - rho2]})], 
                                                              ignore_index=True)

    

    # Null hypothesis test statistic (you can modify this based on your hypothesis)
    null_value = 0.0
    
    # Compute empirical confidence intervals
    dstar.sort()
    confidence_interval = np.percentile(dstar, [2.5, 97.5])
 

    # Plot histogram
    plt.hist(dstar, bins=60, color='skyblue', edgecolor='black')
    plt.title(f"Difference in correlation coefficients {raw_column_name} vs {lit_column_name}")
    plt.xlabel("d*")

    # Display confidence interval as vertical lines
    plt.axvline(confidence_interval[0], linestyle='--', color='blue', label='2.5th Percentile')
    plt.axvline(confidence_interval[1], linestyle='--', color='blue', label='97.5th Percentile')

    # Display null value as a vertical line
    plt.axvline(null_value, linestyle='--', color='red', label='Null Value')
    
    # Add tight layout
    plt.tight_layout()

    # Show legend
    plt.legend()

    # Define the custom plot name
    plot_name = f"Correlation_Difference_{raw_column_name}_vs_{lit_column_name}_NMOSD.png"

    # Save the plot to the specified path    
    plt.savefig(path_to_write_plots + plot_name,dpi=300)

    # Close the plot to suppress displaying it
    plt.close()
    
    
    # Check significance by comparing null value to the confidence interval
    if null_value < confidence_interval[0] or null_value > confidence_interval[1]:
        print("Reject the null hypothesis")
        # Update the "Significant" column for the current row
        bootstrap_df.loc[bootstrap_df.index[-1], "Significant"] = "Yes"
    else:
        print("Fail to reject the null hypothesis")
        # Update the "Significant" column for the current row
        bootstrap_df.loc[bootstrap_df.index[-1], "Significant"] = "Nope"
        
bootstrap_df.to_csv('/Volumes/ms/seropositive_project/csv/corr_coefs_difference_NMOSD_RAW_LIT_BOOTSTRAP_ZOU2007.csv', index=False)


############PLOTS with overlap#########

####MS####
MS_boot= pd.read_csv('/Volumes/ms/seropositive_project/csv/corr_coefs_difference_MS_RAW_LIT_BOOTSTRAP_ZOU2007.csv')
significant_MS_boot_tracts = MS_boot.loc[MS_boot['Significant'] == 'Yes', 'Variable 1'].tolist()
significant_MS_boot_tracts = [value.replace('raw_', '') for value in significant_MS_boot_tracts]
# create a figure with two subplots
fig, ax = plt.subplots()

# plot the first subplot
sns.barplot(data=cor_MS_RAW, x='Variable 2', y='Rho', color="steelblue", ax=ax)

# plot the second subplot
sns.barplot(data=cor_MS_LIT, x='Variable 2', y='Rho', color="lightpink", ax=ax)


# rotate the x-axis ticks by 90 degrees
ax.set_xticklabels(cor_MS_LIT['Variable 2'].str.replace('lit_', ''), rotation=90)

# set the title and axis labels
ax.set_title("Comparison of correlation coefficients for lesion load and NDI values in tracts where lesions were not assessed and in tracts not traversing through lesions in RRMS")
ax.set_ylabel("Rho correlation coefficient")
ax.set_xlabel("Tracts")

# create a legend with color-coded labels
ax.legend(labels=['Correlation before taking lesions into account', 'Correlation in tracts not traversing throught lesions'], labelcolor=['steelblue', 'lightpink'], loc="upper right", handlelength=0)

plt.tight_layout()

## Bold xticklabels based on a condition (if xticklabel is in 'significant_MS_boot_tracts')
xticklabels = ax.get_xticklabels()  # Get the xticklabels

for label in xticklabels:
    tract_name = label.get_text()  # Get the text of the label
    if tract_name in significant_MS_boot_tracts:  # Check if the tract_name is in the list
        label.set_weight('bold')  # Set the label to bold

# show the plot
plt.show()

####NMOSD####
NMOSD_boot= pd.read_csv('/Volumes/ms/seropositive_project/csv/corr_coefs_difference_NMOSD_RAW_LIT_BOOTSTRAP_ZOU2007.csv')
significant_NMOSD_boot_tracts = NMOSD_boot.loc[NMOSD_boot['Significant'] == 'Yes', 'Variable 1'].tolist()
significant_NMOSD_boot_tracts = [value.replace('raw_', '') for value in significant_NMOSD_boot_tracts]
# create a figure with two subplots
fig, ax = plt.subplots()

# plot the first subplot
sns.barplot(data=cor_NMOSD_RAW, x='Variable 2', y='Rho', color="steelblue", ax=ax)

# plot the second subplot
sns.barplot(data=cor_NMOSD_LIT, x='Variable 2', y='Rho', color="lightpink", ax=ax)


# rotate the x-axis ticks by 90 degrees
ax.set_xticklabels(cor_NMOSD_LIT['Variable 2'].str.replace('lit_', ''), rotation=90)

# set the title and axis labels
ax.set_title("Comparison of correlation coefficients for lesion load and NDI values in tracts where lesions were not assessed and in tracts not traversing through lesions in NMOSD")
ax.set_ylabel("Rho correlation coefficient")
ax.set_xlabel("Tracts")

# create a legend with color-coded labels
ax.legend(labels=['Correlation before taking lesions into account', 'Correlation in tracts not traversing throught lesions'], labelcolor=['steelblue', 'lightpink'], loc="upper right", handlelength=0)

plt.tight_layout()

## Bold xticklabels based on a condition (if xticklabel is in 'significant_NMOSD_boot_tracts')
xticklabels = ax.get_xticklabels()  # Get the xticklabels

for label in xticklabels:
    tract_name = label.get_text()  # Get the text of the label
    if tract_name in significant_NMOSD_boot_tracts:  # Check if the tract_name is in the list
        label.set_weight('bold')  # Set the label to bold

# show the plot
plt.show()