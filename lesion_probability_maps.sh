#!/bin/bash

for participantdir in `cat $1`; do

  fixeldir=/home/pjakuszyk/seropositive_project/template_random/lesion_probability

  participant=$(basename $participantdir)

  mslist=/home/pjakuszyk/seropositive_project/MS_patients.txt

  nmosdlist=/home/pjakuszyk/seropositive_project/NMOSD_patients.txt

  dwidir=${participantdir}/Brain/DWI

  if grep -q "$participant" $mslist; then
    echo "MS patient"

    mrtransform ${dwidir}/lesions_in_DWI_masked.nii.gz -warp ${dwidir}/subject2template_warp.mif -interp nearest -datatype bit ${fixeldir}/MS_${participant}.nii.gz


  elif grep -q "$participant" $nmosdlist; then

    echo "NMOSD patient"

    mrtransform ${dwidir}/lesions_in_DWI_masked.nii.gz -warp ${dwidir}/subject2template_warp.mif -interp nearest -datatype bit ${fixeldir}/NMOSD_${participant}.nii.gz


  else

    echo "HC"

  fi

done

fsladd ${fixeldir}/MS_lesion_probablity_map.nii.gz -m ${fixeldir}/MS_*.nii.gz

fsladd ${fixeldir}/NMOSD_lesion_probablity_map.nii.gz -m ${fixeldir}/NMOSD_*.nii.gz

exit
