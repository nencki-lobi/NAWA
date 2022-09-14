#!/bin/bash
for participantdir in `cat $1`; do

  cd $participantdir

  echo "Create participant's stats file variables"

  participant=$(basename $participantdir)

  date=$(date)

  echo "Processing participant: $participant"

  cd Brain/MWF

  echo "Register VISTA to T1"

  fslcpgeom *ViSTa_REF_2mm*.nii* vista3D.nii

  bet *ViSTa_REF_2mm*.nii* MWF_ref_bet.nii.gz  -f 0.5 -m

  fslmaths vista3D.nii -mas MWF_ref_bet_mask.nii.gz vista_bet.nii.gz

  flirt -in vista_bet.nii.gz -ref ../T1/T1_bet_biascorr.nii.gz -out ../T1/MWF_to_T1.nii.gz -omat ../T1/MWF_to_T1.mat -dof 6 -cost normmi

  echo "Create an inverse transformation matrix to bring images from T1 to VISTA"

  cd ../T1

  convert_xfm -omat T1_to_MWF.mat -inverse MWF_to_T1.mat

  echo "Register DWI mean b0 to T1"

  cd ../DWI

  flirt -in mean_b0.nii.gz -ref ../T1/T1_bet_biascorr.nii.gz -out ../T1/b0_in_T1.nii.gz -omat ../T1/b0_to_T1.mat -dof 6 -cost normmi

  echo "Create an inverse transformation matrix to bring images from T1 to b0"

  cd ../T1

  convert_xfm -omat T1_to_b0.mat -inverse b0_to_T1.mat

  echo "Check for lesion mask"

  cd ../FLAIR

  if [ -e FLAIR_lesion_mask.nii.gz ]
  then

      cd ../T1

      echo "The lesion mask exists"

      echo "Segment the T1 lesion filled image to obtain white matter (WM) mask"

      fast T1_filled_bet_fixed.nii.gz

      fslmaths T1_filled_bet_fixed_pve_2.nii.gz -thr 0.95 -bin WM_mask.nii.gz

      echo "Bring WM mask to DWI"

      flirt -in WM_mask.nii.gz  -ref ../DWI/mean_b0.nii.gz -applyxfm -init T1_to_b0.mat -out ../DWI/WM_mask_in_DWI.nii.gz -interp trilinear

      echo "Binarize white matter mask with a large threshold to avoid partial volume effect"

      fslmaths ../DWI/WM_mask_in_DWI.nii.gz -thr 0.7 -bin ../DWI/WM_mask_in_DWI_bin.nii.gz

      echo "Bring WM mask to MWF"

      flirt -in WM_mask.nii.gz  -ref ../MWF/vista_bet.nii.gz -applyxfm -init T1_to_MWF.mat -out ../MWF/WM_mask_in_MWF.nii.gz -interp trilinear

      echo "Binarize white matter  mask with a large threshold to avoid partial volume effect"

      fslmaths ../MWF/WM_mask_in_MWF.nii.gz -thr 0.7 -bin ../MWF/WM_mask_in_MWF_bin.nii.gz

      echo "Bring lesion mask to DWI"

      convert_xfm -omat FLAIR_to_b0.mat -concat T1_to_b0.mat FLAIR_to_T1.mat

      flirt -in ../FLAIR/FLAIR_lesion_mask.nii.gz  -ref ../DWI/mean_b0.nii.gz -applyxfm -init FLAIR_to_b0.mat -out ../DWI/lesions_in_b0.nii.gz -interp trilinear

      echo "Binarize lesion mask with a low threshold to include partial volume edges"

      fslmaths ../DWI/lesions_in_b0.nii.gz -thr 0.3 -bin ../DWI/lesions_in_b0_bin.nii.gz

      echo "Restrict lesion mask to brain mask in DWI"

      fslmaths ../DWI/lesions_in_b0_bin.nii.gz -mas ../DWI/mask.nii ../DWI/lesions_in_DWI_masked.nii.gz

      echo "Bring lesion mask to MWF"

      convert_xfm -omat FLAIR_to_MWF.mat -concat T1_to_MWF.mat FLAIR_to_T1.mat

      flirt -in ../FLAIR/FLAIR_lesion_mask.nii.gz  -ref ../MWF/vista_bet.nii.gz -applyxfm -init FLAIR_to_MWF.mat -out ../MWF/lesions_in_MWF.nii.gz -interp trilinear

      echo "Binarize lesion mask with a low threshold to include partial volume edges"

      fslmaths ../MWF/lesions_in_MWF.nii.gz -thr 0.3 -bin ../MWF/lesions_in_MWF_bin.nii.gz

      echo "Restrict lesion mask to brain mask in MWF"

      fslmaths ../MWF/lesions_in_MWF_bin.nii.gz -mas ../MWF/MWF_ref_bet_mask.nii.gz ../MWF/lesions_in_MWF_masked.nii.gz

      echo "Calculate and store DTI, NODDI and MWF values for the lesioned WM"

      cd ../DWI

      echo "Store mean fractional anisotropy in lesioned WM in a variable"

      FA_lesions=$(fslstats FA.nii.gz -k lesions_in_DWI_masked.nii.gz -M)

      echo "Store mean mean diffusivity in lesioned WM in a variable"

      MD_lesions=$(fslstats MD.nii.gz -k lesions_in_DWI_masked.nii.gz -M)

      echo "Store mean radial diffusivity in lesioned WM in a variable"

      RD_lesions=$(fslstats RD.nii.gz -k lesions_in_DWI_masked.nii.gz -M)

      echo "Store mean neurite density in lesioned WM in a variable"

      ND_lesions=$(fslstats NODDI_ficvf.nii -k lesions_in_DWI_masked.nii.gz -M)

      echo "Store mean orientation dispertion index in lesioned WM in a variable"

      ISO_lesions=$(fslstats NODDI_fiso.nii -k lesions_in_DWI_masked.nii.gz -M)

      echo "Store mean orientation dispertion in lesioned WM in a variable"

      ODI_lesions=$(fslstats NODDI_odi.nii -k lesions_in_DWI_masked.nii.gz -M)

      cd ../MWF

      echo "Store mean apparent myelin water fraction in lesioned WM"

      aMWF_lesions=$(fslstats vista3D.nii -k lesions_in_MWF_masked.nii.gz -M)

      echo "Subtract lesion mask from white matter mask to create NAWM (DWI, WMF)"

      fslmaths lesions_in_MWF_bin.nii.gz -binv -mul WM_mask_in_MWF_bin.nii.gz NAWM_in_MWF.nii.gz

      cd ../DWI

      fslmaths lesions_in_b0_bin.nii.gz -binv -mul WM_mask_in_DWI_bin.nii.gz NAWM_in_DWI.nii.gz

  else

      echo "There is no lesion mask"

      cd ../T1

      echo "Segment the T1 image"

      #fast T1_bet_biascorr.nii.gz

      #fslmaths T1_bet_biascorr_pve_2.nii.gz -thr 0.95 -bin NAWM_mask.nii.gz

      echo "Bring NAWM mask to DWI"

      flirt -in NAWM_mask.nii.gz  -ref ../DWI/mean_b0.nii.gz -applyxfm -init T1_to_b0.mat -out ../DWI/NAWM_in_DWI.nii.gz -interp trilinear

      echo "Binarize white matter mask with a large threshold to avoid partial volume effect"

      fslmaths ../DWI/NAWM_in_DWI.nii.gz -thr 0.7 -bin ../DWI/NAWM_in_DWI_bin.nii.gz

      echo "Bring NAWM mask to MWF"

      flirt -in NAWM_mask.nii.gz  -ref ../MWF/vista_bet.nii.gz -applyxfm -init T1_to_MWF.mat -out ../MWF/NAWM_in_MWF.nii.gz -interp trilinear

      echo "Binarize white matter  mask with a large threshold to avoid partial volume effect"

      fslmaths ../MWF/NAWM_in_MWF.nii.gz -thr 0.7 -bin ../MWF/NAWM_in_MWF_bin.nii.gz

      echo "Create empty variables for healthy participants"

      FA_lesions=""

      MD_lesions=""

      RD_lesions=""

      ND_lesions=""

      ISO_lesions=""

      ODI_lesions=""

      aMWF_lesions=""

  fi

  cd ../DWI

  echo "Restrict NAWM mask to brain mask in DWI"

  fslmaths NAWM_in_DWI.nii.gz -mas mask.nii NAWM_in_DWI_masked.nii.gz

  echo "Calculate and store DTI, NODDI and MWF values for the NAWM"

  echo "Store mean fractional anisotropy in NAWM in a variable"

  FA_NAWM=$(fslstats FA.nii.gz -k NAWM_in_DWI_masked.nii.gz -M)

  echo "Store mean mean diffusivity in NAWM in a variable"

  MD_NAWM=$(fslstats MD.nii.gz -k NAWM_in_DWI_masked.nii.gz -M)

  echo "Store mean radial diffusivity in NAWM in a variable"

  RD_NAWM=$(fslstats RD.nii.gz -k NAWM_in_DWI_masked.nii.gz -M)

  echo "Store mean neurite density in NAWM in a variable"

  ND_NAWM=$(fslstats NODDI_ficvf.nii -k NAWM_in_DWI_masked.nii.gz -M)

  echo "Store mean orientation dispersion index in NAWM in a variable"

  ODI_NAWM=$(fslstats NODDI_odi.nii -k NAWM_in_DWI_masked.nii.gz -M)

  echo "Store mean isotropic water component in NAWM in a variable"

  ISO_NAWM=$(fslstats NODDI_fiso.nii -k NAWM_in_DWI_masked.nii.gz -M)

  cd ../MWF

  echo "Restrict NAWM mask to brain mask in MWF"

  fslmaths NAWM_in_MWF.nii.gz -mas MWF_ref_bet_mask.nii.gz NAWM_in_MWF_masked.nii.gz

  echo "Store mean apparent myelin water fraction in NAWM in a variable"

  aMWF_NAWM=$(fslstats vista3D.nii -k NAWM_in_MWF_masked.nii.gz -M)

  cd ../../

  echo "Make a stats csv file"

  echo "participant,date,FA_lesions,MD_lesions,RD_lesions,ND_lesions,ODI_lesions,ISO_lesions,aMWF_lesions,FA_NAWM,MD_NAWM,RD_NAWM,ND_NAWM,ODI_NAWM,ISO_NAWM,aMWF_NAWM" > stats.csv

  echo "$participant,$date,$FA_lesions,$MD_lesions,$RD_lesions,$ND_lesions,$ODI_lesions,$ISO_lesions,$aMWF_lesions,$FA_NAWM,$MD_NAWM,$RD_NAWM,$ND_NAWM,$ODI_NAWM,$ISO_NAWM,$aMWF_NAWM" >> stats.csv

done

echo "Create a csv file with all the necessary stats"

echo "Find a file matches recursively in directory, concat them and drop duplicate headers:"

cd /home/pjakuszyk/seropositive_project

find /home/pjakuszyk/seropositive_project -type f -name 'stats.csv' -exec cat {} \; > stats_combo.csv; awk '{if (!($0 in x)) {print $0; x[$0]=1} }' stats_combo.csv > aMWF_DTI_NODDI_stats_nice.csv

exit
