#!/bin/bash

#The configuration file for fnirt has been changed due to an error. The lambda parameter was manipulated according to this solution:

#> Warning, Jacobian not within prescribed range. Prescription is 0.01 -- 100 and obtained range is -0.00444645 -- 3.01544

#After each iteration fnirt attempts to make sure that the Jacobians
#(stretches and compressions) are within a pre-determined range. You have
#used the default range, which basically just assures that the field is
#invertible. When doing that fnirt runs a fixed number of iterations, and
#if it hasn't succeeded after those iterations it prints the error message
#above.

#For the next release I'll change that so that one can set the number of
#iterations (to make sure it "always" succeeds). For the time being I would
#recommend that you slightly increase the amount of regularisation that you
#are using. I.e. in your config file you increase the values for lambda.

#If you are using the T1_2_MNI152_2mm file you might e.g. change lamda to

#--lambda=400,200,150,75,60,45

#and I would expect the problem to go away.

#Good luck Jesper


participantdir=$1

cd $participantdir

cd Brain/T1

if [ -e ../FLAIR/FLAIR_lesion_mask.nii.gz ]
then

  #To register the T1-weighted image to standard space requires the following commands to be run:

  flirt -in T1_filled_bet_fixed.nii.gz -ref $FSLDIR/data/standard/MNI152_T1_2mm_brain.nii.gz -dof 12 -omat T1_to_MNI.mat

  #FNIRT requires whole head (non-brain-extracted) input and reference images for optimal accuracy

  cp ../../../../T1_2_MNI152_2mm_lambda_change.cnf .

  fnirt --in=T1_filled_fixed.nii.gz --aff=T1_to_MNI.mat --config=T1_2_MNI152_2mm_lambda_change.cnf --iout=T1toMNInonlin --cout=T1toMNI_coef --fout=T1toMNI_warp

  #Invert warp:

  invwarp -r T1_filled_bet_fixed.nii.gz -w T1toMNI_warp.nii.gz -o MNItoT1_warp

else

  #To register the T1-weighted image to standard space requires the following commands to be run:

  flirt -in T1_bet_biascorr.nii.gz -ref $FSLDIR/data/standard/MNI152_T1_2mm_brain.nii.gz -dof 12 -omat T1_to_MNI.mat

  #FNIRT requires whole head (non-brain-extracted) input and reference images for optimal accuracy

  cp *t1_mpr_iso*nii* T1.nii.gz

  cp ../../../../T1_2_MNI152_2mm_lambda_change.cnf .

  fnirt --in=T1.nii.gz --aff=T1_to_MNI.mat --config=T1_2_MNI152_2mm_lambda_change.cnf --iout=T1toMNInonlin --cout=T1toMNI_coef --fout=T1toMNI_warp

  #Invert warp:

  invwarp -r T1_bet_biascorr.nii.gz -w T1toMNI_warp.nii.gz -o MNItoT1_warp

fi

#To create the corpus callosum, corticospinal tract and optic radiation ROI, enter the following command:
fslmaths $FSLDIR/data/atlases/JHU/JHU-ICBM-labels-2mm.nii.gz -thr 3 -uthr 5 Corpus_Callosum.nii.gz
fslmaths $FSLDIR/data/atlases/JHU/JHU-ICBM-labels-2mm.nii.gz -thr 7 -uthr 8 Cortico_Spinal_Tract.nii.gz
fslmaths $FSLDIR/data/atlases/JHU/JHU-ICBM-labels-2mm.nii.gz -thr 29 -uthr 30 Optic_Radiation.nii.gz


#You need to have the linear transformation matrices from T1 do desired space in order for the rest to work e.g. T1_to_b0.mat
#These two (T1_to_b0.mat and MNItoT1_warp) can now be used to bring the selected tracts into DWI and MWF space with the command
applywarp -r ../DWI/mean_b0.nii.gz -i Corpus_Callosum.nii.gz -w MNItoT1_warp.nii.gz --postmat=T1_to_b0.mat -o ../DWI/JHU_Corpus_Callosum_in_b0.nii.gz
applywarp -r ../DWI/mean_b0.nii.gz -i Cortico_Spinal_Tract.nii.gz -w MNItoT1_warp.nii.gz --postmat=T1_to_b0.mat -o ../DWI/JHU_Cortico_Spinal_Tract_in_b0.nii.gz
applywarp -r ../DWI/mean_b0.nii.gz -i Optic_Radiation.nii.gz -w MNItoT1_warp.nii.gz --postmat=T1_to_b0.mat -o ../DWI/JHU_Optic_Radiation_in_b0.nii.gz

applywarp -r ../MWF/vista_bet.nii.gz -i Corpus_Callosum.nii.gz -w MNItoT1_warp.nii.gz --postmat=T1_to_MWF.mat -o ../MWF/JHU_Corpus_Callosum_in_MWF.nii.gz
applywarp -r ../MWF/vista_bet.nii.gz -i Cortico_Spinal_Tract.nii.gz -w MNItoT1_warp.nii.gz --postmat=T1_to_MWF.mat -o ../MWF/JHU_Cortico_Spinal_Tract_in_MWF.nii.gz
applywarp -r ../MWF/vista_bet.nii.gz -i Optic_Radiation.nii.gz -w MNItoT1_warp.nii.gz --postmat=T1_to_MWF.mat -o ../MWF/JHU_Optic_Radiation_in_MWF.nii.gz



#Binarise the masks:
fslmaths ../DWI/JHU_Corpus_Callosum_in_b0.nii.gz -thr 0.7 -bin ../DWI/JHU_Corpus_Callosum_in_b0_bin.nii.gz
fslmaths ../DWI/JHU_Cortico_Spinal_Tract_in_b0.nii.gz -thr 0.7 -bin ../DWI/JHU_Cortico_Spinal_Tract_in_b0_bin.nii.gz
fslmaths ../DWI/JHU_Optic_Radiation_in_b0.nii.gz -thr 0.7 -bin ../DWI/JHU_Optic_Radiation_in_b0_bin.nii.gz

fslmaths ../MWF/JHU_Corpus_Callosum_in_MWF.nii.gz -thr 0.7 -bin ../MWF/JHU_Corpus_Callosum_in_MWF_bin.nii.gz
fslmaths ../MWF/JHU_Cortico_Spinal_Tract_in_MWF.nii.gz -thr 0.7 -bin ../MWF/JHU_Cortico_Spinal_Tract_in_MWF_bin.nii.gz
fslmaths ../MWF/JHU_Optic_Radiation_in_MWF.nii.gz -thr 0.7 -bin ../MWF/JHU_Optic_Radiation_in_MWF_bin.nii.gz

exit
