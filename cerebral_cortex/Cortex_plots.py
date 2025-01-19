#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 15:14:38 2023

@author: pawel
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import scipy.stats as stats
import ptitprince as pt

# Set float_format to display up to 3 decimal places
pd.options.display.float_format = '{:.3f}'.format

path_to_write='/Volumes/ms/seropositive_project/figures'

# Create the folder if it doesn't exist
if not os.path.exists(path_to_write):
    os.makedirs(path_to_write)

#read in the data
df = pd.read_csv("/Volumes/ms/PJ_gRatio/Stata/data_ready.csv", sep=',')

selected_columns = ['diagnosis', 'lh_gs_frontomargin', 'lh_gs_occipital_inf', 'lh_gs_paracentral', 'lh_gs_subcentral', 'lh_gs_transv_frontopol', 'lh_gs_cingulant', 
                    'lh_gs_cingulmidant', 'lh_gs_cingulmidpost', 'lh_g_cingulpostdorsal', 'lh_g_cingulpostventral', 'lh_g_cuneus', 'lh_g_front_infopercular', 
                    'lh_g_front_inforbital', 'lh_g_front_inftriangul', 'lh_g_front_middle', 'lh_g_front_sup', 'lh_g_ins_lgs_cent_ins', 'lh_g_insular_short', 
                    'lh_g_occipital_middle', 'lh_g_occipital_sup', 'lh_g_octemp_latfusifor', 'lh_g_octemp_medlingual', 'lh_g_octemp_medparahip', 'lh_g_orbital', 
                    'lh_g_pariet_infangular', 'lh_g_pariet_infsupramar', 'lh_g_parietal_sup', 'lh_g_postcentral', 'lh_g_precentral', 'lh_g_precuneus', 'lh_g_rectus',
                    'lh_g_subcallosal', 'lh_g_temp_supg_t_transv', 'lh_g_temp_suplateral', 'lh_g_temp_supplan_polar', 'lh_g_temp_supplan_tempo', 'lh_g_temporal_inf',
                    'lh_g_temporal_middle', 'lh_lat_fisanthorizont', 'lh_lat_fisantvertical', 'lh_lat_fispost', 'lh_pole_occipital', 'lh_pole_temporal', 'lh_s_calcarine',
                    'lh_s_central', 'lh_s_cingulmarginalis', 'lh_s_circular_insula_ant', 'lh_s_circular_insula_inf', 'lh_s_circular_insula_sup', 'lh_s_collat_transv_ant', 
                    'lh_s_collat_transv_post', 'lh_s_front_inf', 'lh_s_front_middle', 'lh_s_front_sup', 'lh_s_interm_primjensen', 'lh_s_intraparietp_trans', 
                    'lh_s_oc_middlelunatus', 'lh_s_oc_suptransversal', 'lh_s_occipital_ant', 'lh_s_octemp_lat', 'lh_s_octemp_medlingual', 'lh_s_orbital_lateral', 
                    'lh_s_orbital_medolfact', 'lh_s_orbitalh_shaped', 'lh_s_parieto_occipital', 'lh_s_pericallosal', 'lh_s_postcentral', 'lh_s_precentralinfpart', 
                    'lh_s_precentralsuppart', 'lh_s_suborbital', 'lh_s_subparietal', 'lh_s_temporal_inf', 'lh_s_temporal_sup', 'lh_s_temporal_transverse', 
                    'rh_gs_frontomargin', 'rh_gs_occipital_inf', 'rh_gs_paracentral', 'rh_gs_subcentral', 'rh_gs_transv_frontopol', 'rh_gs_cingulant', 'rh_gs_cingulmidant', 
                    'rh_gs_cingulmidpost', 'rh_g_cingulpostdorsal', 'rh_g_cingulpostventral', 'rh_g_cuneus', 'rh_g_front_infopercular', 'rh_g_front_inforbital', 
                    'rh_g_front_inftriangul', 'rh_g_front_middle', 'rh_g_front_sup', 'rh_g_ins_lgs_cent_ins', 'rh_g_insular_short', 'rh_g_occipital_middle', 
                    'rh_g_occipital_sup', 'rh_g_octemp_latfusifor', 'rh_g_octemp_medlingual', 'rh_g_octemp_medparahip', 'rh_g_orbital', 'rh_g_pariet_infangular', 
                    'rh_g_pariet_infsupramar', 'rh_g_parietal_sup', 'rh_g_postcentral', 'rh_g_precentral', 'rh_g_precuneus', 'rh_g_rectus', 'rh_g_subcallosal', 
                    'rh_g_temp_supg_t_transv', 'rh_g_temp_suplateral', 'rh_g_temp_supplan_polar', 'rh_g_temp_supplan_tempo', 'rh_g_temporal_inf', 'rh_g_temporal_middle', 
                    'rh_lat_fisanthorizont', 'rh_lat_fisantvertical', 'rh_lat_fispost', 'rh_pole_occipital', 'rh_pole_temporal', 'rh_s_calcarine', 'rh_s_central', 
                    'rh_s_cingulmarginalis', 'rh_s_circular_insula_ant', 'rh_s_circular_insula_inf', 'rh_s_circular_insula_sup', 'rh_s_collat_transv_ant', 
                    'rh_s_collat_transv_post', 'rh_s_front_inf', 'rh_s_front_middle', 'rh_s_front_sup', 'rh_s_interm_primjensen', 'rh_s_intraparietp_trans', 
                    'rh_s_oc_middlelunatus', 'rh_s_oc_suptransversal', 'rh_s_occipital_ant', 'rh_s_octemp_lat', 'rh_s_octemp_medlingual', 'rh_s_orbital_lateral', 
                    'rh_s_orbital_medolfact', 'rh_s_orbitalh_shaped', 'rh_s_parieto_occipital', 'rh_s_pericallosal', 'rh_s_postcentral', 'rh_s_precentralinfpart', 
                    'rh_s_precentralsuppart', 'rh_s_suborbital', 'rh_s_subparietal', 'rh_s_temporal_inf', 'rh_s_temporal_sup', 'rh_s_temporal_transverse']

subset_df = df[selected_columns]

group_order = ['HC', 'RRMS', 'NMOSD']
##################
###Plot for ON####
# Create a figure with a 7x3 subplot grid
fig, axs = plt.subplots(nrows=30, ncols=5, figsize=(30, 20))

# Flatten the axs array for easier indexing
axs = axs.flatten()

# Iterate over the tracts and plot a boxplot for each tract in each subplot
for i, tract in enumerate(subset_df.columns[1:]):
    
    # Create the boxplot
    pt.half_violinplot(data = subset_df, width = .6, palette="Set2", ax=axs[i],x='diagnosis', y=tract,)
    sns.stripplot(data = subset_df, palette="Set2", ax=axs[i],x='diagnosis', y=tract,)
    # plot the mean line
    sns.boxplot(showmeans=True,
                meanline=True,
                meanprops={'color': 'k', 'ls': '--', 'lw': 1.5},
                medianprops={'visible': False},
                whiskerprops={'visible': False},
                data=subset_df,
                showfliers=False,
                showbox=False,
                showcaps=False,
                ax=axs[i],x='diagnosis', y=tract)
        
    #add horizontal grid lines
    axs[i].yaxis.grid(True)    
    axs[i].set_title(tract)
    axs[i].set(ylabel='R1')

# Add a main title to the figure
fig.suptitle('R1 values in cortical parcellations')

# Adjust spacing between subplots
fig.tight_layout()

# Show the plot
plt.show()


import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates

# Subset the data to include only the tracts
tract_data = subset_df.drop('diagnosis', axis=1)

# Normalize the data for better visualization
normalized_data = (tract_data - tract_data.min()) / (tract_data.max() - tract_data.min())

# Add the diagnosis column back to the normalized data
normalized_data['diagnosis'] = subset_df['diagnosis']

# Create the parallel coordinates plot
plt.figure(figsize=(12, 8))
parallel_coordinates(normalized_data, 'diagnosis', colormap='Set2')

# Add a legend
plt.legend(title='Diagnosis')

# Add a title to the plot
plt.title('Parallel Coordinates Plot - R1 values in cortical parcellations')

# Show the plot
plt.show()

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget

# Create a subclass of QMainWindow to hold the plot
class ScrollablePlotWindow(QMainWindow):
    def __init__(self, fig):
        super().__init__()
        self.canvas = FigureCanvas(fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.setCentralWidget(QWidget(self))
        layout = QVBoxLayout(self.centralWidget())
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

# Create a figure with a 7x3 subplot grid
fig, axs = plt.subplots(nrows=30, ncols=5, figsize=(30, 20))

# Flatten the axs array for easier indexing
axs = axs.flatten()

# Iterate over the tracts and plot a boxplot for each tract in each subplot
for i, tract in enumerate(subset_df.columns[1:]):
    # Create the boxplot
    pt.half_violinplot(data=subset_df, width=.6, palette="Set2", ax=axs[i], x='diagnosis', y=tract,)
    sns.stripplot(data=subset_df, palette="Set2", ax=axs[i], x='diagnosis', y=tract,)
    # plot the mean line
    sns.boxplot(showmeans=True,
                meanline=True,
                meanprops={'color': 'k', 'ls': '--', 'lw': 1.5},
                medianprops={'visible': False},
                whiskerprops={'visible': False},
                data=subset_df,
                showfliers=False,
                showbox=False,
                showcaps=False,
                ax=axs[i], x='diagnosis', y=tract)

    # add horizontal grid lines
    axs[i].yaxis.grid(True)
    axs[i].set_title(tract)
    axs[i].set(ylabel='R1')

# Add a main title to the figure
fig.suptitle('R1 values in cortical parcellations')

# Adjust spacing between subplots
fig.tight_layout()

# Create the scrollable plot window
app = QApplication([])
scrollable_plot_window = ScrollablePlotWindow(fig)
scrollable_plot_window.show()

# Run the application event loop
app.exec_()



