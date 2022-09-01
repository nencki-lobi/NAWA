#!/bin/bash

participantdir=$1

cd $participantdir

echo "Store participant id as variable"

participant=$(basename $participantdir)

echo "Now processing participant: $participant"

cd Brain/FLAIR

echo "Brain extract FLAIR"

bet *spc_da-fl*.nii* FLAIR_bet.nii.gz -f 0.4 -R

cd ../T1

echo "Brain extract and perform bias field correction on T1"

bet *t1_mpr_iso_*.nii* T1_bet_biascorr.nii.gz -f 0.4 -B -R

echo "Register FLAIR to T1"

cd ../FLAIR

flirt -in FLAIR_bet.nii.gz -ref ../T1/T1_bet_biascorr.nii.gz -out ../T1/FLAIR_in_T1 -omat ../T1/FLAIR_to_T1.mat -dof 12 -cost normmi

echo "Check for lesion mask to determine whether lesion filling is needed"


if [ -e FLAIR_lesion_mask.nii.gz ]
then

    echo "The lesion mask exists"
    
    echo "Use the obtained transformation matrix to register FLAIR lesion mask to T1"

    flirt -in FLAIR_lesion_mask.nii.gz -ref ../T1/T1_bet_biascorr.nii.gz -out ../T1/FLAIR_lesion_mask_in_T1.nii.gz -init ../T1/FLAIR_to_T1.mat -applyxfm -interp nearestneighbour

    echo "Use the lesion mask to perform the T1 lesion filling"

    cd ../T1

    lesion_filling -i *t1_mpr_iso_*.nii* -l FLAIR_lesion_mask_in_T1.nii.gz -o T1_filled.nii.gz

    lesion_filling -i T1_bet_biascorr.nii.gz -l FLAIR_lesion_mask_in_T1.nii.gz -o T1_filled_bet.nii.gz

    echo "Use lesion flilled T1 to perform recon-all"

    singularity exec /opt/software/bids_freesurfer.simg recon-all -s $participant -i T1_filled.nii.gz -sd /home/pjakuszyk/freesurfer_output/ -all

else

    echo "There is no lesion mask"

    cd ../T1

    echo "Use orginal T1 to perform recon-all"

    singularity exec /opt/software/bids_freesurfer.simg recon-all -s $participant -i *t1_mpr_iso_*.nii* -sd /home/pjakuszyk/freesurfer_output/ -all

fi

cd /home/pjakuszyk/seropositive_project

recon_last_line=$(tail -1 /home/pjakuszyk/freesurfer_output/$participant/scripts/recon-all.log)

echo "Make a text file with last lines from recon-all.log"

echo "$recon_last_line" >> recon_last_line.txt

subdir=/home/pjakuszyk/freesurfer_output

printf "Calculate cortical thickness based on the output from the recon-all command.\nIt has to be calculated for the left and right hemisphere separately and the average is taken into account.\n"

singularity exec /opt/software/bids_freesurfer.simg mris_anatomical_stats -log FS_stats/${participant}_cortical_thickness_lh.log ${participant} lh
singularity exec /opt/software/bids_freesurfer.simg mris_anatomical_stats -log FS_stats/${participant}_cortical_thickness_rh.log ${participant} rh

exit
