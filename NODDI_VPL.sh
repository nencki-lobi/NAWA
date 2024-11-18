#!/bin/bash

# Initialize CSV file
output_csv="/Users/paweljakuszyk/Documents/group_NODDI_values.csv"
echo "Participant_ID,VPL_NDI,VPL_ISO,VPL_ODI" > $output_csv


for participantdir in `cat $1`; do

    participant=$(basename $participantdir)
    PROJECT_DIR=/Volumes/Lacie2/seropositive_project/participants/$participant/Brain
    
    VPL_NDI=$(fslstats $PROJECT_DIR/DWI/NODDI_ficvf.nii -k $PROJECT_DIR/DWI/VPL_mask_in_b0_bin.nii.gz -M)
    VPL_ISO=$(fslstats $PROJECT_DIR/DWI/NODDI_fiso.nii -k $PROJECT_DIR/DWI/VPL_mask_in_b0_bin.nii.gz -M)
    VPL_ODI=$(fslstats $PROJECT_DIR/DWI/NODDI_odi.nii -k $PROJECT_DIR/DWI/VPL_mask_in_b0_bin.nii.gz -M)

    # Append results to the CSV file
    echo "$participant,$VPL_NDI,$VPL_ISO,$VPL_ODI" >> $output_csv

done

echo "NODDI values saved to $output_csv"

