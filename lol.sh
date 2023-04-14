#!/bin/bash

for participantdir in `cat $1`; do

  projectdir=/home/pjakuszyk/seropositive_project

  participant=$(basename $participantdir)

  mslist=/home/pjakuszyk/seropositive_project/MS_patients.txt

  nmosdlist=/home/pjakuszyk/seropositive_project/NMOSD_patients.txt

  dwidir=${participantdir}/Brain/DWI

  flairdir=${participantdir}/Brain/FLAIR

  if [[ ! -e $dwidir/bundle_loads ]]; then
    mkdir $dwidir/bundle_loads
  else
    echo "$dwidir/bundle_loads already exists"
  fi

  if grep -q "$participant" $mslist; then
    echo "MS patient"
    if [ -e $flairdir/FLAIR_lesion_mask.nii.gz ]
    then
      echo "Lesions detected"

      for tract in `cat $projectdir/tract_list.txt`; do

        mrresize -voxel 1.25 ${dwidir}/lesions_in_DWI_masked.nii.gz ${dwidir}/lesions_in_DWI_masked_upsampled.nii.gz -force

        echo "Binarize lesion mask with a low threshold to include partial volume edges"

        fslmaths ${dwidir}/lesions_in_DWI_masked_upsampled.nii.gz -thr 0.1 -bin ${dwidir}/lesions_in_DWI_masked_upsampled_bin.nii.gz

        tckedit ${dwidir}/tractseg_output/TOM_trackings/${tract} ${dwidir}/tractseg_output/TOM_trackings_NAWM/${tract} -exclude ${dwidir}/lesions_in_DWI_masked_upsampled_bin.nii.gz -force

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

        mrresize -voxel 1.25 ${dwidir}/lesions_in_DWI_masked.nii.gz ${dwidir}/lesions_in_DWI_masked_upsampled.nii.gz -force

        echo "Binarize lesion mask with a low threshold to include partial volume edges"

        fslmaths ${dwidir}/lesions_in_DWI_masked_upsampled.nii.gz -thr 0.1 -bin ${dwidir}/lesions_in_DWI_masked_upsampled_bin.nii.gz

        tckedit ${dwidir}/tractseg_output/TOM_trackings/${tract} ${dwidir}/tractseg_output/TOM_trackings_NAWM/${tract} -exclude ${dwidir}/lesions_in_DWI_masked_upsampled_bin.nii.gz -force

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
