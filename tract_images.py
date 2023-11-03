#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 12:36:20 2023

@author: paweljakuszyk
"""
import os
import nibabel as nib
import numpy as np
from dipy.io.streamline import load_tractogram, save_tractogram
from dipy.viz import window, actor
from dipy.io.stateful_tractogram import StatefulTractogram
from PIL import Image

path_to_master_dir='/Volumes/ms/seropositive_project/participants/001_MS_F_TP1/Brain/DWI/'

path_to_tck='/Volumes/ms/seropositive_project/participants/001_MS_F_TP1/Brain/DWI/tractseg_output/TOM_trackings/'

path_to_nii='/Volumes/ms/seropositive_project/participants/001_MS_F_TP1/Brain/DWI/tractseg_output/TOM/'

path_to_write='/Volumes/ms/seropositive_project/track_figures/MS/'

path_to_write_triplets='/Volumes/ms/seropositive_project/track_figures/MS/triplets/'

path_to_merged_tck ='/Volumes/ms/seropositive_project/participants/001_MS_F_TP1/Brain/DWI/tractseg_output/reduced/'

# Create the folder if it doesn't exist
if not os.path.exists(path_to_write):
    os.makedirs(path_to_write)
    
if not os.path.exists(path_to_merged_tck):
    os.makedirs(path_to_merged_tck)
    
if not os.path.exists(path_to_write_triplets):
    os.makedirs(path_to_write_triplets)

# Load binary brain mask
mask = nib.load(path_to_master_dir + 'dwi_mask_upsampled.nii.gz')

mask_data = mask.get_fdata()

# Get a list of all .tck files in the folder
tck_files = [f for f in os.listdir(path_to_tck) if f.endswith('.tck')]

# Group the .tck files by their basename
tck_files_by_basename = {}
for tck_file in tck_files:
    basename = os.path.splitext(tck_file)[0].rsplit('_', 1)[0]
    if basename not in tck_files_by_basename:
        tck_files_by_basename[basename] = []
    tck_files_by_basename[basename].append(tck_file)
    
SLF =[]       
# Loop over the basenames and merge the corresponding .tck files
for basename, tck_files in tck_files_by_basename.items():
    # Load all the .tck files
    streamlines = []
    for tck_file in tck_files:
        tck_path = os.path.join(path_to_tck, tck_file)
        streamlines.append(load_tractogram(tck_path, mask))
    if len(tck_files) == 1:
        merged_tract = streamlines[0]
        print(basename)
    elif basename == 'CC':
        del streamlines[6]
        # merge 1 to 5
        merged_tract = streamlines[0]+streamlines[1]+streamlines[2]+streamlines[3]+streamlines[4]+streamlines[5]+streamlines[6]
    elif basename.startswith('SLF'):
        # do something else
        SLF.extend(streamlines)
    else:
        merged_tract = streamlines[0]+streamlines[1]
    
    # Save the merged streamlines to a new file
    out_path = os.path.join(path_to_merged_tck, f'{basename}.tck')
    save_tractogram(merged_tract, out_path)

#FOR SLF
merged_SLF = SLF[0]+SLF[1]+SLF[2]+SLF[3]+SLF[4]+SLF[5]
out_path = os.path.join(path_to_merged_tck, 'SLF.tck')
save_tractogram(merged_SLF, out_path)


####Make figures


# Get a list of all .tck files in the folder
tck_files_reduced = [f for f in os.listdir(path_to_merged_tck) if f.endswith('.tck')]

# Create an orientation marker widget (arrows int the x y z axes)
axes = actor.axes(scale=(100, 100, 100))

# Iterate through each .tck file
for tck_file in tck_files_reduced:
    tract = path_to_merged_tck + tck_file
    # Load the tract
    tractogram = load_tractogram(tract, mask)  
    #Get tract name without .tck
    tck_name = os.path.splitext(tck_file)[0]
    
    # Check alignment of both files you wish to overlay by verifyin affine matrices
    # Get the affine transformation from the mask image
    affine_mask = mask.affine
    affine_tractogram = tractogram.affine
    #they are the same so we will supply one of them as affine in the figure        
    # Create a 3D visualization window
    scene = window.Scene()
    # Scene widget customization
    #Add axes
    #scene.add(axes)
    
    # Create an isosurface of the binary mask image to form the "glass brain"
    vol_actor = actor.contour_from_roi(mask_data, affine=affine_mask, opacity=0.3)
    # Add the isosurface to the visualization window
    scene.add(vol_actor)
    # Create an actor for the streamlines
    stream_actor = actor.line(tractogram.streamlines)
    # Add the streamlines actor to the visualization window
    scene.add(stream_actor)
    
    # Save the visualization window to a PNG file for axial view
    scene.set_camera(position=(0, 0, 300), focal_point=(0, 0, 0), view_up=(0, 1, 0))
    scene.reset_clipping_range()
    window.record(scene, out_path=path_to_write+tck_name+'_axial.png', size=(800, 800))
   
    # Save the visualization window to a PNG file for coronal view
    scene.set_camera(position=(0, 300, 0), focal_point=(0, 0, 0), view_up=(0, 1, 0))
    scene.reset_clipping_range()
    window.record(scene, out_path=path_to_write+tck_name+'_coronal.png', size=(800, 800))

    # Save the visualization window to a PNG file for sagittal view
    scene.set_camera(position=(300, 0, 0), focal_point=(0, 0, 0), view_up=(0, 0, 1))
    #scene.reset_clipping_range()
    window.record(scene, out_path=path_to_write+tck_name+'_sagittal.png', size=(800, 800))
    

##Combine image triplets into one .PNG per tract
# Path to the directory containing the image files
img_dir = path_to_write

# Loop through each file in the directory
for filename in os.listdir(img_dir):
    if filename.endswith('.png'):
        # Split the filename into base name and suffix
        basename, suffix = filename.rsplit('_', 1)
        suffix = '.' + suffix
        #print(basename)
        # Check if the suffix is axial, sagittal, or coronal
        if suffix in ('.axial.png', '.sagittal.png', '.coronal.png'):
            #print(basename)
            # Get the corresponding filenames for the other two views
            axial_filename = os.path.join(img_dir, basename+'_axial.png')
            sagittal_filename = os.path.join(img_dir, basename+'_sagittal.png')
            coronal_filename = os.path.join(img_dir, basename+'_coronal.png')
            # Check if the other two views exist
            if (os.path.exists(axial_filename) and
                os.path.exists(sagittal_filename) and
                os.path.exists(coronal_filename)):
                # Open the images
                axial_img = Image.open(axial_filename)
                sagittal_img = Image.open(sagittal_filename)
                coronal_img = Image.open(coronal_filename)
                # Combine the images horizontally
                combined_img = Image.new('RGB', (axial_img.width + sagittal_img.width + coronal_img.width, axial_img.height))
                combined_img.paste(axial_img, (0, 0))
                combined_img.paste(sagittal_img, (axial_img.width, 0))
                combined_img.paste(coronal_img, (axial_img.width + sagittal_img.width, 0))
                # Save the combined image
                combined_filename = os.path.join(path_to_write_triplets, basename+'_combined.png')
                combined_img.save(combined_filename)



