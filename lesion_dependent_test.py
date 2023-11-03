#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 17:35:53 2023

@author: pawel
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import scipy.stats as stats
import ptitprince as pt
from scipy.stats import ttest_ind, t
import statsmodels.stats.multitest as smm


# Set float_format to display up to 3 decimal places
pd.options.display.float_format = '{:.3f}'.format

#read in the data
df = pd.read_csv("/Volumes/ms/PJ_gRatio/Stata/data_ready.csv", sep=',')

# Subset the DataFrame based on a column value
subset_HC = df.loc[df['diagnosis'] == 'HC', 'lit_af':'lit_slf']
subset_HC['diagnosis'] = 'HC'

subset_MS = df.loc[df['diagnosis'] == 'RRMS', 'ld_af':'ld_slf']
subset_MS['diagnosis'] = 'RRMS'

subset_NMO = df.loc[df['diagnosis'] == 'NMOSD', 'ld_af':'ld_slf']
subset_NMO['diagnosis'] = 'NMOSD'


#RAW
subset_HC_raw = df.loc[df['diagnosis'] == 'HC', 'af_raw':'slf_raw']
subset_HC_raw['diagnosis'] = 'HC'

subset_MS_raw = df.loc[df['diagnosis'] == 'RRMS', 'af_raw':'slf_raw']
subset_MS_raw['diagnosis'] = 'RRMS'

subset_NMO_raw = df.loc[df['diagnosis'] == 'NMOSD', 'af_raw':'slf_raw']
subset_NMO_raw['diagnosis'] = 'NMOSD'



full_names_lit = {
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

full_names_ld = {
    'ld_af': 'Arcuate fascicle',
    'ld_atr': 'Anterior Thalamic Radiation',
    'ld_cc': 'Corpus Callosum',
    'ld_cg': 'Cingulum',
    'ld_cst': 'Corticospinal tract',
    'ld_fpt': 'Fronto-pontine tract',
    'ld_icp': 'Inferior cerebellar peduncle',
    'ld_ifo': 'Inferior occipito-frontal fascicle',
    'ld_ilf': 'Inferior longitudinal fascicle',
    'ld_mcp': 'Middle cerebellar peduncle',
    'ld_or': 'Optic radiation',
    'ld_popt': 'Parieto‐occipital pontine',
    'ld_scp': 'Superior cerebellar peduncle',
    'ld_slf': 'Superior longitudinal fascicle',
    'ld_str': 'Superior Thalamic Radiation',
    'ld_uf': 'Uncinate fascicle',
    'ld_t_prem': 'Thalamo-premotor fibres',
    'ld_t_par': 'Thalamo-parietal fibres',
    'ld_t_occ': 'Thalamo-occipital fibres',
    'ld_st_fo': 'Striato-fronto-orbital fibres',
    'ld_st_prem': 'Striato-premotor fibres',
}

full_names_raw = {
    'af_raw': 'Arcuate fascicle',
    'atr_raw': 'Anterior Thalamic Radiation',
    'cc_raw': 'Corpus Callosum',
    'cg_raw': 'Cingulum',
    'cst_raw': 'Corticospinal tract',
    'fpt_raw': 'Fronto-pontine tract',
    'icp_raw': 'Inferior cerebellar peduncle',
    'ifo_raw': 'Inferior occipito-frontal fascicle',
    'ilf_raw': 'Inferior longitudinal fascicle',
    'mcp_raw': 'Middle cerebellar peduncle',
    'or_raw': 'Optic radiation',
    'popt_raw': 'Parieto‐occipital pontine',
    'scp_raw': 'Superior cerebellar peduncle',
    'slf_raw': 'Superior longitudinal fascicle',
    'str_raw': 'Superior Thalamic Radiation',
    'uf_raw': 'Uncinate fascicle',
    't_prem_raw': 'Thalamo-premotor fibres',
    't_par_raw': 'Thalamo-parietal fibres',
    't_occ_raw': 'Thalamo-occipital fibres',
    'st_fo_raw': 'Striato-fronto-orbital fibres',
    'st_prem_raw': 'Striato-premotor fibres',
}


# Rename the columns using the updated dictionaries
subset_HC = subset_HC.rename(columns=full_names_lit)
subset_MS = subset_MS.rename(columns=full_names_ld)
subset_NMO = subset_NMO.rename(columns=full_names_ld)

df_ld = pd.concat([subset_HC, subset_MS, subset_NMO], ignore_index=True)

first_column = df_ld.pop('diagnosis')
df_ld.insert(0, 'diagnosis', first_column)


# Rename the columns using the updated dictionaries
subset_HC_raw = subset_HC_raw.rename(columns=full_names_raw)
subset_MS_raw = subset_MS_raw.rename(columns=full_names_raw)
subset_NMO_raw = subset_NMO_raw.rename(columns=full_names_raw)

df_raw = pd.concat([subset_HC_raw, subset_MS_raw, subset_NMO_raw], ignore_index=True)

first_column = df_raw.pop('diagnosis')
df_raw.insert(0, 'diagnosis', first_column)

##################
###Plot ####
# Create a figure with a 7x3 subplot grid
fig, axs = plt.subplots(nrows=3, ncols=7, figsize=(30, 20))

# Flatten the axs array for easier indexing
axs = axs.flatten()

# Iterate over the tracts and plot a boxplot for each tract in each subplot
for i, tract in enumerate(df_ld.columns[1:]):
    
    # Create the boxplot
    pt.half_violinplot(data = df_ld, width = .6, palette="Set2", ax=axs[i],x='diagnosis', y=tract,)
    sns.stripplot(data = df_ld, palette="Set2", ax=axs[i],x='diagnosis', y=tract,)
    # plot the mean line
    sns.boxplot(showmeans=True,
                meanline=True,
                meanprops={'color': 'k', 'ls': '--', 'lw': 1.5},
                medianprops={'visible': False},
                whiskerprops={'visible': False},
                data=df_ld,
                showfliers=False,
                showbox=False,
                showcaps=False,
                ax=axs[i],x='diagnosis', y=tract)
        
    #add horizontal grid lines
    axs[i].yaxis.grid(True)    
    axs[i].set_title(tract)
    axs[i].set(ylabel='NDI')

# Add a main title to the figure
fig.suptitle('Lesion-dependent NDI values in MS and NMOSD vs. healthy white matter')

# Adjust spacing between subplots
fig.tight_layout()

# Show the plot
plt.show()

df_MS_HC= df_ld[df_ld['diagnosis'].isin(['HC', 'RRMS'])]
df_NMOSD_HC= df_ld[df_ld['diagnosis'].isin(['HC', 'NMOSD'])]
df_NMOSD_MS= df_ld[df_ld['diagnosis'].isin(['RRMS', 'NMOSD'])]


p_vals = []
t_stats = []
cohens_ds = []
mean_diffs = []
ci_lower = []
ci_upper = []
ratios = []

#HC vs MS
for bundle in df_ld.columns[1:]:
    t_stat, p_val = ttest_ind(df_MS_HC.loc[df_MS_HC['diagnosis'] == 'RRMS', bundle], df_MS_HC.loc[df_MS_HC['diagnosis'] == 'HC', bundle], equal_var=False, nan_policy='omit')
    t_stats.append(t_stat)
    p_vals.append(p_val)

    # Calculate the confidence interval for the mean difference and Cohen's d effect size
    ms_values = df_MS_HC.loc[df_MS_HC['diagnosis'] == 'RRMS', bundle].dropna()
    hc_values = df_MS_HC.loc[df_MS_HC['diagnosis'] == 'HC', bundle].dropna()

    mean_diff = ms_values.mean() - hc_values.mean()
    mean_diffs.append(mean_diff)

    n_ms = len(ms_values)
    n_hc = len(hc_values)

    t_crit = t.interval(0.95, df=(n_ms + n_hc - 2))[1]

    pooled_sd = np.sqrt(((n_ms - 1) * ms_values.std()**2 + (n_hc - 1) * hc_values.std()**2) / (n_ms + n_hc - 2))

    mean_diff_se = pooled_sd * np.sqrt(1 / n_ms + 1 / n_hc)

    mean_diff_CI_lower = mean_diff - t_crit * mean_diff_se
    mean_diff_CI_upper = mean_diff + t_crit * mean_diff_se

    ci_lower.append(mean_diff_CI_lower)
    ci_upper.append(mean_diff_CI_upper)

    cohens_d = mean_diff / pooled_sd
    cohens_ds.append(cohens_d)

    ratio = ms_values.std() / hc_values.std()
    ratios.append(ratio)

#HC vs NMOSD
for bundle in df_ld.columns[1:]:
    t_stat, p_val = ttest_ind(df_NMOSD_HC.loc[df_NMOSD_HC['diagnosis'] == 'NMOSD', bundle], df_NMOSD_HC.loc[df_NMOSD_HC['diagnosis'] == 'HC', bundle], equal_var=False, nan_policy='omit')
    t_stats.append(t_stat)
    p_vals.append(p_val)

    # Calculate the confidence interval for the mean difference and Cohen's d effect size
    ms_values = df_NMOSD_HC.loc[df_NMOSD_HC['diagnosis'] == 'NMOSD', bundle].dropna()
    hc_values = df_NMOSD_HC.loc[df_NMOSD_HC['diagnosis'] == 'HC', bundle].dropna()

    mean_diff = ms_values.mean() - hc_values.mean()
    mean_diffs.append(mean_diff)

    n_ms = len(ms_values)
    n_hc = len(hc_values)

    t_crit = t.interval(0.95, df=(n_ms + n_hc - 2))[1]

    pooled_sd = np.sqrt(((n_ms - 1) * ms_values.std()**2 + (n_hc - 1) * hc_values.std()**2) / (n_ms + n_hc - 2))

    mean_diff_se = pooled_sd * np.sqrt(1 / n_ms + 1 / n_hc)

    mean_diff_CI_lower = mean_diff - t_crit * mean_diff_se
    mean_diff_CI_upper = mean_diff + t_crit * mean_diff_se

    ci_lower.append(mean_diff_CI_lower)
    ci_upper.append(mean_diff_CI_upper)

    cohens_d = mean_diff / pooled_sd
    cohens_ds.append(cohens_d)

    ratio = ms_values.std() / hc_values.std()
    ratios.append(ratio)

#MS vs NMOSD
    for bundle in df_ld.columns[1:]:
        t_stat, p_val = ttest_ind(df_NMOSD_MS.loc[df_NMOSD_MS['diagnosis'] == 'NMOSD', bundle], df_NMOSD_MS.loc[df_NMOSD_MS['diagnosis'] == 'RRMS', bundle], equal_var=False, nan_policy='omit')
        t_stats.append(t_stat)
        p_vals.append(p_val)

        # Calculate the confidence interval for the mean difference and Cohen's d effect size
        ms_values = df_NMOSD_MS.loc[df_NMOSD_MS['diagnosis'] == 'NMOSD', bundle].dropna()
        hc_values = df_NMOSD_MS.loc[df_NMOSD_MS['diagnosis'] == 'RRMS', bundle].dropna()

        mean_diff = ms_values.mean() - hc_values.mean()
        mean_diffs.append(mean_diff)

        n_ms = len(ms_values)
        n_hc = len(hc_values)

        t_crit = t.interval(0.95, df=(n_ms + n_hc - 2))[1]

        pooled_sd = np.sqrt(((n_ms - 1) * ms_values.std()**2 + (n_hc - 1) * hc_values.std()**2) / (n_ms + n_hc - 2))

        mean_diff_se = pooled_sd * np.sqrt(1 / n_ms + 1 / n_hc)

        mean_diff_CI_lower = mean_diff - t_crit * mean_diff_se
        mean_diff_CI_upper = mean_diff + t_crit * mean_diff_se

        ci_lower.append(mean_diff_CI_lower)
        ci_upper.append(mean_diff_CI_upper)

        cohens_d = mean_diff / pooled_sd
        cohens_ds.append(cohens_d)

        ratio = ms_values.std() / hc_values.std()
        ratios.append(ratio)
    
# Correct for multiple comparisons using the FDR procedure and save results to PDF
p_vals_corr = smm.multipletests(p_vals, alpha=0.05, method='fdr_bh')[1]

# Create a list of values to assign to the "disease" column
disease_values = ['MS vs HC']*21 + ['HC vs NMOSD']*21+ ['NMOSD vs RRMS']*21
bundles_concatenated_index = pd.concat([df_ld.columns[1:].to_frame()]*3)
bundles_concatenated_index = bundles_concatenated_index.reset_index(drop=True).squeeze()


results_df = pd.DataFrame({
    'Comparison': disease_values,
    'Bundle': bundles_concatenated_index,
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


results_df.to_csv('/Volumes/ms/seropositive_project/csv_results/LD_MS_NMOSD_vs_HC.csv', index=False)

#######RAW############
##################
###Plot ####
# Create a figure with a 7x3 subplot grid
fig, axs = plt.subplots(nrows=3, ncols=7, figsize=(30, 20))

# Flatten the axs array for easier indexing
axs = axs.flatten()

# Iterate over the tracts and plot a boxplot for each tract in each subplot
for i, tract in enumerate(df_raw.columns[1:]):
    
    # Create the boxplot
    pt.half_violinplot(data = df_raw, width = .6, palette="Set2", ax=axs[i],x='diagnosis', y=tract,)
    sns.stripplot(data = df_raw, palette="Set2", ax=axs[i],x='diagnosis', y=tract,)
    # plot the mean line
    sns.boxplot(showmeans=True,
                meanline=True,
                meanprops={'color': 'k', 'ls': '--', 'lw': 1.5},
                medianprops={'visible': False},
                whiskerprops={'visible': False},
                data=df_raw,
                showfliers=False,
                showbox=False,
                showcaps=False,
                ax=axs[i],x='diagnosis', y=tract)
        
    #add horizontal grid lines
    axs[i].yaxis.grid(True)    
    axs[i].set_title(tract)
    axs[i].set(ylabel='NDI')

# Add a main title to the figure
fig.suptitle('Tractometry derived NDI values in MS, NMOSD and HC')

# Adjust spacing between subplots
fig.tight_layout()

# Show the plot
plt.show()

df_MS_HC= df_raw[df_raw['diagnosis'].isin(['HC', 'RRMS'])]
df_NMOSD_HC= df_raw[df_raw['diagnosis'].isin(['HC', 'NMOSD'])]
df_NMOSD_MS= df_raw[df_raw['diagnosis'].isin(['RRMS', 'NMOSD'])]


p_vals = []
t_stats = []
cohens_ds = []
mean_diffs = []
ci_lower = []
ci_upper = []
ratios = []

#HC vs MS
for bundle in df_raw.columns[1:]:
    t_stat, p_val = ttest_ind(df_MS_HC.loc[df_MS_HC['diagnosis'] == 'RRMS', bundle], df_MS_HC.loc[df_MS_HC['diagnosis'] == 'HC', bundle], equal_var=False, nan_policy='omit')
    t_stats.append(t_stat)
    p_vals.append(p_val)

    # Calculate the confidence interval for the mean difference and Cohen's d effect size
    ms_values = df_MS_HC.loc[df_MS_HC['diagnosis'] == 'RRMS', bundle].dropna()
    hc_values = df_MS_HC.loc[df_MS_HC['diagnosis'] == 'HC', bundle].dropna()

    mean_diff = ms_values.mean() - hc_values.mean()
    mean_diffs.append(mean_diff)

    n_ms = len(ms_values)
    n_hc = len(hc_values)

    t_crit = t.interval(0.95, df=(n_ms + n_hc - 2))[1]

    pooled_sd = np.sqrt(((n_ms - 1) * ms_values.std()**2 + (n_hc - 1) * hc_values.std()**2) / (n_ms + n_hc - 2))

    mean_diff_se = pooled_sd * np.sqrt(1 / n_ms + 1 / n_hc)

    mean_diff_CI_lower = mean_diff - t_crit * mean_diff_se
    mean_diff_CI_upper = mean_diff + t_crit * mean_diff_se

    ci_lower.append(mean_diff_CI_lower)
    ci_upper.append(mean_diff_CI_upper)

    cohens_d = mean_diff / pooled_sd
    cohens_ds.append(cohens_d)

    ratio = ms_values.std() / hc_values.std()
    ratios.append(ratio)

#HC vs NMOSD
for bundle in df_raw.columns[1:]:
    t_stat, p_val = ttest_ind(df_NMOSD_HC.loc[df_NMOSD_HC['diagnosis'] == 'NMOSD', bundle], df_NMOSD_HC.loc[df_NMOSD_HC['diagnosis'] == 'HC', bundle], equal_var=False, nan_policy='omit')
    t_stats.append(t_stat)
    p_vals.append(p_val)

    # Calculate the confidence interval for the mean difference and Cohen's d effect size
    ms_values = df_NMOSD_HC.loc[df_NMOSD_HC['diagnosis'] == 'NMOSD', bundle].dropna()
    hc_values = df_NMOSD_HC.loc[df_NMOSD_HC['diagnosis'] == 'HC', bundle].dropna()

    mean_diff = ms_values.mean() - hc_values.mean()
    mean_diffs.append(mean_diff)

    n_ms = len(ms_values)
    n_hc = len(hc_values)

    t_crit = t.interval(0.95, df=(n_ms + n_hc - 2))[1]

    pooled_sd = np.sqrt(((n_ms - 1) * ms_values.std()**2 + (n_hc - 1) * hc_values.std()**2) / (n_ms + n_hc - 2))

    mean_diff_se = pooled_sd * np.sqrt(1 / n_ms + 1 / n_hc)

    mean_diff_CI_lower = mean_diff - t_crit * mean_diff_se
    mean_diff_CI_upper = mean_diff + t_crit * mean_diff_se

    ci_lower.append(mean_diff_CI_lower)
    ci_upper.append(mean_diff_CI_upper)

    cohens_d = mean_diff / pooled_sd
    cohens_ds.append(cohens_d)

    ratio = ms_values.std() / hc_values.std()
    ratios.append(ratio)

#MS vs NMOSD
for bundle in df_raw.columns[1:]:
    t_stat, p_val = ttest_ind(df_NMOSD_MS.loc[df_NMOSD_MS['diagnosis'] == 'NMOSD', bundle], df_NMOSD_MS.loc[df_NMOSD_MS['diagnosis'] == 'RRMS', bundle], equal_var=False, nan_policy='omit')
    t_stats.append(t_stat)
    p_vals.append(p_val)

    # Calculate the confidence interval for the mean difference and Cohen's d effect size
    ms_values = df_NMOSD_MS.loc[df_NMOSD_MS['diagnosis'] == 'NMOSD', bundle].dropna()
    hc_values = df_NMOSD_MS.loc[df_NMOSD_MS['diagnosis'] == 'RRMS', bundle].dropna()

    mean_diff = ms_values.mean() - hc_values.mean()
    mean_diffs.append(mean_diff)

    n_ms = len(ms_values)
    n_hc = len(hc_values)

    t_crit = t.interval(0.95, df=(n_ms + n_hc - 2))[1]

    pooled_sd = np.sqrt(((n_ms - 1) * ms_values.std()**2 + (n_hc - 1) * hc_values.std()**2) / (n_ms + n_hc - 2))

    mean_diff_se = pooled_sd * np.sqrt(1 / n_ms + 1 / n_hc)

    mean_diff_CI_lower = mean_diff - t_crit * mean_diff_se
    mean_diff_CI_upper = mean_diff + t_crit * mean_diff_se

    ci_lower.append(mean_diff_CI_lower)
    ci_upper.append(mean_diff_CI_upper)

    cohens_d = mean_diff / pooled_sd
    cohens_ds.append(cohens_d)

    ratio = ms_values.std() / hc_values.std()
    ratios.append(ratio)
    
# Correct for multiple comparisons using the FDR procedure and save results to PDF
p_vals_corr = smm.multipletests(p_vals, alpha=0.05, method='fdr_bh')[1]

# Create a list of values to assign to the "disease" column
disease_values = ['MS vs HC']*21 + ['HC vs NMOSD']*21 + ['NMOSD vs RRMS']*21
bundles_concatenated_index = pd.concat([df_raw.columns[1:].to_frame()]*3)
bundles_concatenated_index = bundles_concatenated_index.reset_index(drop=True).squeeze()


results_df = pd.DataFrame({
    'Comparison': disease_values,
    'Bundle': bundles_concatenated_index,
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


results_df.to_csv('/Volumes/ms/seropositive_project/csv_results/RAW_MS_NMOSD_vs_HC.csv', index=False)



