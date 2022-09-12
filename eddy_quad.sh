#!/bin/bash

participantdir=$1

cd $participantdir

cd Brain/DWI

directory=$(ls -td -- dwifslpreproc*/ | head -n 1)

cp -r $directory dwi_fslpreproc_qc

cd dwi_fslpreproc_qc

eddy_quad dwi_post_eddy -idx eddy_indices.txt -par eddy_config.txt -m eddy_mask.nii -b bvals -f field_map.nii.gz -v

exit
