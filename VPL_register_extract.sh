#!/bin/bash

# Initialize CSV file
output_csv="/Users/paweljakuszyk/Documents/group_FA_MD_values.csv"
echo "Participant_ID,VPL_FA,VPL_MD" > $output_csv


for participantdir in `cat $1`; do

    participant=$(basename $participantdir)
    PROJECT_DIR=/Volumes/Lacie2/seropositive_project/participants/$participant/Brain
    export SUBJECTS_DIR=/Volumes/Lacie2/freesurfer_output/$participant
    BIN_THR=0.4 #Threshold for fslmaths binarisation

    mri_label2vol --seg $SUBJECTS_DIR/mri/ThalamicNuclei.FSvoxelSpace.mgz --temp $SUBJECTS_DIR/mri/rawavg.mgz --regheader $SUBJECTS_DIR/mri/ThalamicNuclei.FSvoxelSpace.mgz --o $SUBJECTS_DIR/mri/ThalamicNuclei_T1_anat.mgz

    mri_binarize --i $SUBJECTS_DIR/mri/ThalamicNuclei_T1_anat.mgz --o $SUBJECTS_DIR/mri/Left-VPL.mgz --match 8133
    mri_binarize --i $SUBJECTS_DIR/mri/ThalamicNuclei_T1_anat.mgz --o $SUBJECTS_DIR/mri/Right-VPL.mgz --match 8233

    mri_convert --in_type mgz --out_type nii $SUBJECTS_DIR/mri/Left-VPL.mgz $SUBJECTS_DIR/mri/Left-VPL.nii.gz 
    mri_convert --in_type mgz --out_type nii $SUBJECTS_DIR/mri/Right-VPL.mgz $SUBJECTS_DIR/mri/Right-VPL.nii.gz

    fslmaths $SUBJECTS_DIR/mri/Left-VPL.nii.gz -add $SUBJECTS_DIR/mri/Right-VPL.nii.gz  -bin $SUBJECTS_DIR/mri/combined_VPL_mask.nii.gz

    flirt -in $SUBJECTS_DIR/mri/combined_VPL_mask.nii.gz -ref $PROJECT_DIR/DWI/mean_b0.nii.gz -out $PROJECT_DIR/DWI/VPL_mask_in_b0.nii.gz -init $PROJECT_DIR/T1/T1_to_b0.mat -applyxfm

    fslmaths $PROJECT_DIR/DWI/VPL_mask_in_b0.nii.gz -thr $BIN_THR -bin $PROJECT_DIR/DWI/VPL_mask_in_b0_bin.nii.gz

    # Extract FA and MD values with fslstats
    VPL_FA=$(fslstats $PROJECT_DIR/DWI/FA.nii.gz -k $PROJECT_DIR/DWI/VPL_mask_in_b0_bin.nii.gz -M)
    VPL_MD=$(fslstats $PROJECT_DIR/DWI/MD.nii.gz -k $PROJECT_DIR/DWI/VPL_mask_in_b0_bin.nii.gz -M)

    # Append results to the CSV file
    echo "$participant,$VPL_FA,$VPL_MD" >> $output_csv

done

echo "FA and MD values saved to $output_csv"

