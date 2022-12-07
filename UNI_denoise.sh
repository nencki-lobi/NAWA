#!/bin/bash

participantdir=$1

echo "Create participant's log file variables"

participant=$(basename $participantdir)

date=$(date)

projectdir=/home/pjakuszyk/seropositive_project

echo "Processing participant: $participant"

cd $participantdir/Brain/MP2RAGE

if [ -e *mp2rage_offline*nii* ]; then

  matlab -nodisplay -nosplash -singleCompThread -batch "addpath(genpath('/opt/software/spm12'));addpath(genpath('/home/pjakuszyk/presurfer-main'));presurf_MPRAGEise('hostrecon_XX/INV2_corrected.nii', 'hostrecon_XX/UNI_corrected.nii');exit;"

  if [ -e hostrecon_XX/presurf_MPRAGEise/UNI_corrected_MPRAGEised.nii ]; then

    echo "Finished denoising UNI for $participant on $date" >> $projectdir/MP2RAGE_denoising.log

  else

    echo "Something went wrong for $participant - check it manually" >> $projectdir/MP2RAGE_denoising.log

  fi

else

  echo "$participant does not have an MP2RAGE image" >> $projectdir/MP2RAGE_denoising.log

fi

exit
