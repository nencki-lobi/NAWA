#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 12:00:24 2023

@author: paweljakuszyk 
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from scipy.stats import ttest_ind
import statsmodels.stats.multitest as smm
from scipy.stats import mannwhitneyu
from statannotations.Annotator import Annotator

np.set_printoptions(precision=8, suppress=True, formatter={'float': '{: 0.8e}'.format})


SM_patients =[
'NAWA_010',
'NAWA_035',
'NAWA_018',
'NAWA_002_MS_F_TP1',
'NAWA_059',
'NAWA_064',
'NAWA_066',
'NAWA_052',
'Nawa_058',
'NAWA_049',
'NAWA_054',
'NAWA_047',
'NAWA_008',
'NAWA_003_MS_M_TP1',
'001_MS_F_TP1',
'NAWA_061',
'NAWA_023',
'NAWA_063',
'NAWA_062',
'NAWA_065'
]
      

# list to store each participant's data
SM_bundles = []

# loop through each participant
for SM_patient in SM_patients:
    # read participant's csv file into a dataframe
    df = pd.read_csv(f"/Volumes/pjakuszyk/seropositive_project/participants/{SM_patient}/Brain/DWI/bundle_loads/BundleLoad.csv", header=None)
    
    # add participant id column to the dataframe
    df['Participant'] = SM_patient
    
    df.columns = ['Bundle', 'Bundle_Load', 'Participant']

    # append participant's data to the list
    SM_bundles.append(df)

# concatenate all participant's data into a single dataframe
SM_bundles_all = pd.concat(SM_bundles)
SM_bundles_long = pd.concat(SM_bundles)

# pivot the dataframe to wide format
SM_bundles_all = SM_bundles_all.pivot(index='Participant', columns='Bundle', values='Bundle_Load')

# save the result to a new csv file
SM_bundles_all.to_csv('/Volumes/pjakuszyk/seropositive_project/SM_bundles.csv', index=False)

#calculate the mean

bundle_means=SM_bundles_all.mean().to_frame().reset_index()
bundle_means.columns = ['Bundle', 'Bundle_Load_mean']

bundle_sds=SM_bundles_all.std().to_frame().reset_index()
bundle_sds.columns = ['Bundle', 'Bundle_Load_sd']

SM_bundles_to_plot=pd.merge(bundle_means, bundle_sds, on='Bundle')

#SM_bundles_to_plot=SM_bundles_to_plot.sort_values(by='Bundle_Load_mean', ascending=False)


#Plot the avergae bundle load
sns.barplot(data=SM_bundles_to_plot, x='Bundle', y='Bundle_Load_mean', yerr=pd.to_numeric(SM_bundles_to_plot['Bundle_Load_sd'], errors='coerce'))
# Add labels and title to the plot
plt.xticks(rotation=90)
plt.xlabel('Bundle')
plt.ylabel('Average Bundle Load')
plt.title('MS patients')
# Show the plot
plt.show()
  
        

NMO_patients =[
'NAWA_032',
'NAWA_043',
'NAWA_031',
'NAWA_025',
'Nawa_056',
'NAWA_028',
'NAWA_026',
'NAWA_067',
'NAWA_038',
'NAWA_033',
'NAWA_024',
'NAWA_022',
'NAWA_055',
'NAWA_051',
'NAWA_011',
'NAWA_021',
'NAWA_037',
'NAWA_040',
'Nawa_042',
'NAWA_036'
]

# list to store each participant's data
NMO_bundles = []

# loop through each participant
for NMO_patient in NMO_patients:
    file_path = f"/Volumes/pjakuszyk/seropositive_project/participants/{NMO_patient}/Brain/DWI/bundle_loads/BundleLoad.csv"
    # check if file exists
    if os.path.exists(file_path):
        # read participant's csv file into a dataframe
        df = pd.read_csv(file_path, header=None)

        # add participant id column to the dataframe
        df['Participant'] = NMO_patient
        
        df.columns = ['Bundle', 'Bundle_Load', 'Participant']
        
        # append participant's data to the list
        NMO_bundles.append(df)
    else:
        # create an empty dataframe with columns Bundle, Bundle_Load, and Participant
        df = pd.read_csv("/Volumes/pjakuszyk/seropositive_project/BundleLoad_empty.csv", header=None, sep=';')

        # add participant id to the empty dataframe
        df['Participant'] = NMO_patient

        df.columns = ['Bundle', 'Bundle_Load', 'Participant']
        
        # append empty dataframe to the list
        NMO_bundles.append(df)


# concatenate all participant's data into a single dataframe
NMO_bundles_all = pd.concat(NMO_bundles)
NMO_bundles_long = pd.concat(NMO_bundles)

# pivot the dataframe to wide format
NMO_bundles_all = NMO_bundles_all.pivot(index='Participant', columns='Bundle', values='Bundle_Load')

# Find the mean of col1 and col2 for all rows except row i
col1_mean = np.mean(NMO_bundles_all.loc[NMO_bundles_all.index != 'NAWA_036', 'CC_4'])
col2_mean = np.mean(NMO_bundles_all.loc[NMO_bundles_all.index != 'NAWA_036', 'STR_left'])

# Fill the NaN values in row i for col1 and col2 with the means
if np.isnan(NMO_bundles_all.loc['NAWA_036', 'CC_4']):
    NMO_bundles_all.loc['NAWA_036', 'CC_4'] = col1_mean

if np.isnan(NMO_bundles_all.loc['NAWA_036', 'STR_left']):
    NMO_bundles_all.loc['NAWA_036', 'STR_left'] = col2_mean

# save the result to a new csv file
NMO_bundles_all.to_csv('/Volumes/pjakuszyk/seropositive_project/NMO_bundles.csv', index=False)

#calculate the mean

bundle_means=NMO_bundles_all.mean().to_frame().reset_index()
bundle_means.columns = ['Bundle', 'Bundle_Load_mean']

bundle_sds=NMO_bundles_all.std().to_frame().reset_index()
bundle_sds.columns = ['Bundle', 'Bundle_Load_sd']

NMO_bundles_to_plot=pd.merge(bundle_means, bundle_sds, on='Bundle')

#NMO_bundles_to_plot=NMO_bundles_to_plot.sort_values(by='Bundle_Load_mean', ascending=False)

#Plot the avergae bundle load
sns.barplot(data=NMO_bundles_to_plot, x='Bundle', y='Bundle_Load_mean', yerr=pd.to_numeric(NMO_bundles_to_plot['Bundle_Load_sd'], errors='coerce'))
# Add labels and title to the plot
plt.xticks(rotation=90)
plt.xlabel('Bundle')
plt.ylabel('Average Bundle Load')
plt.title('NMOSD patients')
# Show the plot
plt.show()

# create a figure with two subplots
fig, ax = plt.subplots()

# plot the first subplot
sns.barplot(data=SM_bundles_to_plot, x='Bundle', y='Bundle_Load_mean', color="steelblue", ax=ax)

# plot the second subplot
sns.barplot(data=NMO_bundles_to_plot, x='Bundle', y='Bundle_Load_mean', color="lightpink", ax=ax)


# rotate the x-axis ticks by 90 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

# set the title and axis labels
ax.set_title("Average Bundle Load in MS and NMOSD")
ax.set_ylabel("Average Bundle Load")

# create a legend with color-coded labels
ax.legend(labels=['MS', 'NMOSD'], labelcolor=['steelblue', 'lightpink'], title="Disease", loc="upper right", handlelength=0)

# show the plot
plt.show()

####Do a t-test and visualize the data####

# Combine the two dataframes and add a 'Disease' column to identify the two groups
data_df = pd.concat([SM_bundles_all, NMO_bundles_all], ignore_index=True)
data_df['Disease'] = ['MS']*len(SM_bundles_all) + ['NMOSD']*len(NMO_bundles_all)



# Perform a Mann-Whitney U test for each tract
p_vals = []
for bundle in SM_bundles_all.columns:
    t_stat, p_val = mannwhitneyu(SM_bundles_all.loc[:, bundle], NMO_bundles_all.loc[:, bundle], alternative='two-sided')
    p_vals.append(p_val)
    if p_val < 0.001:
       p_string = '***'
    elif p_val < 0.01:
       p_string = '**'
    elif p_val < 0.05:
       p_string = '*'
    else:
       p_string = ''       
    
    print(f"Bundle: {bundle}, T-value: {t_stat:.3f}, P-value: {p_val:.3f}{p_string}")
    

# Correct for multiple comparisons using the Bonferroni procedure
p_vals_corr = smm.multipletests(p_vals, alpha=0.05, method='bonferroni_holm')[1]








