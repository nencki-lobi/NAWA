#!/bin/bash

participantdir=$1

cd $participantdir

echo "Store participant id as variable"

participant=$(basename $participantdir)

echo "Now processing participant: $participant"

cd Brain/FLAIR

echo "Check for lesion mask to determine which T1 image to use"

if [ -e FLAIR_lesion_mask.nii.gz ]
then

    echo "The lesion mask exists"
    
    cd ../T1
    
    echo "Use lesion flilled T1 to perform recon-all"

    singularity exec /opt/software/bids_freesurfer.simg recon-all -s $participant -i T1_filled_fixed.nii.gz -sd /home/pjakuszyk/freesurfer_output/ -all

else

    echo "There is no lesion mask"

    cd ../T1

    echo "Use orginal T1 to perform recon-all"

    singularity exec /opt/software/bids_freesurfer.simg recon-all -s $participant -i *t1_mpr_iso_*.nii* -sd /home/pjakuszyk/freesurfer_output/ -all

fi

echo "Make a text file with last lines from recon-all.log"

cd /home/pjakuszyk/seropositive_project

recon_last_line=$(tail -1 /home/pjakuszyk/freesurfer_output/$participant/scripts/recon-all.log)

echo "$recon_last_line" >> recon_last_line.txt

printf "Calculate cortical thickness based on the output from the recon-all command.\nIt has to be calculated for the left and right hemisphere separately and the average is taken into account.\n"

singularity exec /opt/software/bids_freesurfer.simg mris_anatomical_stats -log FS_stats/${participant}_cortical_thickness_lh.log ${participant} lh
singularity exec /opt/software/bids_freesurfer.simg mris_anatomical_stats -log FS_stats/${participant}_cortical_thickness_rh.log ${participant} rh

exit
