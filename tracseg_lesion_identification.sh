#!/bin/bash

for participantdir in `cat $1`; do

  echo "Create  participant's log file variables"

  participant=$(basename $participantdir)

  date=$(date)

  projectdir=/home/pjakuszyk/archive/seropositive_project

  mslist=/home/pjakuszyk/archive/seropositive_project/MS_patients.txt

  nmosdlist=/home/pjakuszyk/archive/seropositive_project/NMOSD_patients.txt

  fixeldir=/home/pjakuszyk/archive/seropositive_project/template_random/

  flairdir=${participantdir}/Brain/FLAIR

  dwidir=${participantdir}/Brain/DWI/tractseg_output

  cd $dwidir

  if grep -q "$participant" $mslist; then
    echo "MS patient"
    if [ -e $flairdir/FLAIR_lesion_mask.nii.gz ]
    then
      echo "Lesions detected"

      echo "Processing participant: $participant"

      Tractometry -i TOM_trackings_lesions/ -o Tractometry_lesion_identification.csv -e endings_segmentations/ -s ../lesions_in_DWI_masked_upsampled_bin.nii.gz


    else

      echo "No lesions"

    fi

  elif grep -q "$participant" $nmosdlist; then

    echo "NMOSD patient"
    if [ -e $flairdir/FLAIR_lesion_mask.nii.gz ]
    then
      echo "Lesions detected"

      echo "Processing participant: $participant"

      Tractometry -i TOM_trackings_lesions/ -o Tractometry_lesion_identification.csv -e endings_segmentations/ -s ../lesions_in_DWI_masked_upsampled_bin.nii.gz


    else

      echo "No lesions"

    fi

  else

    echo "HC"

  fi

  if [ -f Tractometry_lesion_identification.csv ]; then

    echo "Finished identifying lesions for $participant on $date" >> $projectdir/TractSeg_lesion_identification.log

  else

    echo "Something went wrong for $participant - check it manually" >> $projectdir/TractSeg_lesion_identification.log

  fi

done

exit
