#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 10:35:09 2023

@author: pawel
"""

# Retrieve destrieux parcellation in fsaverage5 space from nilearn
from nilearn import datasets
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
import surfplot as surfplot
from surfplot import Plot
import statsmodels.stats.multitest as smm

path_to_write='/Volumes/ms/seropositive_project/figures/'

##Prepare data

# Set float_format to display up to 3 decimal places
pd.options.display.float_format = '{:.3f}'.format

#read in the data
df = pd.read_csv("/Volumes/ms/PJ_gRatio/Stata/data_ready.csv", sep=',')

# Subset the DataFrame based on a column value
subset_HC_rh = df.loc[df['diagnosis'] == 'HC', 'rh_unknown':'rh_s_temporal_transverse']
subset_HC_rh['diagnosis'] = 'HC'

subset_HC_lh = df.loc[df['diagnosis'] == 'HC', 'lh_unknown':'lh_s_temporal_transverse']
subset_HC_lh['diagnosis'] = 'HC'

subset_MS_rh = df.loc[df['diagnosis'] == 'RRMS', 'rh_unknown':'rh_s_temporal_transverse']
subset_MS_rh['diagnosis'] = 'RRMS'

subset_MS_lh = df.loc[df['diagnosis'] == 'RRMS', 'lh_unknown':'lh_s_temporal_transverse']
subset_MS_lh['diagnosis'] = 'RRMS'

subset_NMO_rh = df.loc[df['diagnosis'] == 'NMOSD', 'rh_unknown':'rh_s_temporal_transverse']
subset_NMO_rh['diagnosis'] = 'NMOSD'

subset_NMO_lh = df.loc[df['diagnosis'] == 'NMOSD', 'lh_unknown':'lh_s_temporal_transverse']
subset_NMO_lh['diagnosis'] = 'NMOSD'

df_cortex_rh = pd.concat([subset_HC_rh, subset_MS_rh, subset_NMO_rh], ignore_index=True)
df_cortex_lh = pd.concat([subset_HC_lh, subset_MS_lh, subset_NMO_lh], ignore_index=True)

first_column = df_cortex_rh.pop('diagnosis')
df_cortex_rh.insert(0, 'diagnosis', first_column)

first_column = df_cortex_lh.pop('diagnosis')
df_cortex_lh.insert(0, 'diagnosis', first_column)


df_MS_HC_rh= df_cortex_rh[df_cortex_rh['diagnosis'].isin(['HC', 'RRMS'])]
df_MS_HC_lh= df_cortex_lh[df_cortex_lh['diagnosis'].isin(['HC', 'RRMS'])]

df_NMOSD_HC_rh= df_cortex_rh[df_cortex_rh['diagnosis'].isin(['HC', 'NMOSD'])]
df_NMOSD_HC_lh= df_cortex_lh[df_cortex_lh['diagnosis'].isin(['HC', 'NMOSD'])]

df_NMOSD_MS_rh= df_cortex_rh[df_cortex_rh['diagnosis'].isin(['RRMS', 'NMOSD'])]
df_NMOSD_MS_lh= df_cortex_lh[df_cortex_lh['diagnosis'].isin(['RRMS', 'NMOSD'])]

##Prepare parcellations

destrieux_atlas = datasets.fetch_atlas_surf_destrieux()

# The parcellation is already loaded into memory
parcellation_right = destrieux_atlas['map_right']
parcellation_left = destrieux_atlas['map_left']

# Retrieve fsaverage5 surface dataset for the plotting background. It contains
# the surface template as pial and inflated version and a sulcal depth maps
# which is used for shading
fsaverage = datasets.fetch_surf_fsaverage()

# The fsaverage dataset contains file names pointing to the file locations
print("Fsaverage5 pial surface of left hemisphere is at: "
      f"{fsaverage['pial_left']}")
print("Fsaverage5 inflated surface of left hemisphere is at: "
      f"{fsaverage['infl_left']}")
print("Fsaverage5 sulcal depth map of left hemisphere is at: "
      f"{fsaverage['sulc_left']}")


#Calculate and plot t-statistics

#HC vs MS
p_vals = []
t_stats = []
#RH
for parcelletion in df_cortex_rh.columns[1:]:
    t_stat, p_val = ttest_ind(df_MS_HC_rh.loc[df_MS_HC_rh['diagnosis'] == 'HC', parcelletion], df_MS_HC_rh.loc[df_MS_HC_rh['diagnosis'] == 'RRMS', parcelletion], equal_var=False, nan_policy='omit')
    t_stats.append(t_stat)
    p_vals.append(p_val)

rh_t_vals = np.array(t_stats)

# Replace the label values with t-stats
HC_MS_parcellation_rh = np.zeros_like(parcellation_right, dtype=float)
unique_labels = np.unique(parcellation_right)
for i, label in enumerate(unique_labels):
    mask = parcellation_right == label
    HC_MS_parcellation_rh[mask] = rh_t_vals[i]

#LH
t_stats = []

for parcelletion in df_cortex_lh.columns[1:]:
    t_stat, p_val = ttest_ind(df_MS_HC_lh.loc[df_MS_HC_lh['diagnosis'] == 'HC', parcelletion], df_MS_HC_lh.loc[df_MS_HC_lh['diagnosis'] == 'RRMS', parcelletion], equal_var=False, nan_policy='omit')
    t_stats.append(t_stat)
    p_vals.append(p_val)

lh_t_vals = np.array(t_stats)


# Replace the label values with random numbers
HC_MS_parcellation_lh = np.zeros_like(parcellation_left, dtype=float)
unique_labels = np.unique(parcellation_left)
for i, label in enumerate(unique_labels):
    mask = parcellation_left == label
    HC_MS_parcellation_lh[mask] = lh_t_vals[i]


#HC vs NMOSD
#RH
t_stats = []
for parcelletion in df_cortex_rh.columns[1:]:
    t_stat, p_val = ttest_ind(df_NMOSD_HC_rh.loc[df_NMOSD_HC_rh['diagnosis'] == 'HC', parcelletion], df_NMOSD_HC_rh.loc[df_NMOSD_HC_rh['diagnosis'] == 'NMOSD', parcelletion], equal_var=False, nan_policy='omit')
    t_stats.append(t_stat)
    p_vals.append(p_val)

rh_t_vals = np.array(t_stats)

# Replace the label values with t-stats
NMOSD_HC_parcellation_rh = np.zeros_like(parcellation_right, dtype=float)
unique_labels = np.unique(parcellation_right)
for i, label in enumerate(unique_labels):
    mask = parcellation_right == label
    NMOSD_HC_parcellation_rh[mask] = rh_t_vals[i]
    
#LH
t_stats = []
for parcelletion in df_cortex_lh.columns[1:]:
    t_stat, p_val = ttest_ind(df_NMOSD_HC_lh.loc[df_NMOSD_HC_lh['diagnosis'] == 'HC', parcelletion], df_NMOSD_HC_lh.loc[df_NMOSD_HC_lh['diagnosis'] == 'NMOSD', parcelletion], equal_var=False, nan_policy='omit')
    t_stats.append(t_stat)
    p_vals.append(p_val)

lh_t_vals = np.array(t_stats)

# Replace the label values with random numbers
NMOSD_HC_parcellation_lh = np.zeros_like(parcellation_left, dtype=float)
unique_labels = np.unique(parcellation_left)
for i, label in enumerate(unique_labels):
    mask = parcellation_left == label
    NMOSD_HC_parcellation_lh[mask] = lh_t_vals[i]
    

#MS vs NMOSD
#RH
t_stats = []
for parcelletion in df_cortex_rh.columns[1:]:
    t_stat, p_val = ttest_ind(df_NMOSD_MS_rh.loc[df_NMOSD_MS_rh['diagnosis'] == 'NMOSD', parcelletion], df_NMOSD_MS_rh.loc[df_NMOSD_MS_rh['diagnosis'] == 'RRMS', parcelletion], equal_var=False, nan_policy='omit')
    t_stats.append(t_stat)
    p_vals.append(p_val)
        
rh_t_vals = np.array(t_stats)

# Replace the label values with t-stats
NMOSD_MS_parcellation_rh = np.zeros_like(parcellation_right, dtype=float)
unique_labels = np.unique(parcellation_right)
for i, label in enumerate(unique_labels):
    mask = parcellation_right == label
    NMOSD_MS_parcellation_rh[mask] = rh_t_vals[i]
     
 #LH
t_stats = []
for parcelletion in df_cortex_lh.columns[1:]:
    t_stat, p_val = ttest_ind(df_NMOSD_MS_lh.loc[df_NMOSD_MS_lh['diagnosis'] == 'NMOSD', parcelletion], df_NMOSD_MS_lh.loc[df_NMOSD_MS_lh['diagnosis'] == 'RRMS', parcelletion], equal_var=False, nan_policy='omit')
    t_stats.append(t_stat)
    p_vals.append(p_val)

lh_t_vals = np.array(t_stats)

# Replace the label values with random numbers
NMOSD_MS_parcellation_lh = np.zeros_like(parcellation_left, dtype=float)
unique_labels = np.unique(parcellation_left)
for i, label in enumerate(unique_labels):
    mask = parcellation_left == label
    NMOSD_MS_parcellation_lh[mask] = lh_t_vals[i]
     
    
#Add information about significance
p_vals_corr = smm.multipletests(p_vals, alpha=0.05, method='fdr_bh')[1]

# Length of each subarray
subarray_length = 75

# Number of subarrays
num_subarrays = 6

# Slicing and storing subarrays
subarrays = []
for i in range(num_subarrays):
    #print(f"{i}")
    start_idx = i * subarray_length
    end_idx = start_idx + subarray_length
    subarray = p_vals_corr[start_idx:end_idx]
    subarrays.append(subarray)

# New names for the arrays
new_names = ['HC_MS_rh_p_corr', 'HC_MS_lh_p_corr', 'HC_NMOSD_rh_p_corr', 'HC_NMOSD_lh_p_corr','NMOSD_MS_rh_p_corr', 'NMOSD_MS_lh_p_corr']
        
p_corrected_renamed_arrays = {name: array for name, array in zip(new_names, subarrays)}

binarized_p_corrected_renamed_arrays = {}

for array in p_corrected_renamed_arrays:
    binarized_p_corrected_renamed_arrays[array] = surfplot.utils.threshold(p_corrected_renamed_arrays[array], 0.05, binarize=True, two_sided=True)


# Replace the label values with corrected p-vals
p_vals = {}

comparison_names = ['HC_MS', 'HC_NMOSD', 'NMOSD_MS']
hemisphere_names = ['rh', 'lh']

for comparison_name in comparison_names:
    p_vals[comparison_name] = {}

    for hemisphere_name in hemisphere_names:
        array_name = f"{comparison_name}_{hemisphere_name}_p_corr"
        parcellation = parcellation_right if hemisphere_name == 'rh' else parcellation_left
        p_val_array = np.zeros_like(parcellation, dtype=float)
        unique_labels = np.unique(parcellation)

        for i, label in enumerate(unique_labels):
            mask = parcellation == label
            p_val_array[mask] = binarized_p_corrected_renamed_arrays[array_name][i]

        p_vals[comparison_name][hemisphere_name] = p_val_array

#Generate plots
#HC MS
p = Plot(fsaverage['infl_left'],fsaverage['infl_right'], views=['lateral','medial'], zoom=1.5)
p.add_layer({'left': HC_MS_parcellation_lh, 'right': HC_MS_parcellation_rh}, cmap='YlOrRd', cbar_label='T-statistic')
p.add_layer({'left': p_vals['HC_MS']['lh'], 'right': p_vals['HC_MS']['rh']}, cmap='binary_r',alpha=0.9, cbar=False)
fig = p.build()
fig.axes[0].set_title('T-statistics in RRMS and HC ', pad=-3)
fig.savefig(path_to_write+'HC_MS_cortex_tstat_plot.png', dpi=500, bbox_inches='tight')

#HC NMOSD
p = Plot(fsaverage['infl_left'],fsaverage['infl_right'], views=['lateral','medial'], zoom=1.5)
p.add_layer({'left': NMOSD_HC_parcellation_lh, 'right': NMOSD_HC_parcellation_rh}, cmap='YlOrRd', cbar_label='T-statistic')
p.add_layer({'left': p_vals['HC_NMOSD']['lh'], 'right': p_vals['HC_NMOSD']['rh']}, cmap='binary_r',alpha=0.9, cbar=False)
fig = p.build()
fig.axes[0].set_title('T-statistics in NMOSD and HC ', pad=-3)
fig.savefig(path_to_write+'HC_NMOSD_cortex_tstat_plot.png', dpi=500, bbox_inches='tight')

#NMOSD MS
p = Plot(fsaverage['infl_left'],fsaverage['infl_right'], views=['lateral','medial'], zoom=1.5)
p.add_layer({'left': NMOSD_MS_parcellation_lh, 'right': NMOSD_MS_parcellation_rh}, cmap='YlOrRd', cbar_label='T-statistic')
p.add_layer({'left': p_vals['NMOSD_MS']['lh'], 'right': p_vals['NMOSD_MS']['rh']}, cmap='binary_r',alpha=0.9, cbar=False)
fig = p.build()
fig.axes[0].set_title('T-statistics in RRMS and NMOSD ', pad=-3)
fig.savefig(path_to_write+'NMOSD_MS_cortex_tstat_plot.png', dpi=500, bbox_inches='tight')








