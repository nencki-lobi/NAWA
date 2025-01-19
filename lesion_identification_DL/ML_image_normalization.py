#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 13:16:01 2023

@author: pawel
"""

import os
import nibabel as nib
import numpy as np

#########LOADING DATA#########
data_dir = "/Volumes/ms/ML/LD_data_copy/"

flair_dir = os.path.join(data_dir, 'FLAIR')
mask_dir = os.path.join(data_dir, 'lesion_masks')

output_dir = os.path.join(data_dir, 'normalized_FLAIR')

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate over the FLAIR images and save normalized images
for i, filename in enumerate(os.listdir(flair_dir)):
    if filename.endswith('.nii.gz'):
        flair_path = os.path.join(flair_dir, filename)
        try:
            flair_img = nib.load(flair_path)
            flair_data = flair_img.get_fdata()

            # Normalize the FLAIR image
            image_min = np.min(flair_data)
            image_max = np.max(flair_data)
            normalized_image = (flair_data - image_min) / (image_max - image_min)

            # Create a new Nifti image with the normalized data, using the original header and affine
            normalized_img = nib.Nifti1Image(normalized_image, affine=flair_img.affine, header=flair_img.header)

            # Save the normalized image to the output directory
            output_path = os.path.join(output_dir, filename)
            nib.save(normalized_img, output_path)

        except nib.filebasedimages.ImageFileError:
            print(f"Error loading file: {flair_path}")
            continue

print("Normalized FLAIR images saved successfully.")




