#!/bin/bash

#Lesion volume calc (You need to have FLAIR lesion masks prepared)

participantdir=$1

cd $participantdir

participant=$(basename $participantdir)

date=$(date)

echo "Processing participant: $participant"

cd Brain/FLAIR

if [ -e FLAIR_lesion_mask.nii.gz ]
then

  #to cut out the first value which is the voxel numbe not volume
  volume_lesions=$(fslstats FLAIR_lesion_mask.nii.gz -V | cut -d' ' -f 2)
  
else

  volume_lesions=""

fi

cd ../../

echo "Make a stats csv file"

echo "participant,date,volume_lesions" > stats_lesions.csv

echo "$participant,$date,$volume_lesions" >> stats_lesions.csv

echo "Create a csv file with all the necessary stats"

echo "Find a file matches recursively in directory, concat them and drop duplicate headers:"

cd /home/pjakuszyk/seropositive_project

find /home/pjakuszyk/seropositive_project -type f -name 'stats_lesions.csv' -exec cat {} \; > stats_combo_lesions.csv; awk '{if (!($0 in x)) {print $0; x[$0]=1} }' stats_combo_lesions.csv > lesions_stats_nice.csv

exit
