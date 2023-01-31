#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 15:34:34 2023

@author: paweljakuszyk
"""

import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
from tractseg.libs import tractometry


# Load the tck tract
tck_file = nib.streamlines.load("/Volumes/pjakuszyk/seropositive_project/participants/NAWA_035/Brain/DWI/tractseg_output/TOM_trackings_NAWM/ILF_left.tck")
streamlines = tck_file.streamlines

# Load the scalar image
scalar_image = nib.load('/Volumes/pjakuszyk/seropositive_project/participants/NAWA_035/Brain/DWI/NODDI_ficvf_resampled.nii.gz')

# Load the begginig image
beginnings = nib.load("/Volumes/pjakuszyk/seropositive_project/participants/NAWA_035/Brain/DWI/tractseg_output/endings_segmentations/ILF_left_b.nii.gz")

# Set the number of points to sample along each streamline
NR_POINTS = 100

# Set the dilation factor
DILATION_0 = 0
DILATION_1 = 1
DILATION_2 = 2


# Run the first version of evaluate_along_streamlines with dilation factor of 0
mean, std = tractometry.evaluate_along_streamlines(np.nan_to_num(scalar_image.get_fdata()), streamlines, beginnings.get_fdata(),
                                                               nr_points=NR_POINTS, dilate=DILATION_0, affine=scalar_image.affine)

# Run the first version of evaluate_along_streamlines with dilation factor of 1
mean1, std1 = tractometry.evaluate_along_streamlines(np.nan_to_num(scalar_image.get_fdata()), streamlines, beginnings.get_fdata(),
                                                               nr_points=NR_POINTS, dilate=DILATION_1, affine=scalar_image.affine)

# Run the second version of evaluate_along_streamlines with dilation factor of 2
mean2, std2 = tractometry.evaluate_along_streamlines(np.nan_to_num(scalar_image.get_fdata()), streamlines, beginnings.get_fdata(),
                                                               nr_points=NR_POINTS, dilate=DILATION_2, affine=scalar_image.affine)


# Plot the mean values for each version
plt.plot(mean, '-b', label='dilation factor 0')
plt.plot(mean1, '--r', label='dilation factor 1')
plt.plot(mean2, ':g', label='dilation factor 2')
plt.legend()
plt.xlabel('Streamline index')
plt.ylabel('Mean scalar value')
plt.title('Mean scalar value comparison')
plt.show()

# Plot the standard deviation values for each version
plt.plot(std, '-b', label='dilation factor 0')
plt.plot(std1, '--r', label='dilation factor 1')
plt.plot(std2, ':g', label='dilation factor 2')
plt.legend()
plt.xlabel('Streamline index')
plt.ylabel('Standard deviation of scalar values')
plt.title('Standard deviation comparison')
plt.show()
