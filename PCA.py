#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 11:34:09 2023

@author: paweljakuszyk
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import scipy.stats as stats
import statsmodels.stats.multitest as smm
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from scipy.stats import pearsonr
#read in the data
df = pd.read_csv("/Volumes/ms/PJ_gRatio/Stata/data_ready.csv", sep=',')


#subset data to have separate 
LIT = df.loc[:,'lit_af_left':'lit_uf_right']
LD = df.loc[:,'ld_af_left':'ld_uf_right']
cortex = df.loc[:,'lh_unknown':'rh_s_temporal_transverse']

labels = df['diagnosis']

##FIRST just the white matter
##LD
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(LD)

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)

# Perform PCA
pca = PCA()
X_pca_tracts_LD = pca.fit_transform(X_scaled)

# Calculate explained variance
explained_variance = pca.explained_variance_ratio_
cumulative_variance = np.cumsum(explained_variance)

# Create a Scree plot with colored points
plt.figure(figsize=(8, 6))
plt.plot(range(1, len(cumulative_variance) + 1), cumulative_variance, marker='o', linestyle='--')
plt.title('Scree Plot')
plt.xlabel('Number of Components')
plt.ylabel('Explained Variance')
plt.grid()
plt.legend()
plt.show()

# Assuming you have performed PCA and obtained 50 principal components
# X_pca is a 2D array with the principal components

# Select the first two principal components (PC1 and PC2)
X_pca_first_two = X_pca_tracts_LD[:, :2]
# Create a DataFrame for the first two principal components
pca_df = pd.DataFrame(data=X_pca_first_two, columns=['PC1', 'PC2'])
# Add the 'diagnosis' column from your original DataFrame for labels
pca_df['diagnosis'] = df['diagnosis']

# Define unique labels (e.g., 'M' and 'B' for malignant and benign)
unique_labels = pca_df['diagnosis'].unique()

# Create a scatter plot with labeled points
plt.figure(figsize=(10, 6))

for label in unique_labels:
    data = pca_df[pca_df['diagnosis'] == label]
    plt.scatter(data['PC1'], data['PC2'], label=label)

plt.title('PCA Score Plot with Labeled Observations')
plt.xlabel('Principal Component 1 (PC1)')
plt.ylabel('Principal Component 2 (PC2)')
plt.legend()
plt.grid()
plt.show()

# Assuming you have performed PCA and obtained 3 principal components
# X_pca_first_three is a 2D array with the first three principal components
X_pca_first_three = X_pca_tracts_LD[:, :3]
# Create a DataFrame for the first three principal components
pca_df = pd.DataFrame(data=X_pca_first_three, columns=['PC1', 'PC2', 'PC3'])

# Add the 'diagnosis' column from your original DataFrame for labels
pca_df['diagnosis'] = df['diagnosis']

# Define unique labels (e.g., 'M' and 'B' for malignant and benign)
unique_labels = pca_df['diagnosis'].unique()

# Create a 3D scatter plot with labeled points
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

for label in unique_labels:
    data = pca_df[pca_df['diagnosis'] == label]
    ax.scatter(data['PC1'], data['PC2'], data['PC3'], label=label)

ax.set_title('3D PCA Score Plot with Labeled Observations (First Three Principal Components)')
ax.set_xlabel('Principal Component 1 (PC1)')
ax.set_ylabel('Principal Component 2 (PC2)')
ax.set_zlabel('Principal Component 3 (PC3)')
ax.legend()
plt.show()




##LIT
# Impute missing values
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(LIT)

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)

# Perform PCA
pca = PCA()
X_pca_tracts_LIT = pca.fit_transform(X_scaled)

# Calculate explained variance
explained_variance = pca.explained_variance_ratio_
cumulative_variance = np.cumsum(explained_variance)

# Create a Scree plot with colored points
plt.figure(figsize=(8, 6))
plt.plot(range(1, len(cumulative_variance) + 1), cumulative_variance, marker='o', linestyle='--')
plt.title('Scree Plot')
plt.xlabel('Number of Components')
plt.ylabel('Explained Variance')
plt.grid()
plt.legend()
plt.show()

# Assuming you have performed PCA and obtained 50 principal components
# X_pca is a 2D array with the principal components

# Select the first two principal components (PC1 and PC2)
X_pca_first_two = X_pca_tracts_LIT[:, :2]
# Create a DataFrame for the first two principal components
pca_df = pd.DataFrame(data=X_pca_first_two, columns=['PC1', 'PC2'])
# Add the 'diagnosis' column from your original DataFrame for labels
pca_df['diagnosis'] = df['diagnosis']

# Define unique labels (e.g., 'M' and 'B' for malignant and benign)
unique_labels = pca_df['diagnosis'].unique()

# Create a scatter plot with labeled points
plt.figure(figsize=(10, 6))

for label in unique_labels:
    data = pca_df[pca_df['diagnosis'] == label]
    plt.scatter(data['PC1'], data['PC2'], label=label)

plt.title('PCA Score Plot based on NDI in lesion independent tracts')
plt.xlabel('Principal Component 1 (PC1)')
plt.ylabel('Principal Component 2 (PC2)')
plt.legend()
plt.grid()
plt.show()

# Assuming you have performed PCA and obtained 3 principal components
# X_pca_first_three is a 2D array with the first three principal components
X_pca_first_three = X_pca_tracts_LIT[:, :3]
# Create a DataFrame for the first three principal components
pca_df = pd.DataFrame(data=X_pca_first_three, columns=['PC1', 'PC2', 'PC3'])

# Add the 'diagnosis' column from your original DataFrame for labels
pca_df['diagnosis'] = df['diagnosis']

# Define unique labels (e.g., 'M' and 'B' for malignant and benign)
unique_labels = pca_df['diagnosis'].unique()

# Create a 3D scatter plot with labeled points
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

for label in unique_labels:
    data = pca_df[pca_df['diagnosis'] == label]
    ax.scatter(data['PC1'], data['PC2'], data['PC3'], label=label)

ax.set_title('3D PCA Score Plot based on NDI in lesion independent tracts (First Three Principal Components)')
ax.set_xlabel('Principal Component 1 (PC1)')
ax.set_ylabel('Principal Component 2 (PC2)')
ax.set_zlabel('Principal Component 3 (PC3)')
ax.legend()
plt.show()









##NOW the cortex

# Impute missing values
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(cortex)

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)

# Perform PCA
pca = PCA()
X_pca_cortex = pca.fit_transform(X_scaled)

# Calculate explained variance
explained_variance = pca.explained_variance_ratio_
cumulative_variance = np.cumsum(explained_variance)

# Create a Scree plot with colored points
plt.figure(figsize=(8, 6))
plt.plot(range(1, len(cumulative_variance) + 1), cumulative_variance, marker='o', linestyle='--')
plt.title('Scree Plot')
plt.xlabel('Number of Components')
plt.ylabel('Explained Variance')
plt.grid()
plt.legend()
plt.show()

# Assuming you have performed PCA and obtained 50 principal components
# X_pca is a 2D array with the principal components

# Select the first two principal components (PC1 and PC2)
X_pca_first_two = X_pca_cortex[:, :2]
# Create a DataFrame for the first two principal components
pca_df = pd.DataFrame(data=X_pca_first_two, columns=['PC1', 'PC2'])
# Add the 'diagnosis' column from your original DataFrame for labels
pca_df['diagnosis'] = df['diagnosis']

# Define unique labels (e.g., 'M' and 'B' for malignant and benign)
unique_labels = pca_df['diagnosis'].unique()

# Create a scatter plot with labeled points
plt.figure(figsize=(10, 6))

for label in unique_labels:
    data = pca_df[pca_df['diagnosis'] == label]
    plt.scatter(data['PC1'], data['PC2'], label=label)

plt.title('PCA Score Plot based on R1 in cortical ROIs')
plt.xlabel('Principal Component 1 (PC1)')
plt.ylabel('Principal Component 2 (PC2)')
plt.legend()
plt.grid()
plt.show()

# Assuming you have performed PCA and obtained 3 principal components
# X_pca_first_three is a 2D array with the first three principal components
X_pca_first_three = X_pca_cortex[:, :3]
# Create a DataFrame for the first three principal components
pca_df = pd.DataFrame(data=X_pca_first_three, columns=['PC1', 'PC2', 'PC3'])

# Add the 'diagnosis' column from your original DataFrame for labels
pca_df['diagnosis'] = df['diagnosis']

# Define unique labels (e.g., 'M' and 'B' for malignant and benign)
unique_labels = pca_df['diagnosis'].unique()

# Create a 3D scatter plot with labeled points
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

for label in unique_labels:
    data = pca_df[pca_df['diagnosis'] == label]
    ax.scatter(data['PC1'], data['PC2'], data['PC3'], label=label)

ax.set_title('3D PCA Score Plot based on R1 in cortical ROIs (First Three Principal Components)')
ax.set_xlabel('Principal Component 1 (PC1)')
ax.set_ylabel('Principal Component 2 (PC2)')
ax.set_zlabel('Principal Component 3 (PC3)')
ax.legend()
plt.show()


####Correlation of two first PC's from white matter tracts NDI and cortical ROI's R1 (myelin)
# Select the first principal components (PC1)
X_pca_cortex_1PC = X_pca_cortex[:, :1]
X_pca_tracts_LIT_1PC = X_pca_tracts_LIT[:, :1]
X_pca_tracts_LD_1PC = X_pca_tracts_LD[:, :1]


# Create DataFrames for each PC
cortex_df = pd.DataFrame(data=X_pca_cortex_1PC, columns=['Cortex_PC1'])
tracts_LIT_df = pd.DataFrame(data=X_pca_tracts_LIT_1PC, columns=['Tracts_LIT_PC1'])
tracts_LD_df = pd.DataFrame(data=X_pca_tracts_LD_1PC, columns=['Tracts_LD_PC1'])


# Combine them into one DataFrame
combined_df = pd.concat([cortex_df, tracts_LIT_df, tracts_LD_df], axis=1)# Create a DataFrame for the first two principal components

# Add the 'diagnosis' column from your original DataFrame for labels
combined_df['diagnosis'] = df['diagnosis']
# Add the 'lesion_load' column from your original DataFrame for labels
combined_df['lesion_load'] = df['lesion_load_norm']
# Assuming you have already created and organized the 'combined_df' DataFrame

# List of unique groups (diagnoses)
unique_groups = combined_df['diagnosis'].unique()

# Dictionary to store correlation results
correlation_results = {}

# Perform correlation analysis for each group
for group in unique_groups:
    # Subset the data for the specific group
    group_data = combined_df[combined_df['diagnosis'] == group].reset_index(drop=True)
    
    # Calculate the correlation and p-value between 'Cortex_PC1' and 'Tracts_PC1' columns
    correlation_coefficient, p_value = pearsonr(group_data['Cortex_PC1'], group_data['Tracts_LIT_PC1'])
    
    # Store the result in the dictionary
    correlation_results[group] = (correlation_coefficient, p_value)

# Print or analyze the correlation results
for group, (correlation, p_value) in correlation_results.items():
    print(f'Correlation between PC1 cortex and PC1 tracts LIT for group "{group}": {correlation:.2f}, p-value: {p_value:.4f}')





#Correlation of LIT tracts NDI 1 PC with lesion load as a way to cut it out

# Dictionary to store correlation results
correlation_results = {}

# Perform correlation analysis for each group
for group in unique_groups:
    # Subset the data for the specific group
    group_data = combined_df[combined_df['diagnosis'] == group].reset_index(drop=True)
    
    # Calculate the correlation and p-value between 'Cortex_PC1' and 'Tracts_PC1' columns
    correlation_coefficient, p_value = stats.spearmanr(group_data['Tracts_LIT_PC1'], group_data['lesion_load'],nan_policy="omit")
    
    # Store the result in the dictionary
    correlation_results[group] = (correlation_coefficient, p_value)

# Print or analyze the correlation results
for group, (correlation, p_value) in correlation_results.items():
    print(f'Correlations between PC1 LIT and lesion load for group "{group}": {correlation:.2f}, p-value: {p_value:.4f}')






#Correlation of LD tracts NDI 1 PC with lesion load as a way to cut it out

# Dictionary to store correlation results
correlation_results = {}

# Perform correlation analysis for each group
for group in ['NMOSD','RRMS']:
    # Subset the data for the specific group
    group_data = combined_df[combined_df['diagnosis'] == group].reset_index(drop=True)
    
    # Calculate the correlation and p-value between 'Cortex_PC1' and 'Tracts_PC1' columns
    correlation_coefficient, p_value = stats.spearmanr(group_data['Tracts_LD_PC1'], group_data['lesion_load'],nan_policy="omit")
    
    # Store the result in the dictionary
    correlation_results[group] = (correlation_coefficient, p_value)

# Print or analyze the correlation results
for group, (correlation, p_value) in correlation_results.items():
    print(f'Correlations between PC1 LD and lesion load for group "{group}": {correlation:.2f}, p-value: {p_value:.4f}')
