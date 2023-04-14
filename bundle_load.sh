#!/bin/bash

for participantdir in `cat $1`; do

  projectdir=/Volumes/pjakuszyk/seropositive_project

  participant=$(basename $participantdir)

  compute_BL="python /Users/paweljakuszyk/Lesionometry/lesionometry/compute_BL.py"

  mslist=/Volumes/pjakuszyk/seropositive_project/MS_patients.txt

  nmosdlist=/Volumes/pjakuszyk/seropositive_project/NMOSD_patients.txt

  dwidir=$participantdir/Brain/DWI

  flairdir=$participantdir/Brain/FLAIR

  if [[ ! -e $dwidir/bundle_loads ]]; then
    mkdir $dwidir/bundle_loads
  else
    echo "$dwidir/bundle_loads already exists"
  fi

  rm $dwidir/bundle_loads/BundleLoad.csv

  if grep -q "$participant" $mslist; then
    echo "MS patient"
    if [ -e $flairdir/FLAIR_lesion_mask.nii.gz ]
    then
      echo "Lesions detected"

      for tract in `cat $projectdir/tract_list.txt`; do

        echo "Calculate bundle load for ${tract}"

        $compute_BL $dwidir/lesions_in_DWI_masked_upsampled_bin.nii.gz $dwidir/tractseg_output/TOM_trackings/${tract}.tck -s ${tract} -o $dwidir/bundle_loads

      done

    else

      echo "No lesions"

    fi

  elif grep -q "$participant" $nmosdlist; then

    echo "NMOSD patient"
    if [ -e $flairdir/FLAIR_lesion_mask.nii.gz ]
    then
      echo "Lesions detected"

      for tract in `cat $projectdir/tract_list.txt`; do

        echo "Calculate bundle load for ${tract}"

        $compute_BL $dwidir/lesions_in_DWI_masked_upsampled_bin.nii.gz $dwidir/tractseg_output/TOM_trackings/${tract}.tck -s ${tract} -o $dwidir/bundle_loads

      done

    else

      echo "No lesions"

      #cp ${dwidir}/tractseg_output/TOM_trackings/* ${dwidir}/tractseg_output/TOM_trackings_NAWM/.

    fi


  else

    echo "HC"

  fi

done


exit
