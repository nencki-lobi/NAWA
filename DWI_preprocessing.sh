#!/bin/bash

for participantdir in `cat $1`; do

  cd $participantdir

  cd Brain/DWI
  
  #echo "Find and rename unnecesssary files"
  
  #find . -iname "*PA*nii*" -size -1M -exec mv {} PA_unused.nii.gz \;
  
  #find . -iname "*AP*nii*" -size -1M -exec mv {} AP_unused.nii.gz \;
  
  #all_ap=(*AP*.nii*)
  #echo "${all_ap[1]}"
  #AP=(${all_ap[1]})
  AP=(*AP*nii*)
  PA=(*PA*nii*) 
  #all_pa=(*PA*.nii*)
  #PA=(${all_pa[1]})

  echo $PA

  echo "Convert AP dwi to .mif"

  mrconvert $AP dwi.mif -fslgrad *AP*.bvec *AP*.bval;

  echo "Denoise"

  dwidenoise dwi.mif dwi_den.mif -noise noise.mif;

  echo "Calculate residual from noise"

  mrcalc dwi.mif dwi_den.mif -subtract residual.mif;

  echo "Get rid of the Gibbs ringing artefact"

  mrdegibbs dwi_den.mif dwi_den_unr.mif;

  echo "Convert PA to .mif"

  mrconvert $PA PA.mif;

  echo "Create mean b0 image from PA direction"

  mrconvert PA.mif -fslgrad *PA*.bvec *PA*.bval - | mrmath - mean mean_b0_PA.mif -axis 3;

  echo "Extract mean b0 image drom AP direction"

  dwiextract dwi_den_unr.mif - -bzero | mrmath - mean mean_b0_AP.mif -axis 3;

  echo "Concat mean b0 images from both phase encoding directions"

  mrcat mean_b0_AP.mif mean_b0_PA.mif -axis 3 b0_pair.mif;

  echo "Preprocess the DWI data (topup, eddy, QC)"

  dwifslpreproc dwi_den_unr.mif dwi_den_preproc.mif -nocleanup -pe_dir AP -rpe_pair -se_epi b0_pair.mif -eddyqc_all eddy_qc -eddy_options "--slm=linear  --data_is_shelled --repol --residuals --cnr_maps";

  echo "Perform bias field correction on the preprocessed data"

  dwibiascorrect ants *_preproc.mif den_preproc_unbiased.mif -bias bias.mif

  echo "Create a binary brain mask neede for futher analysis"

  dwi2mask den_preproc_unbiased.mif mask.mif

  echo "Extract b-shell close to a 1000 to estimate a diffusion tensor model"

  dwiextract -shell 0,1250 den_preproc_unbiased.mif dwi_bval1245-55.mif

  echo "Sleep for 5s to wait for the dwi_bval1245-55.mif file to fully take shape"

  sleep 5s

  echo "Create a DTI image"

  dwi2tensor -mask mask.mif dwi_bval1245-55.mif DTI.nii.gz

  echo "Extract FA, MD and RD from the DTI image"

  tensor2metric -fa FA.nii.gz -rd RD.nii.gz -adc MD.nii.gz DTI.nii.gz

  echo "Extract a mean B0 image from the preprocessed data (useful for registration)"

  dwiextract den_preproc_unbiased.mif - -bzero | mrmath - mean mean_b0.mif -axis 3

  echo "Convert this mean b0 image to nifti"

  mrconvert mean_b0.mif mean_b0.nii.gz

  echo "Convert brain mask file to nifti. Useful to restrict model fit only to selected voxels (NODDI)."
  mrconvert mask.mif mask.nii

  echo "Convert preprocessed DWI image to nifti and extract bvals and bvecs (NODDI)"
  mrconvert den_preproc_unbiased.mif den_preproc_unbiased.nii -export_grad_fsl den_preproc_unbiased.bvec den_preproc_unbiased.bval

done

exit



