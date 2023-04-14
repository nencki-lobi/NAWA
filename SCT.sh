#!/bin/bash

#This analysis is done with the Spinal Cord Toolbox https://spinalcordtoolbox.com/
#The files need are the saggital T2 and axial GRE_ME (Medic) in nifti format
#With this we will get: cross-sectional area (CSA) per vertebral level and CSA of the gray and white matter
#The qc reports present fast and convenient way of inspecting analysis steps

T2_path=/Volumes/pjakuszyk/seropositive_project/participants/001_MS_F_TP1/Spine/T2/
GRE_ME_path=/Volumes/pjakuszyk/seropositive_project/participants/001_MS_F_TP1/Spine/GRE_ME/
qc_path=/Users/paweljakuszyk/Documents

T2=/Volumes/pjakuszyk/seropositive_project/participants/001_MS_F_TP1/Spine/T2/001_MS_F_TP1_T2w_20210924141801_4.nii.gz
GRE_ME=/Volumes/pjakuszyk/seropositive_project/participants/001_MS_F_TP1/Spine/GRE_ME/001_MS_F_TP1_GRE-ME_20210924141801_8.nii.gz


####
########First it is best to manually label vertebral levels for CSA -- vertebrae convention: https://spinalcordtoolbox.com/user_section/tutorials/registration-to-template/vertebral-labeling/labeling-conventions.html
####

sct_label_utils -i $T2 -create-viewer 1,2,3,4,5,6,7 -o $T2_path/labels_vertebral.nii.gz -msg "Place labels at the centre of the cord at mid level of vertebral bodies e.g. C3 (value=3), C4 (value=4) and C5 (value=5)"

####
########Perform spinal cord segmentation using deep learning algorithm
####

sct_deepseg_sc -i $T2 -c t2 -ofolder $T2_path/deepseg -qc $qc_path/qc_spinal_cord

##Compute aggregate cross-sectional area (CSA) per vertebral level

sct_process_segmentation -i $T2_path/deepseg/*T2w_*_seg.nii.gz -vert 2,3,4,5,6,7 -vertfile $T2_path/labels_vertebral.nii.gz -perlevel 1 -o $qc_path/csa_per_level.csv

####
########GRE_ME-T2*-weighted data, which has good GM/WM contrast and high in-plane resolution"
####

##Perform cord segmentation

sct_deepseg_sc -i $GRE_ME -c t2s -o $GRE_ME_path/GRE_ME_seg.nii.gz -qc $qc_path/qc_spinal_cord

##Segment gray matter

sct_deepseg_gm -i $GRE_ME -o $GRE_ME_path/GRE_ME_gmseg.nii.gz -qc $qc_path/qc_spinal_cord

##Subtract GM segmentation from cord segmentation to obtain WM segmentation

sct_maths -i $GRE_ME_path/GRE_ME_seg.nii.gz -sub $GRE_ME_path/GRE_ME_gmseg.nii.gz -o $GRE_ME_path/GRE_ME_wmseg.nii.gz

##Compute cross-sectional area (CSA) of the gray and white matter aggregated for all slices in the volume (as opposed to -perslice 1 argumetn which would output perslice values)

sct_process_segmentation -i $GRE_ME_path/GRE_ME_gmseg.nii.gz -o $qc_path/csa_gm.csv -angle-corr 0

sct_process_segmentation -i $GRE_ME_path/GRE_ME_wmseg.nii.gz -o $qc_path/csa_wm.csv -angle-corr 0
