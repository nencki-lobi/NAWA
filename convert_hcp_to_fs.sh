participantdir=$1

echo "Create participant's log file variables"

participant=$(basename $participantdir)

date=$(date)

projectdir=/home/pjakuszyk/seropositive_project

HCPout=/home/pjakuszyk/FS_hcp

FSout=/home/pjakuszyk/freesurfer_output

echo "Processing participant: $participant"


if [ -e $participantdir/Brain/MP2RAGE/*mp2rage_offline*nii* ]; then

  ##map r1 volume to cortical surface for each hemisphere

  #left hemi
  singularity exec /opt/software/bids_freesurfer.simg  mri_convert $HCPout/${participant}/MNINonLinear/Native/${participant}.L.SmoothedqR1.native.func.gii $FSout/${participant}/surf/lh.smoothedR1.mgh

  #right hemi
  singularity exec /opt/software/bids_freesurfer.simg  mri_convert $HCPout/${participant}/MNINonLinear/Native/${participant}.R.SmoothedqR1.native.func.gii $FSout/${participant}/surf/rh.smoothedR1.mgh

else

  echo "$participant does not have an MP2RAGE image" 

fi

exit
