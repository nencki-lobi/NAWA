#!/bin/bash

for participantdir in `cat $1`; do

  cd $participantdir

  cd Spine/T2

  echo "Manual vertebral labeling for CSA"

  sct_label_utils -i *T2w_*.nii.gz -create-viewer 1,2,3,4,5,6,7 -o labels_vertebral.nii.gz -msg "Place labels at the centre of a cord at vertebral bodies e.g. C2-C3 (value=3), C3-C4 (value=4) and C4-C5 (value=5)"

done
