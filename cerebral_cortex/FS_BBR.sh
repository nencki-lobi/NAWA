#!/bin/bash

participantdir=$1

echo "Create participant's log file variables"

participant=$(basename $participantdir)

date=$(date)

projectdir=/home/pjakuszyk/seropositive_project

FSout=/home/pjakuszyk/freesurfer_output

echo "Processing participant: $participant"


if [ -e $participantdir/Brain/MP2RAGE/*mp2rage_offline*nii* ]; then

  # register denoised UNI to T1 used in freesurfer recon-all that matrix will be later used to map R1 volume to FS common surface an cortical parcellation

  singularity exec /opt/software/bids_freesurfer.simg bbregister --s $participant --mov $participantdir/Brain/MP2RAGE/hostrecon_XX/presurf_MPRAGEise/UNI_corrected_MPRAGEised.nii --reg $participantdir/Brain/MP2RAGE/hostrecon_XX/presurf_MPRAGEise/register_UNI2T1.dat --init-coreg --t1 --o $participantdir/Brain/MP2RAGE/UNI_in_T1_FS.nii.gz


  #singularity exec /opt/software/bids_freesurfer.simg bbregister --s NAWA_008 --mov /home/pjakuszyk/seropositive_project/participants/NAWA_008/Brain/MP2RAGE/hostrecon_XX/presurf_MPRAGEise/UNI_corrected_MPRAGEised.nii --reg /home/pjakuszyk/seropositive_project/participants/NAWA_008/Brain/MP2RAGE/hostrecon_XX/presurf_MPRAGEise/register_UNI2T1.lta --init-coreg --t1 --o /home/pjakuszyk/seropositive_project/participants/NAWA_008/Brain/MP2RAGE/hostrecon_XX/presurf_MPRAGEise/UNI_in_T1.nii.gz

  # use the genereated matrix to register t1 map to T1 used in freesurfer

  #singularity exec /opt/software/bids_freesurfer.simg bbregister --s $participant --mov $participantdir/Brain/MP2RAGE/t1map.nii --reg $participantdir/Brain/MP2RAGE/hostrecon_XX/presurf_MPRAGEise/register_t1map2T1.lta --init-reg $participantdir/Brain/MP2RAGE/hostrecon_XX/presurf_MPRAGEise/register_UNI2T1.lta --t2 --o $participantdir/Brain/MP2RAGE/t1map_in_T1_FS.nii.gz


  #singularity exec /opt/software/bids_freesurfer.simg bbregister --s NAWA_008 --mov /home/pjakuszyk/seropositive_project/participants/NAWA_008/Brain/MP2RAGE/t1map.nii --reg /home/pjakuszyk/seropositive_project/participants/NAWA_008/Brain/MP2RAGE/hostrecon_XX/presurf_MPRAGEise/register_t1map2T1.lta --init-reg /home/pjakuszyk/seropositive_project/participants/NAWA_008/Brain/MP2RAGE/hostrecon_XX/presurf_MPRAGEise/register_UNI2T1.lta --t2 --o /home/pjakuszyk/seropositive_project/participants/NAWA_008/Brain/MP2RAGE/t1map_in_T1.nii.gz

  if [ -e $participantdir/Brain/MP2RAGE/UNI_in_T1_FS.nii.gz ]; then

    echo "Finished registering to FS T1 $participant on $date" >> $projectdir/BBR_FS_reg.log

  else

    echo "Something went wrong for $participant - check it manually" >> $projectdir/BBR_FS_reg.log

  fi

else

  echo "$participant does not have an MP2RAGE image" >> $projectdir/BBR_FS_reg.log

fi

exit
