#!/bin/bash

participantdir=$1

echo "Create participant's log file variables"

participant=$(basename $participantdir)

date=$(date)

projectdir=/home/pjakuszyk/seropositive_project

HCPout=/home/pjakuszyk/FS_hcp

echo "Processing participant: $participant"


if [ -e $participantdir/Brain/MP2RAGE/*mp2rage_offline*nii* ]; then

  ##register denoised UNI volume to ciftified T1

  flirt -in $participantdir/Brain/MP2RAGE/hostrecon_XX/presurf_MPRAGEise/UNI_corrected_MPRAGEised.nii -ref $HCPout/${participant}/T1w/T1w.nii.gz -omat $participantdir/Brain/MP2RAGE/UNI_to_T1HCP.mat -out $HCPout/${participant}/T1w/UNI_in_T1_HCP.nii.gz

  ##used the obtained registration matrix to regiter R1 volume to ciftified T1

  flirt -in $participantdir/Brain/MP2RAGE/r1map.nii -ref $HCPout/${participant}/T1w/T1w.nii.gz -out $HCPout/${participant}/T1w/R1_in_T1_HCP.nii.gz -init $participantdir/Brain/MP2RAGE/UNI_to_T1HCP.mat -applyxfm


  if [ -e $HCPout/${participant}/T1w/R1_in_T1_HCP.nii.gz ]; then

    echo "Finished registering R1 volume to ciftified T1 for $participant on $date" >> $projectdir/R1_to_cifti.log

  else

    echo "Something went wrong for $participant - check it manually" >> $projectdir/R1_to_cifti.log

  fi

else

  echo "$participant does not have an MP2RAGE image" >> $projectdir/R1_to_cifti.log

fi

exit
