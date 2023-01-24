#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 11:07:54 2023

@author: paweljakuszyk
"""
import numpy as np
import pandas as pd

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
         
#write the tracts that have values of 0 
with open("/Volumes/pjakuszyk/seropositive_project/SM_patients_affceted_tracts.txt", "w") as f:
    for SM_patient in SM_patients:
        df = pd.read_csv(f"/Volumes/pjakuszyk/seropositive_project/participants/{SM_patient}/Brain/DWI/tractseg_output/Tractometry_NAWM_NODDI_ND.csv", sep=';')
        zero_columns = df.columns[(df == 0).any()].tolist()
        print(f"{SM_patient}'s tracts with values of zero (fully traversing throught WM hyperintensities): {zero_columns}")
        f.write(f"{SM_patient}'s tracts with values of zero (fully traversing throught WM hyperintensities): {zero_columns}\n")
        
        
#find the mean value per tract segment for the group 

df_list_MS = []

for SM_patient in SM_patients:
    df_list_MS.append(pd.read_csv(f"/Volumes/pjakuszyk/seropositive_project/participants/{SM_patient}/Brain/DWI/tractseg_output/Tractometry_NAWM_NODDI_ND.csv", sep=';'))

df_concat_MS = pd.concat(df_list_MS)
mean_values_MS = df_concat_MS.replace(0, np.nan).groupby(df_concat_MS.index).mean()

for SM_patient in SM_patients:
    df = pd.read_csv(f"/Volumes/pjakuszyk/seropositive_project/participants/{SM_patient}/Brain/DWI/tractseg_output/Tractometry_NAWM_NODDI_ND.csv", sep=';')
    df.replace(0,np.nan,inplace=True)
    df.fillna(mean_values_MS,inplace=True)
    df.to_csv(f"/Volumes/pjakuszyk/seropositive_project/participants/{SM_patient}/Brain/DWI/tractseg_output/Tractometry_NAWM_NODDI_ND_substituted.csv", sep=';')
    
NMOSD_patients =[
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

#write the tracts that have values of 0 
with open("/Volumes/pjakuszyk/seropositive_project/NMOSD_patients_affceted_tracts.txt", "w") as f:
    for NMOSD_patient in NMOSD_patients:
        df = pd.read_csv(f"/Volumes/pjakuszyk/seropositive_project/participants/{NMOSD_patient}/Brain/DWI/tractseg_output/Tractometry_NAWM_NODDI_ND.csv", sep=';')
        zero_columns = df.columns[(df == 0).any()].tolist()
        print(f"{NMOSD_patient}'s tracts with values of zero (fully traversing throught WM hyperintensities): {zero_columns}")
        f.write(f"{NMOSD_patient}'s tracts with values of zero (fully traversing throught WM hyperintensities): {zero_columns}\n")
        
        
#find the mean value per tract segment for the group 

df_list_NMOSD = []
for NMOSD_patient in NMOSD_patients:
    df_list_NMOSD.append(pd.read_csv(f"/Volumes/pjakuszyk/seropositive_project/participants/{NMOSD_patient}/Brain/DWI/tractseg_output/Tractometry_NAWM_NODDI_ND.csv", sep=';'))

df_concat_NMOSD = pd.concat(df_list_NMOSD)
mean_values_NMOSD = df_concat_NMOSD.replace(0, np.nan).groupby(df_concat_NMOSD.index).mean()

for NMOSD_patient in NMOSD_patients:
    df = pd.read_csv(f"/Volumes/pjakuszyk/seropositive_project/participants/{NMOSD_patient}/Brain/DWI/tractseg_output/Tractometry_NAWM_NODDI_ND.csv", sep=';')
    df.replace(0,np.nan,inplace=True)
    df.fillna(mean_values_NMOSD,inplace=True)
    df.to_csv(f"/Volumes/pjakuszyk/seropositive_project/participants/{NMOSD_patient}/Brain/DWI/tractseg_output/Tractometry_NAWM_NODDI_ND_substituted.csv", sep=';')
    
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

for control in HC:
    df = pd.read_csv(f"/Volumes/pjakuszyk/seropositive_project/participants/{control}/Brain/DWI/tractseg_output/Tractometry_NAWM_NODDI_ND.csv", sep=';')
    df.to_csv(f"/Volumes/pjakuszyk/seropositive_project/participants/{control}/Brain/DWI/tractseg_output/Tractometry_NAWM_NODDI_ND_substituted.csv", sep=';')
    


    