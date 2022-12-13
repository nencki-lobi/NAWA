#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 10:08:58 2022
         _____                       _ _____            
        /  ___|                     | |  ___|           
        \ `--.  __ _ _ __ ___  _ __ | | |__             
         `--. \/ _` | '_ ` _ \| '_ \| |  __|            
        /\__/ / (_| | | | | | | |_) | | |___            
        \____/ \__,_|_| |_| |_| .__/|_\____/            
                              | |                       
                              |_|                       
______                _                 _        ______ 
| ___ \              | |               (_)       | ___ \
| |_/ /__ _ _ __   __| | ___  _ __ ___  _ _______| |_/ /
|    // _` | '_ \ / _` |/ _ \| '_ ` _ \| |_  / _ \    / 
| |\ \ (_| | | | | (_| | (_) | | | | | | |/ /  __/ |\ \ 
\_| \_\__,_|_| |_|\__,_|\___/|_| |_| |_|_/___\___\_| \_|
                                                        
                                                        
@author: paweljakuszyk
"""
import numpy
import random
from random import sample

SM =['NAWA_065',
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
'NAWA_062']

SM_sample = random.sample(SM, k=10)
print(SM_sample)


NMOSD=['NAWA_036',
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
'Nawa_042']

NMOSD_sample = random.sample(NMOSD, k=10)
print(NMOSD_sample)


HC=['NAWA_045',
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

HC_sample = random.sample(HC, k=10)
print(HC_sample)

random_sample=SM_sample+NMOSD_sample+HC_sample

# open file in write mode and save the list as a txt file
with open('/Users/paweljakuszyk/Documents/fixel_random_sample.txt', 'w') as fp:
    for item in random_sample:
        # write each item on a new line
        fp.write("%s\n" % item)
    print('Done')
