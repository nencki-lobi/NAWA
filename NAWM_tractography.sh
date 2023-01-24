#!/bin/bash

for participantdir in `cat $1`; do

  projectdir=/home/pjakuszyk/seropositive_project

  participant=$(basename $participantdir)

  mslist=/home/pjakuszyk/seropositive_project/MS_patients.txt

  nmosdlist=/home/pjakuszyk/seropositive_project/NMOSD_patients.txt

  dwidir=${participantdir}/Brain/DWI

  flairdir=${participantdir}/Brain/FLAIR

  if [[ ! -e $dwidir/tractseg_output/TOM_trackings_NAWM ]]; then
    mkdir $dwidir/tractseg_output/TOM_trackings_NAWM
  else
    echo "$dwidir/tractseg_output/TOM_trackings_NAWM already exists"
  fi

  if grep -q "$participant" $mslist; then
    echo "MS patient"
    if [ -e $flairdir/FLAIR_lesion_mask.nii.gz ]
    then
      echo "Lesions detected"

      for tract in `cat $projectdir/tract_list.txt`; do

        tckedit ${dwidir}/tractseg_output/TOM_trackings/${tract} ${dwidir}/tractseg_output/TOM_trackings_NAWM/${tract} -exclude ${dwidir}/lesions_in_DWI_masked.nii.gz -force

      done

    else

      echo "No lesions"

      cp ${dwidir}/tractseg_output/TOM_trackings/* ${dwidir}/tractseg_output/TOM_trackings_NAWM/.

    fi



  elif grep -q "$participant" $nmosdlist; then

    echo "NMOSD patient"
    if [ -e $flairdir/FLAIR_lesion_mask.nii.gz ]
    then
      echo "Lesions detected"

      for tract in `cat $projectdir/tract_list.txt`; do

        tckedit ${dwidir}/tractseg_output/TOM_trackings/${tract} ${dwidir}/tractseg_output/TOM_trackings_NAWM/${tract} -exclude ${dwidir}/lesions_in_DWI_masked.nii.gz -force

      done

    else

      echo "No lesions"

      cp ${dwidir}/tractseg_output/TOM_trackings/* ${dwidir}/tractseg_output/TOM_trackings_NAWM/.

    fi


  else

    echo "HC"
    cp ${dwidir}/tractseg_output/TOM_trackings/* ${dwidir}/tractseg_output/TOM_trackings_NAWM/.

  fi

done


exit
