#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 13:43:59 2023

@author: paweljakuszyk
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import scipy.stats as stats
import statsmodels.stats.multitest as smm


#read in the data
df = pd.read_csv("/Volumes/ms/PJ_gRatio/Stata/data_ready.csv", sep=',')

# subset the dataframe based on the value in the 'group' column
group_MS = df[df['diagnosis'] == 'RRMS'].reset_index()
group_NMOSD = df[df['diagnosis'] == 'NMOSD'].reset_index()
group_HC = df[df['diagnosis'] == 'HC'].reset_index()

####MS######
#subset data for correlation
MS_LIT = group_MS.loc[:,'lit_af_left':'lit_uf_right']

MS_cortex = group_MS.loc[:,'lh_unknown':'rh_s_temporal_transverse']

##Correlations
###LIT
# Calculate the Spearman correlation and its p-value
# Create an empty DataFrame to store correlations
corelation_columns = pd.DataFrame(columns=['Comparison','Variable 1', 'Variable 2', 'Rho', 'P-Value'])

# Loop through each NDI variable in your DataFrame
for tract in MS_LIT:  # Skip the first column (lesion load)
    for cortex in MS_cortex:
        rho, p_value = stats.spearmanr(MS_cortex[cortex], MS_LIT[tract], nan_policy='omit')
    
        # Append the results to the correlation_df
        corelation_columns = pd.concat([corelation_columns, pd.DataFrame({'Comparison': ['cortex_ROI-tract_correlation'],
                                                              'Variable 1': [cortex], 
                                                              'Variable 2': [tract], 
                                                              'Rho': [rho], 
                                                              'P-Value': [p_value]})], 
                               ignore_index=True)


# Now, correlation_df contains the pairwise Spearman correlations
# between 'lesion_load' and each of the NDI variables

# Reset the index for the final result
corelation_columns.reset_index(drop=True, inplace=True)


#correct for multiple tests
# Correct for multiple comparisons using the FDR procedure and save results to PDF
p_vals_corr = smm.multipletests(corelation_columns['P-Value'], alpha=0.05, method='fdr_bh')[1]
#p_vals_corr = smm.multipletests(corr_df['P-Value'], alpha=0.05, method='bonferroni')[1]

corelation_columns['Corrected P-value'] = p_vals_corr

# Add asterisks to significant results
corelation_columns['Significance'] = ''
corelation_columns.loc[corelation_columns['Corrected P-value'] < 0.001, 'Significance'] = '***'
corelation_columns.loc[(corelation_columns['Corrected P-value'] >= 0.001) & (corelation_columns['Corrected P-value'] < 0.01), 'Significance'] = '**'
corelation_columns.loc[(corelation_columns['Corrected P-value'] >= 0.01) & (corelation_columns['Corrected P-value'] < 0.05), 'Significance'] = '*'


corelation_columns.to_csv('/Volumes/ms/seropositive_project/csv/Correlations_MS_cortex_roi_tracts_NDI.csv', index=False)

# Set the threshold 'x'
x = 0.05

# Select a subset of rows where 'column_name' is less than 'x'
subset_corr = corelation_columns[corelation_columns['P-Value'] < x]
# Alternatively check only significant negative correlations
subset_corr = corelation_columns[(corelation_columns['P-Value'] < x) & (corelation_columns['Rho'] > 0)]


###Graph analysis of significant correlations between cortex rois and ndi in tracts
G = nx.Graph()

G1 = nx.Graph()
G2 = nx.Graph()
# Add nodes from 'var1' and 'var2' columns
G1.add_nodes_from(subset_corr['Variable 1'])
G2.add_nodes_from(subset_corr['Variable 2'])

G.add_nodes_from(subset_corr['Variable 1'])
G.add_nodes_from(subset_corr['Variable 2'])

# Iterate through the DataFrame to add edges with 'rho' as the edge weight
for _, row in subset_corr.iterrows():
    G.add_edge(row['Variable 1'], row['Variable 2'], weight=row['Rho'])

#####calculates the degree of each node
node_degrees = nx.degree(G)

#####creates list of nodes and a list their degrees that will be used later for their sizes
nodelist, node_sizes = zip(*node_degrees())

pos_out=nx.circular_layout(G1)
pos_in=nx.circular_layout(G2)

pos_in_small = {key: tuple(value * 1 for value in values) for key, values in pos_in.items()}
pos_out_spread  = {key: tuple(value * 2 for value in values) for key, values in pos_out.items()}

# Combine dictionaries using the ** unpacking operator
pos = {**pos_out_spread, **pos_in}

#labels = nx.get_edge_attributes(G, 'weight')
edges,weights = zip(*nx.get_edge_attributes(G,'weight').items())
edge_labels = nx.get_edge_attributes(G, 'weight')

#draws nodes
nx.draw_networkx_nodes(G,pos,node_color='#DA70D6',
                           node_size=tuple([x**3 for x in node_sizes]),alpha=0.6)
    
#Styling for labels
nx.draw_networkx_labels(G, pos, font_size=9, 
                        font_family='Arial',font_weight='normal')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=5, font_family='Arial', font_color='black', font_weight='normal')


#draws the edges
nx.draw_networkx_edges(G, pos, edgelist=edges,style='solid', width=weights, edge_color = weights,
                      edge_vmin = min(weights), edge_vmax=max(weights))


#nx.draw(G, pos, with_labels=False, node_size=500, node_color='skyblue')
plt.show()







###############NMOSD#########################



#subset data for correlation
NMOSD_LIT = group_NMOSD.loc[:,'raw_af_left':'raw_uf_right']

NMOSD_cortex = group_NMOSD.loc[:,'lh_unknown':'rh_s_temporal_transverse']

##Correlations
###LIT
# Calculate the Spearman correlation and its p-value
# Create an empty DataFrame to store correlations
corelation_columns = pd.DataFrame(columns=['Comparison','Variable 1', 'Variable 2', 'Rho', 'P-Value'])

# Loop through each NDI variable in your DataFrame
for tract in NMOSD_LIT:  # Skip the first column (lesion load)
    for cortex in NMOSD_cortex:
        rho, p_value = stats.spearmanr(NMOSD_cortex[cortex], NMOSD_LIT[tract], nan_policy='omit')
    
        # Append the results to the correlation_df
        corelation_columns = pd.concat([corelation_columns, pd.DataFrame({'Comparison': ['cortex_ROI-tract_correlation'],
                                                              'Variable 1': [cortex], 
                                                              'Variable 2': [tract], 
                                                              'Rho': [rho], 
                                                              'P-Value': [p_value]})], 
                               ignore_index=True)


# Now, correlation_df contains the pairwise Spearman correlations
# between 'lesion_load' and each of the NDI variables

# Reset the index for the final result
corelation_columns.reset_index(drop=True, inplace=True)


#correct for multiple tests
# Correct for multiple comparisons using the FDR procedure and save results to PDF
p_vals_corr = smm.multipletests(corelation_columns['P-Value'], alpha=0.05, method='fdr_bh')[1]
#p_vals_corr = smm.multipletests(corr_df['P-Value'], alpha=0.05, method='bonferroni')[1]

corelation_columns['Corrected P-value'] = p_vals_corr

# Add asterisks to significant results
corelation_columns['Significance'] = ''
corelation_columns.loc[corelation_columns['Corrected P-value'] < 0.001, 'Significance'] = '***'
corelation_columns.loc[(corelation_columns['Corrected P-value'] >= 0.001) & (corelation_columns['Corrected P-value'] < 0.01), 'Significance'] = '**'
corelation_columns.loc[(corelation_columns['Corrected P-value'] >= 0.01) & (corelation_columns['Corrected P-value'] < 0.05), 'Significance'] = '*'


corelation_columns.to_csv('/Volumes/ms/seropositive_project/csv/Correlations_NMOSD_cortex_roi_tracts_NDI.csv', index=False)

# Set the threshold 'x'
x = 0.05

# Select a subset of rows where 'column_name' is less than 'x'
subset_corr = corelation_columns[corelation_columns['P-Value'] < x]
# Alternatively check only significant negative correlations
subset_corr = corelation_columns[(corelation_columns['P-Value'] < x) & (corelation_columns['Rho'] < 0)]


###Graph analysis of significant correlations between cortex rois and ndi in tracts
G = nx.Graph()

G1 = nx.Graph()
G2 = nx.Graph()
# Add nodes from 'var1' and 'var2' columns
G1.add_nodes_from(subset_corr['Variable 1'])
G2.add_nodes_from(subset_corr['Variable 2'])

G.add_nodes_from(subset_corr['Variable 1'])
G.add_nodes_from(subset_corr['Variable 2'])

# Iterate through the DataFrame to add edges with 'rho' as the edge weight
for _, row in subset_corr.iterrows():
    G.add_edge(row['Variable 1'], row['Variable 2'], weight=row['Rho'])

#####calculates the degree of each node
node_degrees = nx.degree(G)

#####creates list of nodes and a list their degrees that will be used later for their sizes
nodelist, node_sizes = zip(*node_degrees())

pos_out=nx.circular_layout(G1)
pos_in=nx.circular_layout(G2)

pos_in_small = {key: tuple(value * 1 for value in values) for key, values in pos_in.items()}
pos_out_spread  = {key: tuple(value * 2 for value in values) for key, values in pos_out.items()}

# Combine dictionaries using the ** unpacking operator
pos = {**pos_out_spread, **pos_in}

#labels = nx.get_edge_attributes(G, 'weight')
edges,weights = zip(*nx.get_edge_attributes(G,'weight').items())
edge_labels = nx.get_edge_attributes(G, 'weight')

#draws nodes
nx.draw_networkx_nodes(G,pos,node_color='#DA70D6',
                           node_size=tuple([x**3 for x in node_sizes]),alpha=0.6)
    
#Styling for labels
nx.draw_networkx_labels(G, pos, font_size=9, 
                        font_family='Arial',font_weight='normal')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=5, font_family='Arial', font_color='black', font_weight='normal')


#draws the edges
nx.draw_networkx_edges(G, pos, edgelist=edges,style='solid', width=weights, edge_color = weights,
                      edge_vmin = min(weights), edge_vmax=max(weights))


#nx.draw(G, pos, with_labels=False, node_size=500, node_color='skyblue')
plt.show()














###############HC#########################



#subset data for correlation
HC_LIT = group_HC.loc[:,'lit_af_left':'lit_uf_right']

HC_cortex = group_HC.loc[:,'lh_unknown':'rh_s_temporal_transverse']

##Correlations
###LIT
# Calculate the Spearman correlation and its p-value
# Create an empty DataFrame to store correlations
corelation_columns = pd.DataFrame(columns=['Comparison','Variable 1', 'Variable 2', 'Rho', 'P-Value'])

# Loop through each NDI variable in your DataFrame
for tract in HC_LIT:  # Skip the first column (lesion load)
    for cortex in HC_cortex:
        rho, p_value = stats.spearmanr(HC_cortex[cortex], HC_LIT[tract], nan_policy='omit')
    
        # Append the results to the correlation_df
        corelation_columns = pd.concat([corelation_columns, pd.DataFrame({'Comparison': ['cortex_ROI-tract_correlation'],
                                                              'Variable 1': [cortex], 
                                                              'Variable 2': [tract], 
                                                              'Rho': [rho], 
                                                              'P-Value': [p_value]})], 
                               ignore_index=True)


# Now, correlation_df contains the pairwise Spearman correlations
# between 'lesion_load' and each of the NDI variables

# Reset the index for the final result
corelation_columns.reset_index(drop=True, inplace=True)


#correct for multiple tests
# Correct for multiple comparisons using the FDR procedure and save results to PDF
p_vals_corr = smm.multipletests(corelation_columns['P-Value'], alpha=0.05, method='fdr_bh')[1]
#p_vals_corr = smm.multipletests(corr_df['P-Value'], alpha=0.05, method='bonferroni')[1]

corelation_columns['Corrected P-value'] = p_vals_corr

# Add asterisks to significant results
corelation_columns['Significance'] = ''
corelation_columns.loc[corelation_columns['Corrected P-value'] < 0.001, 'Significance'] = '***'
corelation_columns.loc[(corelation_columns['Corrected P-value'] >= 0.001) & (corelation_columns['Corrected P-value'] < 0.01), 'Significance'] = '**'
corelation_columns.loc[(corelation_columns['Corrected P-value'] >= 0.01) & (corelation_columns['Corrected P-value'] < 0.05), 'Significance'] = '*'


corelation_columns.to_csv('/Volumes/ms/seropositive_project/csv/Correlations_HC_cortex_roi_tracts_NDI.csv', index=False)

# Set the threshold 'x'
x = 0.05

# Select a subset of rows where 'column_name' is less than 'x'
#subset_corr = corelation_columns[corelation_columns['Corrected P-value'] < x]
# Alternatively check only significant negative correlations
subset_corr = corelation_columns[(corelation_columns['Corrected P-value'] < x) & (corelation_columns['Rho'] < 0)]
##no significant positive correlations in HC group

###Graph analysis of significant correlations between cortex rois and ndi in tracts
G = nx.Graph()

G1 = nx.Graph()
G2 = nx.Graph()
# Add nodes from 'var1' and 'var2' columns
G1.add_nodes_from(subset_corr['Variable 1'])
G2.add_nodes_from(subset_corr['Variable 2'])

G.add_nodes_from(subset_corr['Variable 1'])
G.add_nodes_from(subset_corr['Variable 2'])

# Iterate through the DataFrame to add edges with 'rho' as the edge weight
for _, row in subset_corr.iterrows():
    G.add_edge(row['Variable 1'], row['Variable 2'], weight=row['Rho'])

#####calculates the degree of each node
node_degrees = nx.degree(G)

#####creates list of nodes and a list their degrees that will be used later for their sizes
nodelist, node_sizes = zip(*node_degrees())

pos_out=nx.circular_layout(G1)
pos_in=nx.circular_layout(G2)

pos_in_small = {key: tuple(value * 1 for value in values) for key, values in pos_in.items()}
pos_out_spread  = {key: tuple(value * 2 for value in values) for key, values in pos_out.items()}

# Combine dictionaries using the ** unpacking operator
pos = {**pos_out_spread, **pos_in}

#labels = nx.get_edge_attributes(G, 'weight')
edges,weights = zip(*nx.get_edge_attributes(G,'weight').items())
edge_labels = nx.get_edge_attributes(G, 'weight')

#draws nodes
nx.draw_networkx_nodes(G,pos,node_color='#DA70D6',
                           node_size=tuple([x**3 for x in node_sizes]),alpha=0.6)
    
#Styling for labels
nx.draw_networkx_labels(G, pos, font_size=9, 
                        font_family='Arial',font_weight='normal')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=5, font_family='Arial', font_color='black', font_weight='normal')


#draws the edges
nx.draw_networkx_edges(G, pos, edgelist=edges,style='solid', width=weights, edge_color = weights,
                      edge_vmin = min(weights), edge_vmax=max(weights))


#nx.draw(G, pos, with_labels=False, node_size=500, node_color='skyblue')
plt.show()







