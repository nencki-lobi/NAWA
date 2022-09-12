#!/bin/bash

participantdir=$1

echo "Create participant's log file variables"

participant=$(basename $participantdir)

date=$(date)

echo "Processing participant: $participant"

cd $participantdir

cd Brain/DWI

matlab -nodisplay -nosplash -singleCompThread -batch "addpath(genpath('/home/pjakuszyk/NODDI_toolbox_v1.05'));addpath(genpath('/home/pjakuszyk/nifti_matlab-master'));CreateROI('den_preproc_unbiased.nii', 'mask.nii', 'NODDI_roi.mat');protocol = FSL2Protocol('den_preproc_unbiased.bval', 'den_preproc_unbiased.bvec', 5);noddi = MakeModel('WatsonSHStickTortIsoV_B0');batch_fitting_single('NODDI_roi.mat', protocol, noddi, 'FittedParams.mat');SaveParamsAsNIfTI('FittedParams.mat', 'NODDI_roi.mat', 'mask.nii', 'NODDI');exit;"

echo "Finished fitting NODDI on $participant at $date" > NODDI_.log

exit
