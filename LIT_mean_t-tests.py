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
from scipy.stats import ttest_ind, shapiro, t
import statsmodels.stats.multitest as smm
from scipy.stats import mannwhitneyu
from math import sqrt
from scipy.stats import ttest_rel
from scipy.stats import wilcoxon

np.set_printoptions(precision=8, suppress=True, formatter={'float': '{: 0.8e}'.format})

path_to_write='/Volumes/pjakuszyk/seropositive_project/'
# Set the folder name
folder_name = 'figures/'

# Create the folder if it doesn't exist
if not os.path.exists(path_to_write+folder_name):
    os.makedirs(path_to_write+folder_name)



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

SM_bundles_lesion = []
SM_bundles_lesion_long = []
# loop through each participant
for SM_patient in SM_patients:
    # read participant's csv file into a dataframe
    df = pd.read_csv(f"/Volumes/pjakuszyk/seropositive_project/participants/{SM_patient}/Brain/DWI/tractseg_output/Tractometry_NAWM_NODDI_ND.csv", sep=';')
    df_l = pd.read_csv(f"/Volumes/pjakuszyk/seropositive_project/participants/{SM_patient}/Brain/DWI/tractseg_output/Tractometry_lesions_NODDI_ND.csv", sep=';')
    
    #####Lesioned WM######
    # Create a figure with 50 subplots
    fig, axes = plt.subplots(nrows=10, ncols=5, figsize=(60, 50))
    
    # Loop through each column of the data and plot it on a separate subplot
    for i, col in enumerate(df_l.columns):
        # Select the data for the current column
        column_data = df_l[col]
        
        # Calculate the row and column indices for the current subplot
        row_idx = i // 5
        col_idx = i % 5
        
        # Plot the data on the current subplot
        axes[row_idx, col_idx].plot(column_data)
        
        # Set the title for the current subplot
        axes[row_idx, col_idx].set_title(col)
    
    # Set the overall title for the figure
    fig.suptitle(f'MS {SM_patient} data for 50 lesioned Tracts')
    
    # Adjust the spacing between the subplots
    fig.subplots_adjust(wspace=0.25, hspace=1.2)
    
    fig.savefig(os.path.join(path_to_write+folder_name, f"MS_lesioned_tracts_{SM_patient}.png"))
    
    # Close the figure window without displaying the figure
    plt.close()
    ####################

    # make a mean out of the 100 points sampled per tract 
    df = df.mean().to_frame().reset_index()
    df_l = df_l.mean().to_frame().reset_index()
 
    # add participant id column to the dataframe
    df['Participant'] = SM_patient
    df_l['Participant'] = SM_patient

    # bring it from long to wide format
    df_pivot = df.pivot(index='Participant', columns='index', values=0)
    df_pivot_lesion = df_l.pivot(index='Participant', columns='index', values=0)

    # append participant's data to the list
    SM_bundles.append(df_pivot)
    SM_bundles_long.append(df)
    
    SM_bundles_lesion.append(df_pivot_lesion)
    SM_bundles_lesion_long.append(df_l)

# concatenate all participant's data into a single dataframe
SM_bundles_all = pd.concat(SM_bundles)
SM_bundles_long = pd.concat(SM_bundles_long)

SM_bundles_lesion_all = pd.concat(SM_bundles_lesion)
SM_bundles_lesion_long = pd.concat(SM_bundles_lesion_long)

# save the result to a new csv file
SM_bundles_all.to_csv('/Volumes/pjakuszyk/seropositive_project/SM_tracts_mean_NDI_nosubst.csv', index=False)
SM_bundles_lesion_all.to_csv('/Volumes/pjakuszyk/seropositive_project/SM_tracts_NDI_lesions.csv', index=False)

'''
#Plot the avergae bundle load
sns.barplot(data=SM_bundles_long, x='index', y=0)
# Add labels and title to the plot
plt.xticks(rotation=90)
plt.xlabel('Bundle')
plt.ylabel('Average NDI per bundle')
plt.title('MS patients')
# Show the plot
plt.show()
'''  

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

NMO_bundles_lesion = []
NMO_bundles_lesion_long = []
# loop through each participant
for NMO_patient in NMO_patients:
    # read participant's csv file into a dataframe
    df = pd.read_csv(f"/Volumes/pjakuszyk/seropositive_project/participants/{NMO_patient}/Brain/DWI/tractseg_output/Tractometry_NAWM_NODDI_ND.csv", sep=';')
    df_l = pd.read_csv(f"/Volumes/pjakuszyk/seropositive_project/participants/{NMO_patient}/Brain/DWI/tractseg_output/Tractometry_lesions_NODDI_ND.csv", sep=';')

    #####Lesioned WM######
    # Create a figure with 50 subplots
    fig, axes = plt.subplots(nrows=10, ncols=5, figsize=(60, 50))
    
    # Loop through each column of the data and plot it on a separate subplot
    for i, col in enumerate(df_l.columns):
        # Select the data for the current column
        column_data = df_l[col]
        
        # Calculate the row and column indices for the current subplot
        row_idx = i // 5
        col_idx = i % 5
        
        # Plot the data on the current subplot
        axes[row_idx, col_idx].plot(column_data)
        
        # Set the title for the current subplot
        axes[row_idx, col_idx].set_title(col)
    
    # Set the overall title for the figure
    fig.suptitle(f'NMOSD {NMO_patient} data for 50 lesioned Tracts')
    
    # Adjust the spacing between the subplots
    fig.subplots_adjust(wspace=0.25, hspace=1.2)
    
    fig.savefig(os.path.join(path_to_write+folder_name, f"NMOSD_lesioned_tracts_{NMO_patient}.png"))
    
    # Close the figure window without displaying the figure
    plt.close()
    ####################        

    # make a mean out of the 100 points sampled per tract 
    df = df.mean().to_frame().reset_index()
    df_l = df_l.mean().to_frame().reset_index()
 
    # add participant id column to the dataframe
    df['Participant'] = NMO_patient
    df_l['Participant'] = NMO_patient

    # bring it from long to wide format
    df_pivot = df.pivot(index='Participant', columns='index', values=0)
    df_pivot_lesion = df_l.pivot(index='Participant', columns='index', values=0)

    # append participant's data to the list
    NMO_bundles.append(df_pivot)
    NMO_bundles_long.append(df)
    
    NMO_bundles_lesion.append(df_pivot_lesion)
    NMO_bundles_lesion_long.append(df_l)

# concatenate all participant's data into a single dataframe
NMO_bundles_all = pd.concat(NMO_bundles)
NMO_bundles_long = pd.concat(NMO_bundles_long)

NMO_bundles_lesion_all = pd.concat(NMO_bundles_lesion)
NMO_bundles_lesion_long = pd.concat(NMO_bundles_lesion_long)

# save the result to a new csv file
NMO_bundles_all.to_csv('/Volumes/pjakuszyk/seropositive_project/NMO_tracts_mean_NDI_nosubs.csv', index=False)
NMO_bundles_lesion_all.to_csv('/Volumes/pjakuszyk/seropositive_project/NMO_tracts_NDI_lesions.csv', index=False)

'''
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
'''
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
    df = pd.read_csv(f"/Volumes/pjakuszyk/seropositive_project/participants/{subject}/Brain/DWI/tractseg_output/Tractometry_NAWM_NODDI_ND.csv", sep=';')
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

'''
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
'''

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
ax.set(ylim=(0.35, 0.8))

# set the title and axis labels
ax.set_title("Lesion-independent tracts NDI in MS, NMOSD and HC")
ax.set_ylabel("Mean NDI per tract")

# create a legend with color-coded labels
ax.legend(labels=['HC','NMOSD','MS'], labelcolor=['teal','lightpink','steelblue' ], title="Disease", loc="upper right", handlelength=0)

# show the plot
plt.show()

################################################################################

#Independent samples tests

# Change all the zeros produced by insufficient streamlines to NaN values
SM_bundles_all = SM_bundles_all.replace(0, np.nan)
HC_bundles_all = HC_bundles_all.replace(0, np.nan)
NMO_bundles_all = NMO_bundles_all.replace(0, np.nan)


# Calculate n for every group and tract
n_sample_sm = []
n_sample_nmo = []
n_sample_hc = []


for bundle in SM_bundles_all.columns:
    
    n_sm = SM_bundles_all.loc[:, bundle].notna().sum()
    n_sample_sm.append(n_sm)
    
for bundle in NMO_bundles_all.columns:
    
    n_nmo = NMO_bundles_all.loc[:, bundle].notna().sum()
    n_sample_nmo.append(n_nmo)

for bundle in HC_bundles_all.columns:
    
    n_hc= HC_bundles_all.loc[:, bundle].notna().sum()
    n_sample_hc.append(n_hc)

#Combine it all together

# Check normality using Shapiro-Wilk test
sw_test_results = []
for bundle in SM_bundles_all.columns:
    sm_w, sm_p = shapiro(SM_bundles_all.loc[:, bundle])
    nmo_w, nmo_p = shapiro(NMO_bundles_all.loc[:, bundle])
    hc_w, hc_p = shapiro(HC_bundles_all.loc[:, bundle])
    sw_test_results.append({
        'Bundle': bundle,
        'SM W': sm_w,
        'SM p-value': sm_p,
        'NMO W': nmo_w,
        'NMO p-value': nmo_p,
        'HC W' : hc_w,
        'HC p-value' : hc_p
    })

sw_test_df = pd.DataFrame(sw_test_results)
sw_test_df.to_csv('/Volumes/pjakuszyk/seropositive_project/shapiro_wilk_test_results.csv', index=False)

#MS vs HC

# Perform a t-test for each tract
p_vals = []
t_stats = []
cohens_ds = []
mean_diffs = []
ci_lower = []
ci_upper = []
ratios= []


for bundle in SM_bundles_all.columns:
    
    t_stat, p_val = ttest_ind(SM_bundles_all.loc[:, bundle], HC_bundles_all.loc[:, bundle], equal_var=False, nan_policy='omit')
    t_stats.append(t_stat)
    p_vals.append(p_val)
   
    # Calculate the confidence interval for the mean difference and cohen's d effect size
    n_sm = SM_bundles_all.loc[:, bundle].notna().sum()
    n_hc= HC_bundles_all.loc[:, bundle].notna().sum() 
    
    mean_diff = SM_bundles_all.loc[:, bundle].mean() - HC_bundles_all.loc[:, bundle].mean()
    
    mean_diffs.append(mean_diff)
    
    t_crit = t.interval(0.95, df=(n_sm+n_hc-2))[1]
    
    pooled_sd = np.sqrt(((n_sm-1)*SM_bundles_all.loc[:, bundle].std()**2 + (n_hc-1)*HC_bundles_all.loc[:, bundle].std()**2) / (n_sm + n_hc - 2))
    
    mean_diff_se = pooled_sd * np.sqrt(1/n_sm + 1/n_hc)
      
    mean_diff_CI_lower = mean_diff - t_crit * mean_diff_se
    mean_diff_CI_upper = mean_diff + t_crit * mean_diff_se
    
    ci_lower.append(mean_diff_CI_lower)
    ci_upper.append(mean_diff_CI_upper)
    
    cohens_d = (SM_bundles_all.loc[:, bundle].mean() - HC_bundles_all.loc[:, bundle].mean()) / pooled_sd
    cohens_ds.append(cohens_d)
    
    #An informal check for this is to compare the ratio of the two sample standard deviations. If the two are equal, the ratio would be 1 but a good Rule of Thumb to use is to see if the ratio falls from 0.5 to 2.
    ratio = SM_bundles_all.loc[:, bundle].std()/HC_bundles_all.loc[:, bundle].std()
    
    ratios.append(ratio)

#MS vs NMOSD

# Perform a t-test for each tract
for bundle in SM_bundles_all.columns:
    t_stat, p_val = ttest_ind(SM_bundles_all.loc[:, bundle], NMO_bundles_all.loc[:, bundle], equal_var=False,nan_policy='omit')
    t_stats.append(t_stat)
    p_vals.append(p_val)

    # Calculate the confidence interval for the mean difference and cohen's d effect size
    n_sm = SM_bundles_all.loc[:, bundle].notna().sum()
    n_nmo= NMO_bundles_all.loc[:, bundle].notna().sum() 
    
    mean_diff = SM_bundles_all.loc[:, bundle].mean() - NMO_bundles_all.loc[:, bundle].mean()
    
    mean_diffs.append(mean_diff)
    
    t_crit = t.interval(0.95, df=(n_sm+n_nmo-2))[1]
    
    pooled_sd = np.sqrt(((n_sm-1)*SM_bundles_all.loc[:, bundle].std()**2 + (n_nmo-1)*NMO_bundles_all.loc[:, bundle].std()**2) / (n_sm + n_nmo - 2))
    
    mean_diff_se = pooled_sd * np.sqrt(1/n_sm + 1/n_nmo)
      
    mean_diff_CI_lower = mean_diff - t_crit * mean_diff_se
    mean_diff_CI_upper = mean_diff + t_crit * mean_diff_se
    
    ci_lower.append(mean_diff_CI_lower)
    ci_upper.append(mean_diff_CI_upper)
    
    cohens_d = (SM_bundles_all.loc[:, bundle].mean() - NMO_bundles_all.loc[:, bundle].mean()) / pooled_sd
    cohens_ds.append(cohens_d)
    
    #An informal check for this is to compare the ratio of the two sample standard deviations. If the two are equal, the ratio would be 1 but a good Rule of Thumb to use is to see if the ratio falls from 0.5 to 2.
    ratio = SM_bundles_all.loc[:, bundle].std()/NMO_bundles_all.loc[:, bundle].std()
    
    ratios.append(ratio)


#HC vs NMOSD

# Perform a t-test for each tract
for bundle in HC_bundles_all.columns:
    t_stat, p_val = ttest_ind(HC_bundles_all.loc[:, bundle], NMO_bundles_all.loc[:, bundle], equal_var=False,nan_policy='omit')
    t_stats.append(t_stat)
    p_vals.append(p_val)
    
    # Calculate the confidence interval for the mean difference and cohen's d effect size
    n_hc = HC_bundles_all.loc[:, bundle].notna().sum()
    n_nmo= NMO_bundles_all.loc[:, bundle].notna().sum() 
    
    mean_diff = HC_bundles_all.loc[:, bundle].mean() - NMO_bundles_all.loc[:, bundle].mean()
    
    mean_diffs.append(mean_diff)
    
    t_crit = t.interval(0.95, df=(n_hc+n_nmo-2))[1]
    
    pooled_sd = np.sqrt(((n_hc-1)*HC_bundles_all.loc[:, bundle].std()**2 + (n_nmo-1)*NMO_bundles_all.loc[:, bundle].std()**2) / (n_hc + n_nmo - 2))
    
    mean_diff_se = pooled_sd * np.sqrt(1/n_hc + 1/n_nmo)
      
    mean_diff_CI_lower = mean_diff - t_crit * mean_diff_se
    mean_diff_CI_upper = mean_diff + t_crit * mean_diff_se
    
    ci_lower.append(mean_diff_CI_lower)
    ci_upper.append(mean_diff_CI_upper)
    
    cohens_d = (HC_bundles_all.loc[:, bundle].mean() - NMO_bundles_all.loc[:, bundle].mean()) / pooled_sd
    cohens_ds.append(cohens_d)
    
    #An informal check for this is to compare the ratio of the two sample standard deviations. If the two are equal, the ratio would be 1 but a good Rule of Thumb to use is to see if the ratio falls from 0.5 to 2.
    ratio = HC_bundles_all.loc[:, bundle].std()/NMO_bundles_all.loc[:, bundle].std()
    
    ratios.append(ratio)


# Correct for multiple comparisons using the FDR procedure and save results to PDF
p_vals_corr = smm.multipletests(p_vals, alpha=0.05, method='fdr_bh')[1]

# Create a list of values to assign to the "disease" column
disease_values = ['MS vs HC']*50 + ['MS vs NMOSD']*50 + ['HC vs NMOSD']*50
bundles_index = HC_bundles_all.columns
bundles_concatenated_index = pd.concat([HC_bundles_all.columns.to_frame()]*3)
bundles_concatenated_index = bundles_concatenated_index.reset_index(drop=True).squeeze()

# Insert n value for every group and tract in the right place
number_sm = n_sample_sm+n_sample_sm+['']*50
number_nmo = ['']*50 + n_sample_nmo + n_sample_nmo
number_hc = n_sample_hc+['']*50+n_sample_hc


results_df = pd.DataFrame({
    'Comparison': disease_values,
    'Bundle': bundles_concatenated_index,
    'n SM':number_sm,
    'n NMO':number_nmo,
    'n HC':number_hc,
    'Ratio': ratios,
    'T-value': t_stats,
    'Cohen\'s d': cohens_ds,
    'Lower CI 95': ci_lower,
    'Mean diff': mean_diffs,
    'Upper CI 95': ci_upper,
    'P-value': p_vals,
    'Corrected P-value': p_vals_corr
})


# Add asterisks to significant results
results_df['Significance'] = ''
results_df.loc[results_df['Corrected P-value'] < 0.001, 'Significance'] = '***'
results_df.loc[(results_df['Corrected P-value'] >= 0.001) & (results_df['Corrected P-value'] < 0.01), 'Significance'] = '**'
results_df.loc[(results_df['Corrected P-value'] >= 0.01) & (results_df['Corrected P-value'] < 0.05), 'Significance'] = '*'


results_df.to_csv('/Volumes/pjakuszyk/seropositive_project/All_groups_all_tracts_t_test_results_nosubs.csv', index=False)

#########Lesioned streamlines vs NAWM streamlines

##########SM############

#Make all the 0 values in tracts that were not lesioned into np.nan
SM_bundles_all = SM_bundles_all.replace(0, np.nan)
SM_bundles_lesion_all = SM_bundles_lesion_all.replace(0, np.nan)


# Check normality using Shapiro-Wilk test
sw_test_results = []
for bundle in SM_bundles_lesion_all.columns:
    # Drop NaN values from the data
    data = SM_bundles_lesion_all.loc[:, bundle].dropna()
    # Run the Shapiro-Wilk test on the cleaned data
    sm_w, sm_p = shapiro(data)
    sw_test_results.append({
        'Bundle': bundle,
        'SM W': sm_w,
        'SM p-value': sm_p,
    })


sw_test_df = pd.DataFrame(sw_test_results)
sw_test_df.to_csv('/Volumes/pjakuszyk/seropositive_project/shapiro_wilk_test_results_lesions.csv', index=False)

#Distribution is not normal
# Perform a mann whitney for each tract
p_vals = []
t_stats = []
cohens_ds = []
mean_diffs = []
ci_lower = []
ci_upper = []
ratios = []
n_sample = []

for bundle in SM_bundles_lesion_all.columns:
    _, p_val = wilcoxon(SM_bundles_lesion_all.loc[:, bundle], SM_bundles_all.loc[:, bundle],nan_policy='omit', zero_method='wilcox')
    t_stats.append(None) # Wilcoxon test doesn't have a test statistic
    p_vals.append(p_val)
    
    # Calculate the confidence interval for the mean difference and cohen's d effect size
    
    # For proper df calculation define the number of non nan entries in the bundle with lesions
    
    n = (SM_bundles_lesion_all.loc[:, bundle] - SM_bundles_all.loc[:, bundle]).notna().sum()
    
    n_sample.append(n)
    
    diff = SM_bundles_lesion_all.loc[:, bundle] - SM_bundles_all.loc[:, bundle]
        
    mean_diff=diff.mean()
    
    sd_diff=diff.std()
    
    mean_diffs.append(mean_diff)
    
    t_crit = t.interval(0.95, df=(n-1))[1]
        
    mean_diff_se = sd_diff / np.sqrt(n)
      
    mean_diff_CI_lower = mean_diff - t_crit * mean_diff_se
    mean_diff_CI_upper = mean_diff + t_crit * mean_diff_se
    
    ci_lower.append(mean_diff_CI_lower)
    ci_upper.append(mean_diff_CI_upper)
    
    cohens_d = mean_diff / sd_diff
    cohens_ds.append(cohens_d)
    
    #An informal check for this is to compare the ratio of the two sample standard deviations. If the two are equal, the ratio would be 1 but a good Rule of Thumb to use is to see if the ratio falls from 0.5 to 2.
    ratio = SM_bundles_lesion_all.loc[:, bundle].std()/SM_bundles_all.loc[:, bundle].std()
    
    ratios.append(ratio)


# Correct for multiple comparisons using the FDR procedure and save results to PDF
p_vals_corr = smm.multipletests(p_vals, alpha=0.05, method='fdr_bh')[1]

# Create a list of values to assign to the "disease" column
disease_values = ['lesions vs NAWM']*50
bundles_index = SM_bundles_lesion_all.columns

results_df_lesions = pd.DataFrame({
    'Comparison': disease_values,
    'n': n_sample,
    'Bundle': bundles_index,
    'Ratio': ratios,
    'T-value': t_stats,
    'Cohen\'s d': cohens_ds,
    'Lower CI 95': ci_lower,
    'Mean diff': mean_diffs,
    'Upper CI 95': ci_upper,
    'P-value': p_vals,
    'Corrected P-value': p_vals_corr
})


# Add asterisks to significant results
results_df_lesions['Significance'] = ''
results_df_lesions.loc[results_df_lesions['Corrected P-value'] < 0.001, 'Significance'] = '***'
results_df_lesions.loc[(results_df_lesions['Corrected P-value'] >= 0.001) & (results_df_lesions['Corrected P-value'] < 0.01), 'Significance'] = '**'
results_df_lesions.loc[(results_df_lesions['Corrected P-value'] >= 0.01) & (results_df_lesions['Corrected P-value'] < 0.05), 'Significance'] = '*'


results_df_lesions.to_csv('/Volumes/pjakuszyk/seropositive_project/MS_NAWM_vs_lesions_t_test_results.csv', index=False)

##########NMO############

#Make all the 0 values in tracts that were not lesioned into np.nan
NMO_bundles_all = NMO_bundles_all.replace(0, np.nan)
NMO_bundles_lesion_all = NMO_bundles_lesion_all.replace(0, np.nan)

#For testing normality
NMO_norm_df=NMO_bundles_lesion_all.dropna()

# Check normality using Shapiro-Wilk test
sw_test_results = []
for bundle in NMO_bundles_lesion_all.columns:
    # Drop NaN values from the data
    data = SM_bundles_lesion_all.loc[:, bundle].dropna()
    # Run the Shapiro-Wilk test on the cleaned data
    sm_w, sm_p = shapiro(data)
    sw_test_results.append({
        'Bundle': bundle,
        'SM W': sm_w,
        'SM p-value': sm_p,
    })

sw_test_df = pd.DataFrame(sw_test_results)
sw_test_df.to_csv('/Volumes/pjakuszyk/seropositive_project/shapiro_wilk_test_results_lesions_nmosd.csv', index=False)

#Distribution is not normal
# Perform a mann whitney for each tract
p_vals = []
t_stats = []
cohens_ds = []
mean_diffs = []
ci_lower = []
ci_upper = []
ratios= []
bundles =[]
n_sample = []

for bundle in NMO_bundles_lesion_all.columns:
    if NMO_bundles_lesion_all.loc[:, bundle].isnull().all() or NMO_bundles_all.loc[:, bundle].isnull().all():
        # skip empty columns
        continue
    else:
        _, p_val = wilcoxon(NMO_bundles_lesion_all.loc[:, bundle], NMO_bundles_all.loc[:, bundle],nan_policy='omit', zero_method='wilcox')
        t_stats.append(None) # Wilcoxon test doesn't have a test statistic
        p_vals.append(p_val)
        
        # For proper df calculation define the number of non nan entries in the bundle with lesions
       
        n = (NMO_bundles_lesion_all.loc[:, bundle] - NMO_bundles_all.loc[:, bundle]).notna().sum()
       
        n_sample.append(n)
       
        diff = NMO_bundles_lesion_all.loc[:, bundle] - NMO_bundles_all.loc[:, bundle]
       
        mean_diff=diff.mean()
       
        sd_diff=diff.std()
       
        mean_diffs.append(mean_diff)
       
        t_crit = t.interval(0.95, df=(n-1))[1]
           
        mean_diff_se = sd_diff / np.sqrt(n)
          
        mean_diff_CI_lower = mean_diff - t_crit * mean_diff_se
        mean_diff_CI_upper = mean_diff + t_crit * mean_diff_se
        
        ci_lower.append(mean_diff_CI_lower)
        ci_upper.append(mean_diff_CI_upper)
        
        cohens_d = mean_diff / sd_diff
        cohens_ds.append(cohens_d)
        
        #An informal check for this is to compare the ratio of the two sample standard deviations. If the two are equal, the ratio would be 1 but a good Rule of Thumb to use is to see if the ratio falls from 0.5 to 2.
        ratio = NMO_bundles_lesion_all.loc[:, bundle].std()/NMO_bundles_all.loc[:, bundle].std()
        
        ratios.append(ratio)
        
        bundles.append(bundle)


# Correct for multiple comparisons using the FDR procedure and save results to PDF
p_vals_corr = smm.multipletests(p_vals, alpha=0.05, method='fdr_bh')[1]

# Create a list of values to assign to the "disease" column
disease_values = ['lesions vs NAWM']*len(bundles)

results_df_lesions = pd.DataFrame({
    'Comparison': disease_values,
    'n':n_sample,
    'Bundle': bundles,
    'Ratio': ratios,
    'T-value': t_stats,
    'Cohen\'s d': cohens_ds,
    'Lower CI 95': ci_lower,
    'Mean diff': mean_diffs,
    'Upper CI 95': ci_upper,
    'P-value': p_vals,
    'Corrected P-value': p_vals_corr
})


# Add asterisks to significant results
results_df_lesions['Significance'] = ''
results_df_lesions.loc[results_df_lesions['Corrected P-value'] < 0.001, 'Significance'] = '***'
results_df_lesions.loc[(results_df_lesions['Corrected P-value'] >= 0.001) & (results_df_lesions['Corrected P-value'] < 0.01), 'Significance'] = '**'
results_df_lesions.loc[(results_df_lesions['Corrected P-value'] >= 0.01) & (results_df_lesions['Corrected P-value'] < 0.05), 'Significance'] = '*'


results_df_lesions.to_csv('/Volumes/pjakuszyk/seropositive_project/NMOSD_NAWM_vs_lesions_t_test_results.csv', index=False)


