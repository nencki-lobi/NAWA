#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 10:41:24 2024

@author: paweljakuszyk
"""

import pandas as pd
from scipy.stats import kruskal
import scikit_posthocs as sp
import ptitprince as pt
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("/Users/paweljakuszyk/Documents/NAWA-Seropositivedatabase.csv", sep=';')


df['TM_and_diagnosis']=''

df = df[~((df['Diagnosis'] == 'NMOSD') & (df['Transverse myelitis'] == 'No'))]

# Updating 'TM_and_diagnosis' column where diagnosis is 'RRMS' and TM is 'Yes'
df.loc[(df['Diagnosis'] == 'RRMS') & (df['Transverse myelitis'] == 'Yes'), 'TM_and_diagnosis'] = 'RRMS_TM+'

df.loc[(df['Diagnosis'] == 'RRMS') & (df['Transverse myelitis'] == 'No'), 'TM_and_diagnosis'] = 'RRMS_TM-'

df.loc[(df['Diagnosis'] == 'NMOSD')& (df['Transverse myelitis'] == 'Yes'), 'TM_and_diagnosis'] = 'NMOSD_TM+'

df.loc[(df['Diagnosis'] == 'HC'), 'TM_and_diagnosis'] = 'HC'


##MEAN CSA
groups = df.groupby('TM_and_diagnosis')['Mean CSA'].apply(list)

# Create arrays for each group
rrms_tm_plus_measurements = groups.get('RRMS_TM+', [])
rrms_tm_minus_measurements = groups.get('RRMS_TM-', [])
hc_measurements = groups.get('HC', [])
nmosd_measurements = groups.get('NMOSD_TM+', [])



# Perform Kruskal-Wallis test
statistic, p_value = kruskal(nmosd_measurements,rrms_tm_plus_measurements,hc_measurements, nan_policy='omit')



# Output the results
print("Kruskal-Wallis Test:")
print("Statistic:", statistic)
print("p-value:", p_value)


# Perform post hoc Dunn's test
dunn_results = sp.posthoc_dunn([nmosd_measurements, rrms_tm_plus_measurements, hc_measurements], p_adjust='fdr_bh')

print("\nDunn's Test Results:")
print(dunn_results)


data = [
        nmosd_measurements,
        rrms_tm_plus_measurements, 
        rrms_tm_minus_measurements,
        hc_measurements, 
        ]


# Set up the figure and axis
fig, ax = plt.subplots()

ax = pt.half_violinplot(data = data, width = .6, palette="Set2")
ax = sns.stripplot(data = data, palette="Set2")
# plot the mean line
ax = sns.boxplot(showmeans=True,
            meanline=True,
            meanprops={'color': 'k', 'ls': '--', 'lw': 1.5},
            medianprops={'visible': False},
            whiskerprops={'visible': False},
            data=data,
            showfliers=False,
            showbox=False,
            showcaps=False,
            ax=ax)

#add horizontal grid lines
ax.yaxis.grid(True)   

# Set the x-axis tick labels
ax.set_xticklabels(['NMOSD', 'MS_TM+','MS_TM-','HC'])

# Add a title and y-axis label
ax.set_title('Mean CSA per group')
ax.set_ylabel('Mean CSA')

# Show the plot
plt.show()



##FA_WM
groups = df.groupby('TM_and_diagnosis')['FA_WM'].apply(list)

# Create arrays for each group
rrms_tm_plus_measurements = groups.get('RRMS_TM+', [])
rrms_tm_minus_measurements = groups.get('RRMS_TM-', [])
hc_measurements = groups.get('HC', [])
nmosd_measurements = groups.get('NMOSD_TM+', [])



# Perform Kruskal-Wallis test
statistic, p_value = kruskal(nmosd_measurements,rrms_tm_plus_measurements,hc_measurements, nan_policy='omit')



# Output the results
print("Kruskal-Wallis Test:")
print("Statistic:", statistic)
print("p-value:", p_value)


# Perform post hoc Dunn's test
dunn_results = sp.posthoc_dunn([nmosd_measurements, rrms_tm_plus_measurements, hc_measurements], p_adjust='fdr_bh')

print("\nDunn's Test Results:")
print(dunn_results)


data = [
        nmosd_measurements,
        rrms_tm_plus_measurements, 
        rrms_tm_minus_measurements,
        hc_measurements, 
        ]


# Set up the figure and axis
fig, ax = plt.subplots()

ax = pt.half_violinplot(data = data, width = .6, palette="Set2")
ax = sns.stripplot(data = data, palette="Set2")
# plot the mean line
ax = sns.boxplot(showmeans=True,
            meanline=True,
            meanprops={'color': 'k', 'ls': '--', 'lw': 1.5},
            medianprops={'visible': False},
            whiskerprops={'visible': False},
            data=data,
            showfliers=False,
            showbox=False,
            showcaps=False,
            ax=ax)

#add horizontal grid lines
ax.yaxis.grid(True)   

# Set the x-axis tick labels
ax.set_xticklabels(['NMOSD', 'MS_TM+','MS_TM-','HC'])

# Add a title and y-axis label
ax.set_title('FA in white matter per group')
ax.set_ylabel('FA WM')

# Show the plot
plt.show()


#dorsal_col_FA
groups = df.groupby('TM_and_diagnosis')['dorsal_col_FA'].apply(list)

# Create arrays for each group
rrms_tm_plus_measurements = groups.get('RRMS_TM+', [])
rrms_tm_minus_measurements = groups.get('RRMS_TM-', [])
hc_measurements = groups.get('HC', [])
nmosd_measurements = groups.get('NMOSD', [])



# Perform Kruskal-Wallis test
statistic, p_value = kruskal(nmosd_measurements,rrms_tm_plus_measurements,rrms_tm_minus_measurements,hc_measurements, nan_policy='omit')



# Output the results
print("Kruskal-Wallis Test:")
print("Statistic:", statistic)
print("p-value:", p_value)


# Perform post hoc Dunn's test
dunn_results = sp.posthoc_dunn([nmosd_measurements, rrms_tm_plus_measurements, rrms_tm_minus_measurements, hc_measurements], p_adjust='fdr_bh')

print("\nDunn's Test Results:")
print(dunn_results)


data = [
        nmosd_measurements,
        rrms_tm_plus_measurements, 
        rrms_tm_minus_measurements,
        hc_measurements, 
        ]


# Set up the figure and axis
fig, ax = plt.subplots()

ax = pt.half_violinplot(data = data, width = .6, palette="Set2")
ax = sns.stripplot(data = data, palette="Set2")
# plot the mean line
ax = sns.boxplot(showmeans=True,
            meanline=True,
            meanprops={'color': 'k', 'ls': '--', 'lw': 1.5},
            medianprops={'visible': False},
            whiskerprops={'visible': False},
            data=data,
            showfliers=False,
            showbox=False,
            showcaps=False,
            ax=ax)

#add horizontal grid lines
ax.yaxis.grid(True)   

# Set the x-axis tick labels
ax.set_xticklabels(['NMOSD', 'MS_TM+','MS_TM-','HC'])

# Add a title and y-axis label
ax.set_title('Dorsal column FA per group')
ax.set_ylabel('FA')

# Show the plot
plt.show()


#CST_FA_spine
groups = df.groupby('TM_and_diagnosis')['CST_FA_spine'].apply(list)

# Create arrays for each group
rrms_tm_plus_measurements = groups.get('RRMS_TM+', [])
rrms_tm_minus_measurements = groups.get('RRMS_TM-', [])
hc_measurements = groups.get('HC', [])
nmosd_measurements = groups.get('NMOSD', [])



# Perform Kruskal-Wallis test
statistic, p_value = kruskal(nmosd_measurements,rrms_tm_plus_measurements,rrms_tm_minus_measurements,hc_measurements, nan_policy='omit')



# Output the results
print("Kruskal-Wallis Test:")
print("Statistic:", statistic)
print("p-value:", p_value)


# Perform post hoc Dunn's test
dunn_results = sp.posthoc_dunn([nmosd_measurements, rrms_tm_plus_measurements, rrms_tm_minus_measurements, hc_measurements], p_adjust='fdr_bh')

print("\nDunn's Test Results:")
print(dunn_results)


data = [
        nmosd_measurements,
        rrms_tm_plus_measurements, 
        rrms_tm_minus_measurements,
        hc_measurements, 
        ]


# Set up the figure and axis
fig, ax = plt.subplots()

ax = pt.half_violinplot(data = data, width = .6, palette="Set2")
ax = sns.stripplot(data = data, palette="Set2")
# plot the mean line
ax = sns.boxplot(showmeans=True,
            meanline=True,
            meanprops={'color': 'k', 'ls': '--', 'lw': 1.5},
            medianprops={'visible': False},
            whiskerprops={'visible': False},
            data=data,
            showfliers=False,
            showbox=False,
            showcaps=False,
            ax=ax)

#add horizontal grid lines
ax.yaxis.grid(True)   

# Set the x-axis tick labels
ax.set_xticklabels(['NMOSD', 'MS_TM+','MS_TM-','HC'])

# Add a title and y-axis label
ax.set_title('CST FA per group')
ax.set_ylabel('FA')

# Show the plot
plt.show()