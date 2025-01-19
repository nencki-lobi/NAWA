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

column_mapping = {
    'lh_gs_frontomargin': 'lh_Fronto-marginal gyrus (of Wernicke) and sulcus',
    'rh_gs_frontomargin': 'rh_Fronto-marginal gyrus (of Wernicke) and sulcus',
    'lh_gs_occipital_inf': 'lh_Inferior occipital gyrus (o3) and sulcus',
    'rh_gs_occipital_inf': 'rh_Inferior occipital gyrus (o3) and sulcus',
    'lh_gs_paracentral': 'lh_paracentral lobule and sulcus',
    'rh_gs_paracentral': 'rh_paracentral lobule and sulcus',
    'lh_gs_subcentral': 'lh_subcentral gyrus (central operculum) and sulci',
    'rh_gs_subcentral': 'rh_subcentral gyrus (central operculum) and sulci',
    'lh_gs_transv_frontopol': 'lh_transverse frontopolar gyri and sulci',
    'rh_gs_transv_frontopol': 'rh_transverse frontopolar gyri and sulci',
    'lh_gs_cingulant': 'lh_anterior part of the cingulate gyrus and sulcus (aCC)',
    'rh_gs_cingulant': 'rh_anterior part of the cingulate gyrus and sulcus (aCC)',
    'lh_gs_cingulmidant': 'lh_middle-anterior part of the cingulate gyrus and sulcus (amCC)',
    'rh_gs_cingulmidant': 'rh_middle-anterior part of the cingulate gyrus and sulcus (amCC)',
    'lh_gs_cingulmidpost': 'lh_middle-posterior part of the cingulate gyrus and sulcus (pmCC)',
    'rh_gs_cingulmidpost': 'rh_middle-posterior part of the cingulate gyrus and sulcus (pmCC)',
    'lh_g_cingulpostdorsal': 'lh_posterior-dorsal part of the cingulate gyrus (dpCC)',
    'rh_g_cingulpostdorsal': 'rh_posterior-dorsal part of the cingulate gyrus (dpCC)',
    'lh_g_cingulpostventral': 'lh_posterior-ventral part of the cingulate gyrus (vpCC, isthmus of the cingulate gyrus)',
    'rh_g_cingulpostventral': 'rh_posterior-ventral part of the cingulate gyrus (vpCC, isthmus of the cingulate gyrus)',
    'lh_g_cuneus': 'lh_Cuneus (o6)',
    'rh_g_cuneus': 'rh_Cuneus (o6)',
    'lh_g_front_infopercular': 'lh_opercular part of the inferior frontal gyrus',
    'rh_g_front_infopercular': 'rh_opercular part of the inferior frontal gyrus',
    'lh_g_front_inforbital': 'lh_orbital part of the inferior frontal gyrus',
    'rh_g_front_inforbital': 'rh_orbital part of the inferior frontal gyrus',
    'lh_g_front_inftriangul': 'lh_triangular part of the inferior frontal gyrus',
    'rh_g_front_inftriangul': 'rh_triangular part of the inferior frontal gyrus',
    'lh_g_front_middle': 'lh_middle frontal gyrus (F2)',
    'rh_g_front_middle': 'rh_middle frontal gyrus (F2)',
    'lh_g_front_sup': 'lh_superior frontal gyrus (F1)',
    'rh_g_front_sup': 'rh_superior frontal gyrus (F1)',
    'lh_g_ins_lgs_cent_ins': 'lh_long insular gyrus and central sulcus of the insula',
    'rh_g_ins_lgs_cent_ins': 'rh_long insular gyrus and central sulcus of the insula',
    'lh_g_insular_short': 'lh_short insular gyri',
    'rh_g_insular_short': 'rh_short insular gyri',
    'lh_g_occipital_middle': 'lh_middle occipital gyrus (o2, lateral occipital gyrus)',
    'rh_g_occipital_middle': 'rh_middle occipital gyrus (o2, lateral occipital gyrus)',
    'lh_g_occipital_sup': 'lh_superior occipital gyrus (o1)',
    'rh_g_occipital_sup': 'rh_superior occipital gyrus (o1)',
    'lh_g_octemp_latfusifor': 'lh_lateral occipito-temporal gyrus (fusiform gyrus, o4-t4)',
    'rh_g_octemp_latfusifor': 'rh_lateral occipito-temporal gyrus (fusiform gyrus, o4-t4)',
    'lh_g_octemp_medlingual': 'lh_lingual gyrus, lingual part of the medial occipito-temporal gyrus, (o5)',
    'rh_g_octemp_medlingual': 'rh_lingual gyrus, lingual part of the medial occipito-temporal gyrus, (o5)',
    'lh_g_octemp_medparahip': 'lh_parahippocampal gyrus, parahippocampal part of the medial occipito-temporal gyrus, (t5)',
    'rh_g_octemp_medparahip': 'rh_parahippocampal gyrus, parahippocampal part of the medial occipito-temporal gyrus, (t5)',
    'lh_g_orbital': 'lh_orbital gyri',
    'rh_g_orbital': 'rh_orbital gyri',
    'lh_g_pariet_infangular': 'lh_angular gyrus',
    'rh_g_pariet_infangular': 'rh_angular gyrus',
    'lh_g_pariet_infsupramar': 'lh_supramarginal gyrus',
    'rh_g_pariet_infsupramar': 'rh_supramarginal gyrus',
    'lh_g_parietal_sup': 'lh_superior parietal lobule (lateral part of p1)',
    'rh_g_parietal_sup': 'rh_superior parietal lobule (lateral part of p1)',
    'lh_g_postcentral': 'lh_postcentral gyrus',
    'rh_g_postcentral': 'rh_postcentral gyrus',
    'lh_g_precentral': 'lh_precentral gyrus',
    'rh_g_precentral': 'rh_precentral gyrus',
    'lh_g_precuneus': 'lh_precuneus (medial part of p1)',
    'rh_g_precuneus': 'rh_precuneus (medial part of p1)',
    'lh_g_rectus': 'lh_straight gyrus, gyrus rectus',
    'rh_g_rectus': 'rh_straight gyrus, gyrus rectus',
    'lh_g_subcallosal': 'lh_subcallosal area, subcallosal gyrus',
    'rh_g_subcallosal': 'rh_subcallosal area, subcallosal gyrus',
    'lh_g_temp_supg_t_transv': 'lh_anterior transverse temporal gyrus (of heschl)',
    'rh_g_temp_supg_t_transv': 'rh_anterior transverse temporal gyrus (of heschl)',
    'lh_g_temp_suplateral': 'lh_lateral aspect of the superior temporal gyrus',
    'rh_g_temp_suplateral': 'rh_lateral aspect of the superior temporal gyrus',
    'lh_g_temp_supplan_polar': 'lh_planum polare of the superior temporal gyrus',
    'rh_g_temp_supplan_polar': 'rh_planum polare of the superior temporal gyrus',
    'lh_g_temp_supplan_tempo': 'lh_planum temporale or temporal plane of the superior temporal gyrus',
    'rh_g_temp_supplan_tempo': 'rh_planum temporale or temporal plane of the superior temporal gyrus',
    'lh_g_temporal_inf': 'lh_Inferior temporal gyrus (t3)',
    'rh_g_temporal_inf': 'rh_Inferior temporal gyrus (t3)',
    'lh_g_temporal_middle': 'lh_middle temporal gyrus (t2)',
    'rh_g_temporal_middle': 'rh_middle temporal gyrus (t2)',
    'lh_lat_fisanthorizont': 'lh_horizontal ramus of the anterior segment of the lateral sulcus (or fissure)',
    'rh_lat_fisanthorizont': 'rh_horizontal ramus of the anterior segment of the lateral sulcus (or fissure)',
    'lh_lat_fisantvertical': 'lh_vertical ramus of the anterior segment of the lateral sulcus (or fissure)',
    'rh_lat_fisantvertical': 'rh_vertical ramus of the anterior segment of the lateral sulcus (or fissure)',
    'lh_lat_fispost': 'lh_posterior ramus (or segment) of the lateral sulcus (or fissure)',
    'rh_lat_fispost': 'rh_posterior ramus (or segment) of the lateral sulcus (or fissure)',
    'lh_pole_occipital': 'lh_occipital pole',
    'rh_pole_occipital': 'rh_occipital pole',
    'lh_pole_temporal': 'lh_temporal pole',
    'rh_pole_temporal': 'rh_temporal pole',
    'lh_s_calcarine': 'lh_Calcarine sulcus',
    'rh_s_calcarine': 'rh_Calcarine sulcus',
    'lh_s_central': 'lh_Central sulcus (Rolando\'s fissure)',
    'rh_s_central': 'rh_Central sulcus (Rolando\'s fissure)',
    'lh_s_cingulmarginalis': 'lh_marginal sulcus of cingulate gyrus',
    'rh_s_cingulmarginalis': 'rh_marginal sulcus of cingulate gyrus',
    'lh_s_circular_insula_ant': 'lh_anterior circular sulcus of the insula',
    'rh_s_circular_insula_ant': 'rh_anterior circular sulcus of the insula',
    'lh_s_circular_insula_inf': 'lh_Inferior circular sulcus of the insula',
    'rh_s_circular_insula_inf': 'rh_Inferior circular sulcus of the insula',
    'lh_s_circular_insula_sup': 'lh_superior circular sulcus of the insula',
    'rh_s_circular_insula_sup': 'rh_superior circular sulcus of the insula',
    'lh_s_collat_transv_ant': 'lh_anterior transverse collateral sulcus',
    'rh_s_collat_transv_ant': 'rh_anterior transverse collateral sulcus',
    'lh_s_collat_transv_post': 'lh_posterior transverse collateral sulcus',
    'rh_s_collat_transv_post': 'rh_posterior transverse collateral sulcus',
    'lh_s_front_inf': 'lh_Inferior frontal sulcus',
    'rh_s_front_inf': 'rh_Inferior frontal sulcus',
    'lh_s_front_middle': 'lh_middle frontal sulcus',
    'rh_s_front_middle': 'rh_middle frontal sulcus',
    'lh_s_front_sup': 'lh_superior frontal sulcus',
    'rh_s_front_sup': 'rh_superior frontal sulcus',
    'lh_s_interm_primjensen': 'lh_Intermediate sulcus of Jensen',
    'rh_s_interm_primjensen': 'rh_Intermediate sulcus of Jensen',
    'lh_s_intraparietp_trans': 'lh_Intraparietal sulcus and posterior transverse parietal sulcus',
    'rh_s_intraparietp_trans': 'rh_Intraparietal sulcus and posterior transverse parietal sulcus',
    'lh_s_oc_middlelunatus': 'lh_middle occipital sulcus and sulcus lunatus (secondary intermediate sulcus)',
    'rh_s_oc_middlelunatus': 'rh_middle occipital sulcus and sulcus lunatus (secondary intermediate sulcus)',
    'lh_s_oc_suptransversal': 'lh_superior occipital sulcus and transverse occipital sulcus (superior intermediate sulcus)',
    'rh_s_oc_suptransversal': 'rh_superior occipital sulcus and transverse occipital sulcus (superior intermediate sulcus)',
    'lh_s_occipital_ant': 'lh_anterior occipital sulcus',
    'rh_s_occipital_ant': 'rh_anterior occipital sulcus',
    'lh_s_octemp_lat': 'lh_lateral occipito-temporal sulcus',
    'rh_s_octemp_lat': 'rh_lateral occipito-temporal sulcus',
    'lh_s_octemp_medlingual': 'lh_medial occipito-temporal sulcus and lingual sulcus',
    'rh_s_octemp_medlingual': 'rh_medial occipito-temporal sulcus and lingual sulcus',
    'lh_s_orbital_lateral': 'lh_lateral orbital sulcus',
    'rh_s_orbital_lateral': 'rh_lateral orbital sulcus',
    'lh_s_orbital_medolfact': 'lh_medial orbital sulcus, olfactory sulcus',
    'rh_s_orbital_medolfact': 'rh_medial orbital sulcus, olfactory sulcus',
    'lh_s_orbitalh_shaped': 'lh_h-shaped orbital sulcus',
    'rh_s_orbitalh_shaped': 'rh_h-shaped orbital sulcus',
    'lh_s_parieto_occipital': 'lh_parieto-occipital sulcus',
    'rh_s_parieto_occipital': 'rh_parieto-occipital sulcus',
    'lh_s_pericallosal': 'lh_pericallosal sulcus',
    'rh_s_pericallosal': 'rh_pericallosal sulcus',
    'lh_s_postcentral': 'lh_postcentral sulcus',
    'rh_s_postcentral': 'rh_postcentral sulcus',
    'lh_s_precentralinfpart': 'lh_Inferior part of the precentral sulcus',
    'rh_s_precentralinfpart': 'rh_Inferior part of the precentral sulcus',
    'lh_s_precentralsuppart': 'lh_superior part of the precentral sulcus',
    'rh_s_precentralsuppart': 'rh_superior part of the precentral sulcus',
    'lh_s_suborbital': 'lh_suborbital sulcus',
    'rh_s_suborbital': 'rh_suborbital sulcus',
    'lh_s_subparietal': 'lh_subparietal sulcus',
    'rh_s_subparietal': 'rh_subparietal sulcus',
    'lh_s_temporal_inf': 'lh_Inferior temporal sulcus',
    'rh_s_temporal_inf': 'rh_Inferior temporal sulcus',
    'lh_s_temporal_sup': 'lh_superior temporal sulcus',
    'rh_s_temporal_sup': 'rh_superior temporal sulcus',
    'lh_s_temporal_transverse': 'lh_transverse temporal sulcus (heschl\'s gyrus)',
    'rh_s_temporal_transverse': 'rh_transverse temporal sulcus (heschl\'s gyrus)',
    'lh_s_temporalpole': 'lh_temporal pole',
    'rh_s_temporalpole': 'rh_temporal pole',
    'lh_temporal_Inf': 'lh_Inferior temporal sulcus',
    'rh_temporal_Inf': 'rh_Inferior temporal sulcus',
    'lh_temporal_mid': 'lh_middle temporal sulcus',
    'rh_temporal_mid': 'rh_middle temporal sulcus',
    'lh_temporal_pole': 'lh_temporal pole',
    'rh_temporal_pole': 'rh_temporal pole',
    'lh_temporal_sup': 'lh_superior temporal sulcus',
    'rh_temporal_sup': 'rh_superior temporal sulcus',
    'lh_temporal_trans': 'lh_transverse temporal sulcus (heschl\'s sulcus)',
    'rh_temporal_trans': 'rh_transverse temporal sulcus (heschl\'s sulcus)'
}


# Set float_format to display up to 3 decimal places
pd.options.display.float_format = '{:.3f}'.format

#read in the data
df = pd.read_csv("/Volumes/ms/PJ_gRatio/Stata/data_ready.csv", sep=',')

# Subset the DataFrame based on a column value
subset_HC = df.loc[df['diagnosis'] == 'HC', 'lh_unknown':'rh_s_temporal_transverse']
subset_HC['diagnosis'] = 'HC'

subset_MS = df.loc[df['diagnosis'] == 'RRMS', 'lh_unknown':'rh_s_temporal_transverse']
subset_MS['diagnosis'] = 'RRMS'

subset_NMO = df.loc[df['diagnosis'] == 'NMOSD', 'lh_unknown':'rh_s_temporal_transverse']
subset_NMO['diagnosis'] = 'NMOSD'


# Rename the columns using the updated dictionaries
subset_HC = subset_HC.rename(columns=column_mapping)
subset_MS = subset_MS.rename(columns=column_mapping)
subset_NMO = subset_NMO.rename(columns=column_mapping)


df_cortex = pd.concat([subset_HC, subset_MS, subset_NMO], ignore_index=True)

first_column = df_cortex.pop('diagnosis')
df_cortex.insert(0, 'diagnosis', first_column)


df_MS_HC= df_cortex[df_cortex['diagnosis'].isin(['HC', 'RRMS'])]
df_NMOSD_HC= df_cortex[df_cortex['diagnosis'].isin(['HC', 'NMOSD'])]
df_NMOSD_MS= df_cortex[df_cortex['diagnosis'].isin(['RRMS', 'NMOSD'])]


p_vals = []
t_stats = []
cohens_ds = []
mean_diffs = []
ci_lower = []
ci_upper = []
ratios = []

#HC vs MS
for parcelletion in df_cortex.columns[1:]:
    t_stat, p_val = ttest_ind(df_MS_HC.loc[df_MS_HC['diagnosis'] == 'RRMS', parcelletion], df_MS_HC.loc[df_MS_HC['diagnosis'] == 'HC', parcelletion], equal_var=False, nan_policy='omit')
    t_stats.append(t_stat)
    p_vals.append(p_val)

    # Calculate the confidence interval for the mean difference and Cohen's d effect size
    ms_values = df_MS_HC.loc[df_MS_HC['diagnosis'] == 'RRMS', parcelletion].dropna()
    hc_values = df_MS_HC.loc[df_MS_HC['diagnosis'] == 'HC', parcelletion].dropna()

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
for parcelletion in df_cortex.columns[1:]:
    t_stat, p_val = ttest_ind(df_NMOSD_HC.loc[df_NMOSD_HC['diagnosis'] == 'NMOSD', parcelletion], df_NMOSD_HC.loc[df_NMOSD_HC['diagnosis'] == 'HC', parcelletion], equal_var=False, nan_policy='omit')
    t_stats.append(t_stat)
    p_vals.append(p_val)

    # Calculate the confidence interval for the mean difference and Cohen's d effect size
    ms_values = df_NMOSD_HC.loc[df_NMOSD_HC['diagnosis'] == 'NMOSD', parcelletion].dropna()
    hc_values = df_NMOSD_HC.loc[df_NMOSD_HC['diagnosis'] == 'HC', parcelletion].dropna()

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
    for parcelletion in df_cortex.columns[1:]:
        t_stat, p_val = ttest_ind(df_NMOSD_MS.loc[df_NMOSD_MS['diagnosis'] == 'NMOSD', parcelletion], df_NMOSD_MS.loc[df_NMOSD_MS['diagnosis'] == 'RRMS', parcelletion], equal_var=False, nan_policy='omit')
        t_stats.append(t_stat)
        p_vals.append(p_val)

        # Calculate the confidence interval for the mean difference and Cohen's d effect size
        ms_values = df_NMOSD_MS.loc[df_NMOSD_MS['diagnosis'] == 'NMOSD', parcelletion].dropna()
        hc_values = df_NMOSD_MS.loc[df_NMOSD_MS['diagnosis'] == 'RRMS', parcelletion].dropna()

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
disease_values = ['MS vs HC']*150 + ['HC vs NMOSD']*150+ ['NMOSD vs RRMS']*150
parcelletions_concatenated_index = pd.concat([df_cortex.columns[1:].to_frame()]*3)
parcelletions_concatenated_index = parcelletions_concatenated_index.reset_index(drop=True).squeeze()


results_df = pd.DataFrame({
    'Comparison': disease_values,
    'parcelletion': parcelletions_concatenated_index,
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


results_df.to_csv('/Volumes/ms/seropositive_project/csv_results/cortex_parcels_t-tests.csv', index=False)

results_grouped = results_df.sort_values(by=['Comparison', 'Corrected P-value'])


results_grouped.to_csv('/Volumes/ms/seropositive_project/csv_results/cortex_parcels_t-tests.csv', index=False)

