#!/bin/bash

#In this script the fixel measures of FD, FC and FDC will be converted to voxel measures and assessed in NAWM and lesions
#The reasons for converting using specified paramateres are explained in https://community.mrtrix.org/t/fixel2voxel-how-to-extract-primary-secondary-and-tertiary-voxel-based-fd-maps/4394/2

participantdir=$1

participant=$(basename $participantdir)

date=$(date)

echo "Processing participant: $participant"

#Specify directories

tempdir=/home/pjakuszyk/seropositive_project/template

FLAIRdir=$participantdir/Brain/FLAIR

DWIdir=$participantdir/Brain/DWI

#Create directories for output files if they don't exit already
if [[ ! -e $tempdir/FD_sum_voxel_smoothed ]]; then
    mkdir $tempdir/FD_sum_voxel_smoothed
else
  echo "Directory already exists"
fi

if [[ ! -e $tempdir/FC_weighted_mean_voxel_smoothed ]]; then
    mkdir $tempdir/FC_weighted_mean_voxel_smoothed
else
  echo "Directory already exists"
fi

if [[ ! -e $tempdir/FDC_sum_voxel_smoothed ]]; then
    mkdir $tempdir/FDC_sum_voxel_smoothed
else
  echo "Directory already exists"
fi

if [[ ! -e $tempdir/NAWM_and_lesions_in_template_space ]]; then
    mkdir $tempdir/NAWM_and_lesions_in_template_space
else
  echo "Directory already exists"
fi

if [[ ! -e $tempdir/FBA_stats ]]; then
    mkdir $tempdir/FBA_stats
else
  echo "Directory already exists"
fi


###FD
#convert fixel values to voxel

fixel2voxel $tempdir/fd_smooth/${participant}.mif sum $tempdir/FD_sum_voxel_smoothed/${participant}_FD_sum_smooth.mif -force

###FC

fixel2voxel -weighted $tempdir/fd_smooth/${participant}.mif $tempdir/log_fc_smooth/${participant}.mif mean $tempdir/FC_weighted_mean_voxel_smoothed/${participant}_FC_weighted_mean_smooth.mif -force

###FDC

fixel2voxel $tempdir/fdc_smooth/${participant}.mif sum $tempdir/FDC_sum_voxel_smoothed/${participant}_FDC_sum_smooth.mif -force

#Convert scalar maps to nifti

mrconvert $tempdir/FD_sum_voxel_smoothed/${participant}_FD_sum_smooth.mif $tempdir/FD_sum_voxel_smoothed/${participant}_FD_sum_smooth.nii.gz -force

mrconvert $tempdir/FC_weighted_mean_voxel_smoothed/${participant}_FC_weighted_mean_smooth.mif $tempdir/FC_weighted_mean_voxel_smoothed/${participant}_FC_weighted_mean_smooth.nii.gz -force

mrconvert $tempdir/FDC_sum_voxel_smoothed/${participant}_FDC_sum_smooth.mif $tempdir/FDC_sum_voxel_smoothed/${participant}_FDC_sum_smooth.nii.gz -force

#Make binary masks of the maps (>0) that will be used to restrict the NAWM and lesion masks (you can use FD for this mask)

fslmaths $tempdir/FD_sum_voxel_smoothed/${participant}_FD_sum_smooth.nii.gz -thr 0.01 -bin $tempdir/NAWM_and_lesions_in_template_space/${participant}_restriction_mask.nii.gz

#Warp NAWM and lesion masks to template space

##NAWM

mrtransform $DWIdir/NAWM_in_DWI_masked.nii.gz -warp $DWIdir/subject2template_warp.mif $tempdir/NAWM_and_lesions_in_template_space/${participant}_NAWM_in_template.nii.gz -force

#Binarize NAWM mask

fslmaths $tempdir/NAWM_and_lesions_in_template_space/${participant}_NAWM_in_template.nii.gz -thr 0.7 -bin $tempdir/NAWM_and_lesions_in_template_space/${participant}_NAWM_in_template_bin.nii.gz

#Restrict NAWM mask to scalar map binary mask

fslmaths $tempdir/NAWM_and_lesions_in_template_space/${participant}_NAWM_in_template_bin.nii.gz -mas $tempdir/NAWM_and_lesions_in_template_space/${participant}_restriction_mask.nii.gz $tempdir/NAWM_and_lesions_in_template_space/${participant}_NAWM_restricted.nii.gz

#Calculate and store FD, FC and FDC values for NAWM

#FD

FD_NAWM=$(fslstats $tempdir/FD_sum_voxel_smoothed/${participant}_FD_sum_smooth.nii.gz -k $tempdir/NAWM_and_lesions_in_template_space/${participant}_NAWM_restricted.nii.gz -M)

#FC

FC_NAWM=$(fslstats $tempdir/FC_weighted_mean_voxel_smoothed/${participant}_FC_weighted_mean_smooth.nii.gz -k $tempdir/NAWM_and_lesions_in_template_space/${participant}_NAWM_restricted.nii.gz -M)

#FDC

FDC_NAWM=$(fslstats $tempdir/FDC_sum_voxel_smoothed/${participant}_FDC_sum_smooth.nii.gz -k $tempdir/NAWM_and_lesions_in_template_space/${participant}_NAWM_restricted.nii.gz -M)


if [ -e $FLAIRdir/FLAIR_lesion_mask.nii.gz ]
then

  ##Lesions

  mrtransform $DWIdir/lesions_in_DWI_masked.nii.gz -warp $DWIdir/subject2template_warp.mif $tempdir/NAWM_and_lesions_in_template_space/${participant}_lesions_in_template.nii.gz -force

  #Binarize lesion mask

  fslmaths $tempdir/NAWM_and_lesions_in_template_space/${participant}_lesions_in_template.nii.gz -thr 0.3 -bin $tempdir/NAWM_and_lesions_in_template_space/${participant}_lesions_in_template_bin.nii.gz

  #Restrict lesion mask to scalar maps binary masks

  fslmaths $tempdir/NAWM_and_lesions_in_template_space/${participant}_lesions_in_template_bin.nii.gz -mas $tempdir/NAWM_and_lesions_in_template_space/${participant}_restriction_mask.nii.gz $tempdir/NAWM_and_lesions_in_template_space/${participant}_lesions_restricted.nii.gz

  #Calculate and store FD, FC and FDC values for the lesioned WM

  #FD

  FD_lesions=$(fslstats $tempdir/FD_sum_voxel_smoothed/${participant}_FD_sum_smooth.nii.gz -k $tempdir/NAWM_and_lesions_in_template_space/${participant}_lesions_restricted.nii.gz -M)

  #FC

  FC_lesions=$(fslstats  $tempdir/FC_weighted_mean_voxel_smoothed/${participant}_FC_weighted_mean_smooth.nii.gz -k $tempdir/NAWM_and_lesions_in_template_space/${participant}_lesions_restricted.nii.gz -M)

  #FDC

  FDC_lesions=$(fslstats $tempdir/FDC_sum_voxel_smoothed/${participant}_FDC_sum_smooth.nii.gz -k $tempdir/NAWM_and_lesions_in_template_space/${participant}_lesions_restricted.nii.gz -M)


else

  #Create empty variables for participants without WM lesions

  FD_lesions=""

  FC_lesions=""

  FDC_lesions=""

fi

#Make a stats csv file

echo "participant,date,FD_lesions,FC_lesions,FDC_lesions,FD_NAWM,FC_NAWM,FDC_NAWM" > $tempdir/FBA_stats/${participant}_FBA_stats.csv

echo "$participant,$date,$FD_lesions,$FC_lesions,$FDC_lesions,$FD_NAWM,$FC_NAWM,$FDC_NAWM" >> $tempdir/FBA_stats/${participant}_FBA_stats.csv


#Create a csv file with all the necessary stats

#Find a file matches recursively in directory, concat them and drop duplicate headers#


find $tempdir/FBA_stats -type f -name '*_FBA_stats.csv' -exec cat {} \; > $tempdir/FBA_stats/stats_combo.csv; awk '{if (!($0 in x)) {print $0; x[$0]=1} }' $tempdir/FBA_stats/stats_combo.csv > $tempdir/FBA_stats/fixel2voxel_stats_nice.csv


exit
