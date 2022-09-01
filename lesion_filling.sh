#!/bin/bash

participantdir=$1

cd $participantdir

echo "Store participant id as variable"

participant=$(basename $participantdir)

echo "Now processing participant: $participant"

cd Brain/FLAIR

echo "Brain extract FLAIR"

bet *spc_da-fl*.nii* FLAIR_bet.nii.gz -f 0.4 -R

cd ../T1

echo "Brain extract and perform bias field correction on T1"

bet *t1_mpr_iso_*.nii* T1_bet_biascorr.nii.gz -f 0.4 -B -R

echo "Register FLAIR to T1"

cd ../FLAIR

flirt -in FLAIR_bet.nii.gz -ref ../T1/T1_bet_biascorr.nii.gz -out ../T1/FLAIR_in_T1 -omat ../T1/FLAIR_to_T1.mat -dof 12 -cost normmi

echo "Check for lesion mask to determine whether lesion filling is needed"

if [ -e FLAIR_lesion_mask.nii.gz ]
then

    echo "The lesion mask exists"

    echo "Use the obtained transformation matrix to register FLAIR lesion mask to T1"

    flirt -in FLAIR_lesion_mask.nii.gz -ref ../T1/T1_bet_biascorr.nii.gz -out ../T1/FLAIR_lesion_mask_in_T1.nii.gz -init ../T1/FLAIR_to_T1.mat -applyxfm -interp nearestneighbour

    cd ../T1

    echo "Segment white matter from T1 to get white matter mask"

    fast T1_bet_biascorr.nii.gz

    fslmaths T1_bet_biascorr_pve_2.nii.gz -thr 0.95 -bin WM_mask_not_lesion_filled.nii.gz

    #echo "Make sure the lesions in the mask are within white matter mask, because otherwise it is all fucked up" - maybe not

    #fslmaths FLAIR_lesion_mask_in_T1.nii.gz -mas WM_mask_not_lesion_filled.nii.gz FLAIR_lesion_mask_in_T1_NAWM_restricted.nii.gz

    echo "Use the lesion mask to perform the T1 lesion filling"

    lesion_filling -i *t1_mpr_iso_*.nii* -l FLAIR_lesion_mask_in_T1.nii.gz -w WM_mask_not_lesion_filled.nii.gz -o T1_filled_fixed.nii.gz

    lesion_filling -i T1_bet_biascorr.nii.gz -l FLAIR_lesion_mask_in_T1.nii.gz -w WM_mask_not_lesion_filled.nii.gz -o T1_filled_bet_fixed.nii.gz

else

    echo "There is no lesion mask"

fi

echo "Goodbye cruel world"

exit
