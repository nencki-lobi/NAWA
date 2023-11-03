#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import networkx as nx
import scipy.stats as stats
import statsmodels.stats.multitest as smm
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from scipy.stats import pearsonr
#import boto
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import scale 
from sklearn import model_selection
from sklearn.model_selection import RepeatedKFold
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import r2_score
from sklearn.model_selection import KFold
#specify colors for plotting
RRMS_color = (109/255, 176/255, 155/255)
NMOSD_color = (225/255, 145/255, 113/255)
HC_color = (150/255, 162/255, 195/255)
#for handling NaNs
imputer = SimpleImputer(strategy='mean')
# Dictionary to map diagnosis to colors
#diagnosis_colors = {'RRMS': RRMS_color, 'HC': HC_color,'NMOSD' : NMOSD_color}  # Customize colors as needed
path_to_write='/Volumes/ms/seropositive_project/figures'

#read in the data
df = pd.read_csv("/Volumes/ms/PJ_gRatio/Stata/data_ready.csv", sep=',')
#for corraltions
# subset the dataframe based on the value in the 'group' column
group_MS = df[df['diagnosis'] == 'RRMS'].reset_index()
group_NMOSD = df[df['diagnosis'] == 'NMOSD'].reset_index()

###Lesion_load_norm
NMOSD_LL = group_NMOSD.get(['lesion_load_norm'])
RRMS_LL = group_MS.get(['lesion_load_norm'])

#feature evaluation index
df_feature_names = df.loc[:,'lit_af_left':'lit_uf_right']

# Subset the DataFrame based on a column value
subset_HC = df.loc[df['diagnosis'] == 'HC', 'lit_af_left':'lit_uf_right']
subset_HC = pd.DataFrame(imputer.fit_transform(subset_HC))
subset_HC['diagnosis'] = 'HC'

subset_MS = df.loc[df['diagnosis'] == 'RRMS', 'lit_af_left':'lit_uf_right']
subset_MS = pd.DataFrame(imputer.fit_transform(subset_MS))
subset_MS['diagnosis'] = 'RRMS'

subset_NMO = df.loc[df['diagnosis'] == 'NMOSD', 'lit_af_left':'lit_uf_right']
subset_NMO = pd.DataFrame(imputer.fit_transform(subset_NMO))
subset_NMO['diagnosis'] = 'NMOSD'

df_parcel = pd.concat([subset_HC, subset_MS, subset_NMO], ignore_index=True)

first_column = df_parcel.pop('diagnosis')
df_parcel.insert(0, 'diagnosis', first_column)

df_MS_HC = df_parcel[df_parcel['diagnosis'].isin(['HC', 'RRMS'])].reset_index().drop(columns=['index'])

df_NMOSD_HC = df_parcel[df_parcel['diagnosis'].isin(['HC', 'NMOSD'])].reset_index().drop(columns=['index'])

df_NMOSD_MS = df_parcel[df_parcel['diagnosis'].isin(['RRMS', 'NMOSD'])].reset_index().drop(columns=['index'])

##for LD

subset_MS_LD = df.loc[df['diagnosis'] == 'RRMS', 'ld_af_left':'ld_uf_right']
subset_MS_LD = pd.DataFrame(imputer.fit_transform(subset_MS_LD))
subset_MS_LD['diagnosis'] = 'RRMS'

subset_NMO_LD = df.loc[df['diagnosis'] == 'NMOSD', 'ld_af_left':'ld_uf_right']
subset_NMO_LD = pd.DataFrame(imputer.fit_transform(subset_NMO_LD))
subset_NMO_LD['diagnosis'] = 'NMOSD'

df_parcel_LD = pd.concat([subset_NMO_LD, subset_MS_LD], ignore_index=True)

first_column = df_parcel_LD.pop('diagnosis')
df_parcel_LD.insert(0, 'diagnosis', first_column)

df_NMOSD_MS_LD = df_parcel_LD[df_parcel_LD['diagnosis'].isin(['RRMS', 'NMOSD'])].reset_index().drop(columns=['index'])
df_NMOSD_MS_LD = df_NMOSD_MS_LD.iloc[:, :-2]

##for RAW

subset_MS_RAW = df.loc[df['diagnosis'] == 'RRMS', 'raw_af_left':'raw_uf_right']
subset_MS_RAW = pd.DataFrame(imputer.fit_transform(subset_MS_RAW))
subset_MS_RAW['diagnosis'] = 'RRMS'

subset_NMO_RAW = df.loc[df['diagnosis'] == 'NMOSD', 'raw_af_left':'raw_uf_right']
subset_NMO_RAW = pd.DataFrame(imputer.fit_transform(subset_NMO_RAW))
subset_NMO_RAW['diagnosis'] = 'NMOSD'

df_parcel_RAW = pd.concat([subset_NMO_RAW, subset_MS_RAW], ignore_index=True)

first_column = df_parcel_RAW.pop('diagnosis')
df_parcel_RAW.insert(0, 'diagnosis', first_column)

df_NMOSD_MS_RAW = df_parcel_RAW[df_parcel_RAW['diagnosis'].isin(['RRMS', 'NMOSD'])].reset_index().drop(columns=['index'])


###OLS DA RRMS vs HC

# get dummies will dummy code your categorical variables (also called one-hot encoding)
data_dummified = pd.get_dummies(df_MS_HC)

# Split the dummified data into X and Y
# Split the dummified data into X and Y
Y = data_dummified[['diagnosis_HC', 'diagnosis_RRMS']]
X = data_dummified.loc[:,0:49]

# Instantiate a PLSR model
pls = PLSRegression(n_components=50)

# Fit the PLSR model to your data (X and Y)
pls.fit(X, Y)  # Replace X and Y with your data

# Calculate the explained variance for each component
explained_variance = np.cumsum(np.var(pls.x_scores_, axis=0) / np.sum(np.var(pls.x_scores_, axis=0)))

# Create a scree plot
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(explained_variance) + 1), explained_variance, marker='o', linestyle='-', color='b')
plt.title('Scree Plot for PLSR RRMS HC')
plt.xlabel('Number of Components')
plt.ylabel('Explained Variance')
plt.grid()
plt.show()

#define cross-validation method
cv = RepeatedKFold(n_splits=5, n_repeats=100, random_state=1)

mse = []
n = len(X)


# Calculate MSE using cross-validation, adding one component at a time
for i in np.arange(1, 50):
    pls = PLSRegression(n_components=i)
    score = -1*model_selection.cross_val_score(pls, scale(X), Y, cv=cv,
               scoring='neg_mean_squared_error').mean()
    mse.append(score)

#plot test MSE vs. number of components
plt.plot(mse)
plt.xlabel('Number of PLS Components')
plt.ylabel('MSE')
plt.title('RRMS vs HC MSE')


# fit the pls regression
my_plsr = PLSRegression(n_components=2, scale=True)
my_plsr.fit(X, Y)

# Get the R² (coefficient of determination)
r2 = my_plsr.score(X, Y)
print("R²:", r2)

# Define the number of cross-validation folds
n_splits = 5  # You can adjust the number of folds as needed

# Initialize a variable to store R² scores
r2_scores = []

# Create a KFold cross-validation object
kf = KFold(n_splits=n_splits, shuffle=True, random_state=1)

# Perform cross-validated OPLS-DA
for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]
    Y_train, Y_test = Y[train_index], Y[test_index]

    my_plsr.fit(X_train, Y_train)
    predicted_y = my_plsr.predict(X_test)

    r2 = r2_score(Y_test, predicted_y)
    r2_scores.append(r2)

# Calculate the mean R² score
mean_r2 = np.mean(r2_scores)


# hand made biplot alternative in Python

# extract scores (one score per individual per component)
scores_df = pd.DataFrame(my_plsr.x_scores_)

# standardize scores between -1 and 1 so they fit on the plot
std_scores_dim1 = 2 * ( (scores_df[0] - min(scores_df[0])) / (max(scores_df[0]) - min(scores_df[0])) ) -1
std_scores_dim2 = 2 * ( (scores_df[1] - min(scores_df[1])) / (max(scores_df[1]) - min(scores_df[1])) ) -1

#extract loadings (one loading per variable per component)
loadings_df = pd.DataFrame(my_plsr.x_loadings_)

# create the biplot by plotting each data point individualle (one by one)
plt.figure(figsize=(15, 15))
plt.xlim((-1.2,1.2))
plt.ylim((-1.2,1.2))

# Add vertical and horizontal axes lines
plt.axhline(0, color='black', linewidth=2)
plt.axvline(0, color='black', linewidth=2)

# Add a grid
plt.grid(True, linestyle='--', color='gray')

# Dictionary to map diagnosis to colors
diagnosis_colors = {'RRMS': RRMS_color, 'HC': HC_color}  # Customize colors as needed

for i in range(len(std_scores_dim1)):
    x = std_scores_dim1[i]
    y = std_scores_dim2[i]
    diagnosis = df_MS_HC.loc[i, 'diagnosis']

    # Add colored scatter points
    plt.scatter(x, y, color=diagnosis_colors.get(diagnosis, 'black'), s=100)  # Adjust the size 's' as needed

# Create a legend for diagnosis labels and colors
for diagnosis, color in diagnosis_colors.items():
    plt.scatter([], [], color=color, label=diagnosis)

legend = plt.legend(fontsize=15)  # Adjust the font size as needed

# Add X-axis and Y-axis labels
plt.xlabel('PC1')
plt.ylabel('PC2')

# Add a subtitle with R² value
# Add a subtitle with R² value, centered below the plot
subtitle = f"R²: {r2}"
text_x = (plt.xlim()[0] + plt.xlim()[1]) / 2  # Calculate the center of X-axis
text_y = plt.ylim()[0] - 0.3  # Adjust the Y position as needed

plt.text(text_x, text_y, subtitle, fontsize=12, color='black', ha='center')
plt.title("Partial Least Squares Discriminant Analysis in tracts not traversing through white matter lesions RRMS and HC")

# Save the plot as a PNG file with high DPI
plt.savefig(path_to_write + '/PLSDA_MS_HC', dpi=300)

plt.show()












###OLS DA RRMS vs NMOSD

# get dummies will dummy code your categorical variables (also called one-hot encoding)
data_dummified = pd.get_dummies(df_NMOSD_MS, dtype=bool)     

# Split the dummified data into X and Y
# Split the dummified data into X and Y
Y = data_dummified[['diagnosis_NMOSD', 'diagnosis_RRMS']]
X = data_dummified.loc[:,0:49]

# Instantiate a PLSR model
pls = PLSRegression(n_components=50)

# Fit the PLSR model to your data (X and Y)
pls.fit(X, Y)  # Replace X and Y with your data

# Calculate the explained variance for each component
explained_variance = np.cumsum(np.var(pls.x_scores_, axis=0) / np.sum(np.var(pls.x_scores_, axis=0)))

# Create a scree plot
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(explained_variance) + 1), explained_variance, marker='o', linestyle='-', color='b')
plt.title('Scree Plot for PLSR RRMS NMOSD')
plt.xlabel('Number of Components')
plt.ylabel('Explained Variance')
plt.grid()
plt.show()

#define cross-validation method
cv = RepeatedKFold(n_splits=5, n_repeats=3, random_state=1)

mse = []
n = len(X)

# Calculate MSE using cross-validation, adding one component at a time
for i in np.arange(1, 50):
    pls = PLSRegression(n_components=i)
    score = -1*model_selection.cross_val_score(pls, scale(X), Y, cv=cv,
               scoring='neg_mean_squared_error').mean()
    mse.append(score)

#plot test MSE vs. number of components
plt.plot(mse)
plt.xlabel('Number of PLS Components')
plt.ylabel('MSE')
plt.title('RRMS vs NMOSD MSE')


# fit the pls regression
my_plsr = PLSRegression(n_components=2, scale=True)
my_plsr.fit(X, Y)


# Get the R² (coefficient of determination)
r2 = my_plsr.score(X, Y)
print("R²:", r2)

# hand made biplot alternative in Python

# extract scores (one score per individual per component)
scores_df = pd.DataFrame(my_plsr.x_scores_)

# standardize scores between -1 and 1 so they fit on the plot
std_scores_dim1 = 2 * ( (scores_df[0] - min(scores_df[0])) / (max(scores_df[0]) - min(scores_df[0])) ) -1
std_scores_dim2 = 2 * ( (scores_df[1] - min(scores_df[1])) / (max(scores_df[1]) - min(scores_df[1])) ) -1

#extract loadings (one loading per variable per component)
loadings_df = pd.DataFrame(my_plsr.x_loadings_)

#perform correlation on 2 PCs and lesion load
df_corr = pd.merge(scores_df, Y, left_index=True, right_index=True)

df_corr_MS = df_corr[df_corr['diagnosis_RRMS']]
df_corr_NMO = df_corr[~df_corr['diagnosis_RRMS']]

#NMOSD
#correlation for PC1
rho, p_value = stats.spearmanr(NMOSD_LL, df_corr_NMO[0], nan_policy='omit')
# Print the result nicely
print(f"LIT NMOSD PC1 correlation with lesion load Spearman's rho: {rho:.3f} P-value: {p_value:.3f}")
#correlation fot PC2
rho, p_value = stats.spearmanr(NMOSD_LL, df_corr_NMO[1], nan_policy='omit')
# Print the result nicely
print(f"LIT NMOSD PC2 correlation with lesion load Spearman's rho: {rho:.3f} P-value: {p_value:.3f}")

##RRMS
#correlation for PC1
rho, p_value = stats.spearmanr(RRMS_LL, df_corr_MS[0], nan_policy='omit')
# Print the result nicely
print(f"LIT MS PC1 correlation with lesion load Spearman's rho: {rho:.3f} P-value: {p_value:.3f}")
#correlation fot PC2
rho, p_value = stats.spearmanr(RRMS_LL, df_corr_MS[1], nan_policy='omit')
# Print the result nicely
print(f"LIT MS PC2 correlation with lesion load Spearman's rho: {rho:.3f} P-value: {p_value:.3f}")


# Access the loadings for the first PLS component
loadings_component_1 = my_plsr.x_loadings_[:, 0]

# Find the indices of the variables with the highest absolute loadings
# For example, the top 5 variables
top_variable_indices = abs(loadings_component_1).argsort()[-10:][::-1]

# Access the variable names corresponding to the top indices
important_variables = df_feature_names.columns[top_variable_indices]

# create the biplot by plotting each data point individualle (one by one)
plt.figure(figsize=(15, 15))
plt.xlim((-1.2,1.2))
plt.ylim((-1.2,1.2))

# Add vertical and horizontal axes lines
plt.axhline(0, color='black', linewidth=2)
plt.axvline(0, color='black', linewidth=2)

# Add a grid
plt.grid(True, linestyle='--', color='gray')

# Dictionary to map diagnosis to colors
diagnosis_colors = {'RRMS': RRMS_color, 'NMOSD': NMOSD_color}  # Customize colors as needed

for i in range(len(std_scores_dim1)):
    x = std_scores_dim1[i]
    y = std_scores_dim2[i]
    diagnosis = df_NMOSD_MS.loc[i, 'diagnosis']

    # Add colored scatter points
    plt.scatter(x, y, color=diagnosis_colors.get(diagnosis, 'black'), s=100)  # Adjust the size 's' as needed

# Create a legend for diagnosis labels and colors
for diagnosis, color in diagnosis_colors.items():
    plt.scatter([], [], color=color, label=diagnosis)

legend = plt.legend(fontsize=15)  # Adjust the font size as needed

# Add X-axis and Y-axis labels
plt.xlabel('PC1')
plt.ylabel('PC2')

# Add a subtitle with R² value
# Add a subtitle with R² value, centered below the plot
subtitle = f"R²: {r2}"
text_x = (plt.xlim()[0] + plt.xlim()[1]) / 2  # Calculate the center of X-axis
text_y = plt.ylim()[0] - 0.3  # Adjust the Y position as needed

plt.text(text_x, text_y, subtitle, fontsize=12, color='black', ha='center')
plt.title("Partial Least Squares Discriminant Analysis  in tracts not traversing through white matter lesions in RRMS and NMOSD")

# Save the plot as a PNG file with high DPI
plt.savefig(path_to_write + '/PLSDA_MS_NMOSD', dpi=300)

plt.show()







###OLS DA HC vs NMOSD

# get dummies will dummy code your categorical variables (also called one-hot encoding)
data_dummified = pd.get_dummies(df_NMOSD_HC)

# Split the dummified data into X and Y
# Split the dummified data into X and Y
Y = data_dummified[['diagnosis_HC', 'diagnosis_NMOSD']]
X = data_dummified.loc[:,0:49]

# Instantiate a PLSR model
pls = PLSRegression(n_components=50)

# Fit the PLSR model to your data (X and Y)
pls.fit(X, Y)  # Replace X and Y with your data

# Calculate the explained variance for each component
explained_variance = np.cumsum(np.var(pls.x_scores_, axis=0) / np.sum(np.var(pls.x_scores_, axis=0)))

# Create a scree plot
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(explained_variance) + 1), explained_variance, marker='o', linestyle='-', color='b')
plt.title('Scree Plot for PLSR NMOSD HC')
plt.xlabel('Number of Components')
plt.ylabel('Explained Variance')
plt.grid()
plt.show()

#define cross-validation method
cv = RepeatedKFold(n_splits=5, n_repeats=3, random_state=1)

mse = []
n = len(X)

# Calculate MSE using cross-validation, adding one component at a time
for i in np.arange(1, 50):
    pls = PLSRegression(n_components=i)
    score = model_selection.cross_val_score(pls, scale(X), Y, cv=cv,
               scoring='neg_mean_squared_error').mean()
    mse.append(score)

#plot test MSE vs. number of components
plt.plot(mse)
plt.xlabel('Number of PLS Components')
plt.ylabel('MSE')
plt.title('RRMS vs HC MSE')

# fit the pls regression
my_plsr = PLSRegression(n_components=2, scale=True)
my_plsr.fit(X, Y)

# Get the R² (coefficient of determination)
r2 = my_plsr.score(X, Y)
print("R²:", r2)

# hand made biplot alternative in Python

# extract scores (one score per individual per component)
scores_df = pd.DataFrame(my_plsr.x_scores_)

# standardize scores between -1 and 1 so they fit on the plot
std_scores_dim1 = 2 * ( (scores_df[0] - min(scores_df[0])) / (max(scores_df[0]) - min(scores_df[0])) ) -1
std_scores_dim2 = 2 * ( (scores_df[1] - min(scores_df[1])) / (max(scores_df[1]) - min(scores_df[1])) ) -1

#extract loadings (one loading per variable per component)
loadings_df = pd.DataFrame(my_plsr.x_loadings_)

# create the biplot by plotting each data point individualle (one by one)
plt.figure(figsize=(15, 15))
plt.xlim((-1.2,1.2))
plt.ylim((-1.2,1.2))

# Add vertical and horizontal axes lines
plt.axhline(0, color='black', linewidth=2)
plt.axvline(0, color='black', linewidth=2)

# Add a grid
plt.grid(True, linestyle='--', color='gray')

# Dictionary to map diagnosis to colors
diagnosis_colors = {'HC': HC_color, 'NMOSD': NMOSD_color}  # Customize colors as needed

for i in range(len(std_scores_dim1)):
    x = std_scores_dim1[i]
    y = std_scores_dim2[i]
    diagnosis = df_NMOSD_HC.loc[i, 'diagnosis']

    # Add colored scatter points
    plt.scatter(x, y, color=diagnosis_colors.get(diagnosis, 'black'), s=100)  # Adjust the size 's' as needed

# Create a legend for diagnosis labels and colors
for diagnosis, color in diagnosis_colors.items():
    plt.scatter([], [], color=color, label=diagnosis)

legend = plt.legend(fontsize=15)  # Adjust the font size as needed

# Add X-axis and Y-axis labels
plt.xlabel('PC1')
plt.ylabel('PC2')

# Add a subtitle with R² value
# Add a subtitle with R² value, centered below the plot
subtitle = f"R²: {r2}"
text_x = (plt.xlim()[0] + plt.xlim()[1]) / 2  # Calculate the center of X-axis
text_y = plt.ylim()[0] - 0.3  # Adjust the Y position as needed

plt.text(text_x, text_y, subtitle, fontsize=12, color='black', ha='center')
plt.title("Partial Least Squares Discriminant Analysis in tracts not traversing through white matter lesions in NMOSD and HC")

# Save the plot as a PNG file with high DPI
plt.savefig(path_to_write + '/PLSDA_NMOSD_HC', dpi=300)

plt.show()

















###OLS DA RRMS vs NMOSD ###LD

# get dummies will dummy code your categorical variables (also called one-hot encoding)
data_dummified = pd.get_dummies(df_NMOSD_MS_LD, dtype=bool)     

# Split the dummified data into X and Y
# Split the dummified data into X and Y
Y = data_dummified[['diagnosis_NMOSD', 'diagnosis_RRMS']]
X = data_dummified.loc[:,0:47]

#define cross-validation method
cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)

mse = []
n = len(X)

# Calculate MSE using cross-validation, adding one component at a time
for i in np.arange(1, 6):
    pls = PLSRegression(n_components=i)
    score = -1*model_selection.cross_val_score(pls, scale(X), Y, cv=cv,
               scoring='neg_mean_squared_error').mean()
    mse.append(score)

#plot test MSE vs. number of components
plt.plot(mse)
plt.xlabel('Number of PLS Components')
plt.ylabel('MSE')
plt.title('RRMS vs NMOSD LD MSE')


# fit the pls regression
my_plsr = PLSRegression(n_components=2, scale=True)
my_plsr.fit(X, Y)

# Get the R² (coefficient of determination)
r2 = my_plsr.score(X, Y)
print("R²:", r2)

# hand made biplot alternative in Python

# extract scores (one score per individual per component)
scores_df = pd.DataFrame(my_plsr.x_scores_)

# standardize scores between -1 and 1 so they fit on the plot
std_scores_dim1 = 2 * ( (scores_df[0] - min(scores_df[0])) / (max(scores_df[0]) - min(scores_df[0])) ) -1
std_scores_dim2 = 2 * ( (scores_df[1] - min(scores_df[1])) / (max(scores_df[1]) - min(scores_df[1])) ) -1

#extract loadings (one loading per variable per component)
loadings_df = pd.DataFrame(my_plsr.x_loadings_)

#perform correlation on 2 PCs and lesion load
df_corr = pd.merge(scores_df, Y, left_index=True, right_index=True)

df_corr_MS = df_corr[df_corr['diagnosis_RRMS']]
df_corr_NMO = df_corr[~df_corr['diagnosis_RRMS']]

#NMOSD
#correlation for PC1
rho, p_value = stats.spearmanr(NMOSD_LL, df_corr_NMO[0], nan_policy='omit')
# Print the result nicely
print(f"LD NMOSD PC1 correlation with lesion load Spearman's rho: {rho:.3f} P-value: {p_value:.3f}")
#correlation fot PC2
rho, p_value = stats.spearmanr(NMOSD_LL, df_corr_NMO[1], nan_policy='omit')
# Print the result nicely
print(f"LD NMOSD PC2 correlation with lesion load Spearman's rho: {rho:.3f} P-value: {p_value:.3f}")

##RRMS
#correlation for PC1
rho, p_value = stats.spearmanr(RRMS_LL, df_corr_MS[0], nan_policy='omit')
# Print the result nicely
print(f"LD MS PC1 correlation with lesion load Spearman's rho: {rho:.3f} P-value: {p_value:.3f}")
#correlation fot PC2
rho, p_value = stats.spearmanr(RRMS_LL, df_corr_MS[1], nan_policy='omit')
# Print the result nicely
print(f"LD MS PC2 correlation with lesion load Spearman's rho: {rho:.3f} P-value: {p_value:.3f}")


# create the biplot by plotting each data point individualle (one by one)
plt.figure(figsize=(15, 15))
plt.xlim((-1.2,1.2))
plt.ylim((-1.2,1.2))

# Add vertical and horizontal axes lines
plt.axhline(0, color='black', linewidth=2)
plt.axvline(0, color='black', linewidth=2)

# Add a grid
plt.grid(True, linestyle='--', color='gray')

# Dictionary to map diagnosis to colors
diagnosis_colors = {'RRMS': RRMS_color, 'NMOSD': NMOSD_color}  # Customize colors as needed

for i in range(len(std_scores_dim1)):
    x = std_scores_dim1[i]
    y = std_scores_dim2[i]
    diagnosis = df_NMOSD_MS_LD.loc[i, 'diagnosis']

    # Add colored scatter points
    plt.scatter(x, y, color=diagnosis_colors.get(diagnosis, 'black'), s=100)  # Adjust the size 's' as needed

# Create a legend for diagnosis labels and colors
for diagnosis, color in diagnosis_colors.items():
    plt.scatter([], [], color=color, label=diagnosis)

legend = plt.legend(fontsize=15)  # Adjust the font size as needed

# Add X-axis and Y-axis labels
plt.xlabel('PC1')
plt.ylabel('PC2')

# Add a subtitle with R² value
# Add a subtitle with R² value, centered below the plot
subtitle = f"R²: {r2}"
text_x = (plt.xlim()[0] + plt.xlim()[1]) / 2  # Calculate the center of X-axis
text_y = plt.ylim()[0] - 0.3  # Adjust the Y position as needed

plt.text(text_x, text_y, subtitle, fontsize=12, color='black', ha='center')
plt.title("Partial Least Squares Discriminant Analysis in RRMS and NMOSD in lesion dependent tracts")

# Save the plot as a PNG file with high DPI
plt.savefig(path_to_write + '/PLSDA_MS_NMOSD_LD', dpi=300)

plt.show()










###OLS DA RRMS vs NMOSD ###RAW

# get dummies will dummy code your categorical variables (also called one-hot encoding)
data_dummified = pd.get_dummies(df_NMOSD_MS_RAW, dtype=bool)     

# Split the dummified data into X and Y
# Split the dummified data into X and Y
Y = data_dummified[['diagnosis_NMOSD', 'diagnosis_RRMS']]
X = data_dummified.loc[:,0:49]

#define cross-validation method
cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)

mse = []
n = len(X)

# Calculate MSE using cross-validation, adding one component at a time
for i in np.arange(1, 6):
    pls = PLSRegression(n_components=i)
    score = -1*model_selection.cross_val_score(pls, scale(X), Y, cv=cv,
               scoring='neg_mean_squared_error').mean()
    mse.append(score)

#plot test MSE vs. number of components
plt.plot(mse)
plt.xlabel('Number of PLS Components')
plt.ylabel('MSE')
plt.title('RRMS vs NMOSD RAW MSE')


# fit the pls regression
my_plsr = PLSRegression(n_components=2, scale=True)
my_plsr.fit(X, Y)

# Get the R² (coefficient of determination)
r2 = my_plsr.score(X, Y)
print("R²:", r2)

# hand made biplot alternative in Python

# extract scores (one score per individual per component)
scores_df = pd.DataFrame(my_plsr.x_scores_)

# standardize scores between -1 and 1 so they fit on the plot
std_scores_dim1 = 2 * ( (scores_df[0] - min(scores_df[0])) / (max(scores_df[0]) - min(scores_df[0])) ) -1
std_scores_dim2 = 2 * ( (scores_df[1] - min(scores_df[1])) / (max(scores_df[1]) - min(scores_df[1])) ) -1

#extract loadings (one loading per variable per component)
loadings_df = pd.DataFrame(my_plsr.x_loadings_)

#perform correlation on 2 PCs and lesion load
df_corr = pd.merge(scores_df, Y, left_index=True, right_index=True)

df_corr_MS = df_corr[df_corr['diagnosis_RRMS']]
df_corr_NMO = df_corr[~df_corr['diagnosis_RRMS']]

###NMOSD
#correlation for PC1
rho, p_value = stats.spearmanr(NMOSD_LL, df_corr_NMO[0], nan_policy='omit')
# Print the result nicely
print(f"RAW NMOSD PC1 correlation with lesion load Spearman's rho: {rho:.3f} P-value: {p_value:.3f}")
#correlation fot PC2
rho, p_value = stats.spearmanr(NMOSD_LL, df_corr_NMO[1], nan_policy='omit')
# Print the result nicely
print(f"RAW NMOSD PC2 correlation with lesion load Spearman's rho: {rho:.3f} P-value: {p_value:.3f}")

###RRMS
#correlation for PC1
rho, p_value = stats.spearmanr(RRMS_LL, df_corr_MS[0], nan_policy='omit')
# Print the result nicely
print(f"RAW MS PC1 correlation with lesion load Spearman's rho: {rho:.3f} P-value: {p_value:.3f}")
#correlation fot PC2
rho, p_value = stats.spearmanr(RRMS_LL, df_corr_MS[1], nan_policy='omit')
# Print the result nicely
print(f"RAW MS PC2 correlation with lesion load Spearman's rho: {rho:.3f} P-value: {p_value:.3f}")


# create the biplot by plotting each data point individualle (one by one)
plt.figure(figsize=(15, 15))
plt.xlim((-1.2,1.2))
plt.ylim((-1.2,1.2))

# Add vertical and horizontal axes lines
plt.axhline(0, color='black', linewidth=2)
plt.axvline(0, color='black', linewidth=2)

# Add a grid
plt.grid(True, linestyle='--', color='gray')

# Dictionary to map diagnosis to colors
diagnosis_colors = {'RRMS': RRMS_color, 'NMOSD': NMOSD_color}  # Customize colors as needed

for i in range(len(std_scores_dim1)):
    x = std_scores_dim1[i]
    y = std_scores_dim2[i]
    diagnosis = df_NMOSD_MS_RAW.loc[i, 'diagnosis']

    # Add colored scatter points
    plt.scatter(x, y, color=diagnosis_colors.get(diagnosis, 'black'), s=100)  # Adjust the size 's' as needed

# Create a legend for diagnosis labels and colors
for diagnosis, color in diagnosis_colors.items():
    plt.scatter([], [], color=color, label=diagnosis)

legend = plt.legend(fontsize=15)  # Adjust the font size as needed

# Add X-axis and Y-axis labels
plt.xlabel('PC1')
plt.ylabel('PC2')

# Add a subtitle with R² value
# Add a subtitle with R² value, centered below the plot
subtitle = f"R²: {r2}"
text_x = (plt.xlim()[0] + plt.xlim()[1]) / 2  # Calculate the center of X-axis
text_y = plt.ylim()[0] - 0.3  # Adjust the Y position as needed

plt.text(text_x, text_y, subtitle, fontsize=12, color='black', ha='center')
plt.title("Partial Least Squares Discriminant Analysis in RRMS and NMOSD in unsegmented tracts")

# Save the plot as a PNG file with high DPI
plt.savefig(path_to_write + '/PLSDA_MS_NMOSD_RAW', dpi=300)

plt.show()

