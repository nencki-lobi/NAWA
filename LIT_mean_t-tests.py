#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 15:31:02 2023

@author: paweljakuszyk
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from reportlab.pdfgen import canvas
from scipy.stats import ttest_ind
import statsmodels.stats.multitest as smm
from scipy.stats import mannwhitneyu

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
SM_bundles_long = []
# loop through each participant
for SM_patient in SM_patients:
    # read participant's csv file into a dataframe
    df = pd.read_csv(f"/Volumes/pjakuszyk/seropositive_project/participants/{SM_patient}/Brain/DWI/tractseg_output/Tractometry_NAWM_NODDI_ND_substituted.csv", sep=';')
    
    # make a mean out of the 100 points sampled per tract 
    df = df.mean().to_frame().reset_index()
    # add participant id column to the dataframe
    df['Participant'] = SM_patient
    # bring it from long to wide format
    df_pivot = df.pivot(index='Participant', columns='index', values=0)

    # append participant's data to the list
    SM_bundles.append(df_pivot)
    SM_bundles_long.append(df)

# concatenate all participant's data into a single dataframe
SM_bundles_all = pd.concat(SM_bundles)
SM_bundles_long = pd.concat(SM_bundles_long)

# save the result to a new csv file
SM_bundles_all.to_csv('/Volumes/pjakuszyk/seropositive_project/SM_tracts_mean_NDI.csv', index=False)


#Plot the avergae bundle load
sns.barplot(data=SM_bundles_long, x='index', y=0)
# Add labels and title to the plot
plt.xticks(rotation=90)
plt.xlabel('Bundle')
plt.ylabel('Average NDI per bundle')
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
NMO_bundles_long = []
# loop through each participant
for NMO_patient in NMO_patients:
    # read participant's csv file into a dataframe
    df = pd.read_csv(f"/Volumes/pjakuszyk/seropositive_project/participants/{NMO_patient}/Brain/DWI/tractseg_output/Tractometry_NAWM_NODDI_ND_substituted.csv", sep=';')
    df = df.mean().to_frame().reset_index()
    # add participant id column to the dataframe
    df['Participant'] = NMO_patient
    # bring it from long to wide format
    df_pivot = df.pivot(index='Participant', columns='index', values=0)

    # append participant's data to the list
    NMO_bundles.append(df_pivot)
    NMO_bundles_long.append(df)

# concatenate all participant's data into a single dataframe
NMO_bundles_all = pd.concat(NMO_bundles)
NMO_bundles_long = pd.concat(NMO_bundles_long)

# save the result to a new csv file
NMO_bundles_all.to_csv('/Volumes/pjakuszyk/seropositive_project/NMO_tracts_mean_NDI.csv', index=False)


#Plot the avergae bundle load
sns.barplot(data=NMO_bundles_long, x='index', y=0)
# Add labels and title to the plot
plt.xticks(rotation=90)
plt.xlabel('Bundle')
plt.ylabel('Average NDI per bundle')
plt.title('NMOSD patients')
# Show the plot
plt.show()

#### create a figure with two subplots #####
fig, ax = plt.subplots()

# plot the first subplot
sns.barplot(data=NMO_bundles_long, x='index', y=0, color="lightpink", ax=ax, ci=None)

# plot the second subplot
sns.barplot(data=SM_bundles_long, x='index', y=0, color="steelblue", ax=ax, ci=None)


# rotate the x-axis ticks by 90 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

# set scale for y
ax.set(ylim=(0.4, 0.8))

# set the title and axis labels
ax.set_title("NDI in MS and NMOSD")
ax.set_ylabel("Mean NDI per tract")

# create a legend with color-coded labels
ax.legend(labels=['NMOSD','MS'], labelcolor=['lightpink','steelblue' ], title="Disease", loc="upper right", handlelength=0)

# show the plot
plt.show()

HC=[
'NAWA_045',
'NAWA_060',
'NAWA_013',
'NAWA_044',
'NAWA_050',
'NAWA_048',
'NAWA_029',
'NAWA_34',
'nawa_041',
'NAWA_030',
'NAWA_012',
'NAWA_053',
'NAWA_016',
'NAWA_015',
'NAWA_017',
'NAWA_014',
'NAWA_046',
'NAWA_020',
'NAWA_039',
'NAWA_057']

# list to store each participant's data
HC_bundles = []
HC_bundles_long = []
# loop through each participant
for subject in HC:
    # read participant's csv file into a dataframe
    df = pd.read_csv(f"/Volumes/pjakuszyk/seropositive_project/participants/{subject}/Brain/DWI/tractseg_output/Tractometry_NAWM_NODDI_ND_substituted.csv", sep=';')
    df = df.mean().to_frame().reset_index()
    # add participant id column to the dataframe
    df['Participant'] = subject
    # bring it from long to wide format
    df_pivot = df.pivot(index='Participant', columns='index', values=0)

    # append participant's data to the list
    HC_bundles.append(df_pivot)
    HC_bundles_long.append(df)

# concatenate all participant's data into a single dataframe
HC_bundles_all = pd.concat(HC_bundles)
HC_bundles_long = pd.concat(HC_bundles_long)

# save the result to a new csv file
HC_bundles_all.to_csv('/Volumes/pjakuszyk/seropositive_project/HC_tracts_mean_NDI.csv', index=False)

#Plot the avergae bundle load
sns.barplot(data=HC_bundles_long, x='index', y=0)
# Add labels and title to the plot
plt.xticks(rotation=90)
plt.xlabel('Bundle')
plt.ylabel('Average NDI per bundle')
plt.title('Healthy controls')
# Show the plot
plt.show()

#### create a figure with two subplots #####
fig, ax = plt.subplots()

# plot the first subplot
sns.barplot(data=HC_bundles_long, x='index', y=0, color="teal", ax=ax, ci=None)

# plot the second subplot
sns.barplot(data=SM_bundles_long, x='index', y=0, color="steelblue", ax=ax, ci=None)


# rotate the x-axis ticks by 90 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

# set scale for y
ax.set(ylim=(0.4, 0.8))

# set the title and axis labels
ax.set_title("NDI in MS and HC")
ax.set_ylabel("Mean NDI per tract")

# create a legend with color-coded labels
ax.legend(labels=['HC','MS'], labelcolor=['teal','steelblue' ], title="Disease", loc="upper right", handlelength=0)

# show the plot
plt.show()


########### create a figure with three subplots ##########
fig, ax = plt.subplots()

# plot the first subplot
sns.barplot(data=HC_bundles_long, x='index', y=0, color="teal", ax=ax, ci=None)

# plot the second subplot
sns.barplot(data=NMO_bundles_long, x='index', y=0, color="lightpink", ax=ax, ci=None)

#third subplot
sns.barplot(data=SM_bundles_long, x='index', y=0, color="steelblue", ax=ax, ci=None)


# rotate the x-axis ticks by 90 degrees
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

# set scale for y
ax.set(ylim=(0.4, 0.8))

# set the title and axis labels
ax.set_title("NDI in MS, NMOSD and HC")
ax.set_ylabel("Mean NDI per tract")

# create a legend with color-coded labels
ax.legend(labels=['HC','NMOSD','MS'], labelcolor=['teal','lightpink','steelblue' ], title="Disease", loc="upper right", handlelength=0)

# show the plot
plt.show()

################################################################################

####Do a t-test and visualize the data####

# Combine the two dataframes and add a 'Disease' column to identify the two groups
data_df = pd.concat([SM_bundles_all, NMO_bundles_all], ignore_index=True)
data_df['Disease'] = ['MS']*len(SM_bundles_all) + ['NMOSD']*len(NMO_bundles_all)


#MS vs HC

# Perform a t-test for each tract
p_vals = []
t_stats = []
for bundle in SM_bundles_all.columns:
    t_stat, p_val = ttest_ind(SM_bundles_all.loc[:, bundle], HC_bundles_all.loc[:, bundle], equal_var=False)
    t_stats.append(t_stat)
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


# Correct for multiple comparisons using the FDR procedure and save results to PDF
p_vals_corr = smm.multipletests(p_vals, alpha=0.05, method='fdr_bh')[1]

results_df = pd.DataFrame({
    'Bundle': SM_bundles_all.columns,
    'T-value': t_stats,
    'P-value': p_vals,
    'Corrected P-value': p_vals_corr
})


# Add asterisks to significant results
results_df['Significance'] = ''
results_df.loc[results_df['Corrected P-value'] < 0.001, 'Significance'] = '***'
results_df.loc[(results_df['Corrected P-value'] >= 0.001) & (results_df['Corrected P-value'] < 0.01), 'Significance'] = '**'
results_df.loc[(results_df['Corrected P-value'] >= 0.01) & (results_df['Corrected P-value'] < 0.05), 'Significance'] = '*'


results_df.to_csv('/Volumes/pjakuszyk/seropositive_project/MS_HC_t_test_results.csv', index=False)

#MS vs NMOSD

# Perform a t-test for each tract
p_vals = []
t_stats = []
for bundle in SM_bundles_all.columns:
    t_stat, p_val = ttest_ind(SM_bundles_all.loc[:, bundle], NMO_bundles_all.loc[:, bundle], equal_var=False)
    t_stats.append(t_stat)
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


# Correct for multiple comparisons using the FDR procedure and save results to PDF
p_vals_corr = smm.multipletests(p_vals, alpha=0.05, method='fdr_bh')[1]

results_df = pd.DataFrame({
    'Bundle': SM_bundles_all.columns,
    'T-value': t_stats,
    'P-value': p_vals,
    'Corrected P-value': p_vals_corr
})


# Add asterisks to significant results
results_df['Significance'] = ''
results_df.loc[results_df['Corrected P-value'] < 0.001, 'Significance'] = '***'
results_df.loc[(results_df['Corrected P-value'] >= 0.001) & (results_df['Corrected P-value'] < 0.01), 'Significance'] = '**'
results_df.loc[(results_df['Corrected P-value'] >= 0.01) & (results_df['Corrected P-value'] < 0.05), 'Significance'] = '*'


results_df.to_csv('/Volumes/pjakuszyk/seropositive_project/MS_NMOSD_t_test_results.csv', index=False)

#HC vs NMOSD

# Perform a t-test for each tract
p_vals = []
t_stats = []
for bundle in HC_bundles_all.columns:
    t_stat, p_val = ttest_ind(HC_bundles_all.loc[:, bundle], NMO_bundles_all.loc[:, bundle], equal_var=False)
    t_stats.append(t_stat)
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


# Correct for multiple comparisons using the FDR procedure and save results to PDF
p_vals_corr = smm.multipletests(p_vals, alpha=0.05, method='fdr_bh')[1]

results_df = pd.DataFrame({
    'Bundle': HC_bundles_all.columns,
    'T-value': t_stats,
    'P-value': p_vals,
    'Corrected P-value': p_vals_corr
})


# Add asterisks to significant results
results_df['Significance'] = ''
results_df.loc[results_df['Corrected P-value'] < 0.001, 'Significance'] = '***'
results_df.loc[(results_df['Corrected P-value'] >= 0.001) & (results_df['Corrected P-value'] < 0.01), 'Significance'] = '**'
results_df.loc[(results_df['Corrected P-value'] >= 0.01) & (results_df['Corrected P-value'] < 0.05), 'Significance'] = '*'


results_df.to_csv('/Volumes/pjakuszyk/seropositive_project/HC_NMOSD_t_test_results.csv', index=False)

