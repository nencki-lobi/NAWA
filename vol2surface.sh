#!/bin/bash

participantdir=$1

echo "Create participant's log file variables"

participant=$(basename $participantdir)

date=$(date)

projectdir=/home/pjakuszyk/seropositive_project

FSout=/home/pjakuszyk/freesurfer_output

echo "Processing participant: $participant"


if [ -e $participantdir/Brain/MP2RAGE/*mp2rage_offline*nii* ]; then

  ##map r1 volume to cortical surface for each hemisphere

  #left hemi
  singularity exec /opt/software/bids_freesurfer.simg  mri_vol2surf --src $participantdir/Brain/MP2RAGE/r1map.nii --reg $participantdir/Brain/MP2RAGE/hostrecon_XX/presurf_MPRAGEise/register_UNI2T1.dat  --out $participantdir/Brain/MP2RAGE/lh_${participant}_r1map.mgh --regheader $participant --hemi lh --projfrac 0.5 --fwhm 5

  #right hemi
  singularity exec /opt/software/bids_freesurfer.simg  mri_vol2surf --src $participantdir/Brain/MP2RAGE/r1map.nii --reg $participantdir/Brain/MP2RAGE/hostrecon_XX/presurf_MPRAGEise/register_UNI2T1.dat  --out $participantdir/Brain/MP2RAGE/rh_${participant}_r1map.mgh --regheader $participant --hemi rh --projfrac 0.5 --fwhm 5


  #singularity exec /opt/software/bids_freesurfer.simg mri_vol2surf --src /home/pjakuszyk/seropositive_project/participants/NAWA_008/Brain/MP2RAGE/t1map_in_T1_FS.nii.gz --out /home/pjakuszyk/seropositive_project/participants/NAWA_008/Brain/MP2RAGE/rh_NAWA_008_t1map.mgh --regheader NAWA_008 --hemi rh --projfrac 0.5 --fwhm 5

  #sample r1 values along the cortex

  #left hemi

  singularity exec /opt/software/bids_freesurfer.simg mri_segstats --annot $participant lh aparc.a2009s --i $participantdir/Brain/MP2RAGE/lh_${participant}_r1map.mgh --sum $participantdir/Brain/MP2RAGE/lh_${participant}_r1map.sum

  #right hemi

  singularity exec /opt/software/bids_freesurfer.simg mri_segstats --annot $participant rh aparc.a2009s --i $participantdir/Brain/MP2RAGE/rh_${participant}_r1map.mgh --sum $participantdir/Brain/MP2RAGE/rh_${participant}_r1map.sum


  if [ -e $participantdir/Brain/MP2RAGE/rh_${participant}_r1map.sum ]; then

    echo "Finished registering T1 volume to cortical surface for $participant on $date" >> $projectdir/vol_surf_FS_reg.log

  else

    echo "Something went wrong for $participant - check it manually" >> $projectdir/vol_surf_FS_reg.log

  fi

  #copy inflated surfaces from FS dir to be able to review the data (high r1-high myelination should be visible in central gyrus and visual cortex)

  cp $FSout/${participant}/surf/lh.inflated $participantdir/Brain/MP2RAGE/lh.inflated
  cp $FSout/${participant}/surf/rh.inflated $participantdir/Brain/MP2RAGE/rh.inflated

else

  echo "$participant does not have an MP2RAGE image" >> $projectdir/vol_surf_FS_reg.log

fi

exit
