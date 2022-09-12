#!/bin/bash

for participantdir in `cat $1`; do

  cd $participantdir

  echo "Create participant's stats file variables"

  participant=$(basename $participantdir)

  cd Spine/T2

  echo "Check for vertebral labeles file"

  if [ -e labels_vertebal.nii.gz ]
  then

    echo "Perform spinal cord segmentation using deep learning algorithm"

    sct_deepseg_sc -i *T2w*nii* -c t2 -ofolder deepseg -qc ../qc_spine_$participant

    echo "Register t2 image to PAM50 template"

    #remember to check if the -l says vertebral or vertebal

    sct_register_to_template -i *T2w*nii* -s deepseg/*T2w_*_seg.nii.gz -l labels_vertebal.nii.gz -c t2 -qc ../qc_spine_$participant

    echo "Warp template to subject space"

    sct_warp_template -d *T2w*nii* -w warp_template2anat.nii.gz -a 0 -qc ../qc_spine_$participant

    echo "Compute aggregate cross-sectional area (CSA) per vertebral level"

    sct_process_segmentation -i deepseg/*T2w*seg* -vert 2,3,4,5,6,7  -vertfile labels_vertebal.nii.gz -perlevel 1 -o csa_perlevel.csv;

    echo "Go to T2*-weighted data, which has good GM/WM contrast and high in-plane resolution"

    #GRE_ME

    cd ../GRE_ME

    echo "Perform cord segmentation"

    sct_deepseg_sc -i *GRE-ME*nii* -c t2s -o GRE_ME_seg.nii.gz -qc ../qc_spine_$participant

    echo "Segment gray matter"

    sct_deepseg_gm -i *GRE-ME*nii* -o GRE_ME_gmseg.nii.gz -qc ../qc_spine_$participant

    echo "Subtract GM segmentation from cord segmentation to obtain WM segmentation"

    sct_maths -i GRE_ME_seg.nii.gz -sub GRE_ME_gmseg.nii.gz -o GRE_ME_wmseg.nii.gz

    echo "Perform GM informed template registration"

    sct_register_multimodal -i ${SCT_DIR}/data/PAM50/template/PAM50_t2s.nii.gz -iseg ${SCT_DIR}/data/PAM50/template/PAM50_wm.nii.gz -d *GRE-ME*nii* -dseg GRE_ME_wmseg.nii.gz -o GRE_ME_reg.nii.gz -param step=1,type=seg,algo=rigid:step=2,type=seg,algo=bsplinesyn,slicewise=1,iter=3 -initwarp ../T2/warp_template2anat.nii.gz -initwarpinv ../T2/warp_anat2template.nii.gz -qc ../qc_spine_$participant

    echo "Rename warps for clarity"

    mv warp*PAM50_*GRE-ME*.nii.gz warp_template2t2s.nii.gz

    mv warp*GRE-ME*PAM50*.nii.gz warp_t2s2template.nii.gz

    echo "Warp template to subject space"

    sct_warp_template -d *GRE-ME*nii* -w warp_template2t2s.nii.gz -qc ../qc_spine_$participant

    echo "Compute cross-sectional area (CSA) of the gray and white matter for all slices in the volume"

    sct_process_segmentation -i GRE_ME_gmseg.nii.gz -o csa_gm.csv -angle-corr 0

    sct_process_segmentation -i GRE_ME_wmseg.nii.gz -o csa_wm.csv -angle-corr 0

    #DWI

    cd ../DWI

    echo "Merge BO volumes with the rest of data"

    sct_dmri_concat_b0_and_dwi -i *b0*nii* *DWI_2*.nii.gz -bvec *DWI*.bvec -bval *DWI*.bval -order b0 dwi -o dmri_concat.nii.gz -obval bvals_concat.txt -obvec bvecs_concat.txt

    echo "Compute mean DWI image"

    sct_maths -i dmri_concat.nii.gz -mean t -o dmri_mean.nii.gz

    echo "Segment cord on mean DWI image"

    sct_propseg -i dmri_mean.nii.gz -c dwi -qc ../qc_spine_$participant

    echo "Create mask (for subsequent cropping)"

    sct_create_mask -i dmri_mean.nii.gz -p centerline,dmri_mean_seg.nii.gz -size 35mm

    echo "Crop data for faster processing"

    sct_crop_image -i dmri_concat.nii.gz -m mask_dmri_mean.nii.gz -o dmri_crop.nii.gz

    echo "Motion correction (moco)"

    sct_dmri_moco -i dmri_crop.nii.gz -bvec bvecs_concat.txt

    echo "Register template to DWI"

    echo "Segment cord on motion-corrected mean DWI data"

    sct_deepseg_sc -i dmri_crop_moco_dwi_mean.nii.gz -c dwi -qc ../qc_spine_$participant

    echo "Perform registration"

    sct_register_multimodal -i $SCT_DIR/data/PAM50/template/PAM50_t1.nii.gz -iseg $SCT_DIR/data/PAM50/template/PAM50_cord.nii.gz -d dmri_crop_moco_dwi_mean.nii.gz -dseg dmri_crop_moco_dwi_mean_seg.nii.gz -param step=1,type=seg,algo=centermass:step=2,type=seg,algo=bsplinesyn,slicewise=1,iter=3 -initwarp ../GRE_ME/warp_template2t2s.nii.gz -initwarpinv ../GRE_ME/warp_t2s2template.nii.gz -qc ../qc_spine_$participant

    echo "Rename warps for clarity"

    mv warp_PAM50_t12dmri_crop_moco_dwi_mean.nii.gz warp_template2dmri.nii.gz

    mv warp_dmri_crop_moco_dwi_mean2PAM50_t1.nii.gz warp_dmri2template.nii.gz

    echo "Warp template"

    sct_warp_template -d dmri_crop_moco_dwi_mean.nii.gz -w warp_template2dmri.nii.gz -qc ../qc_spine_$participant

    echo "Compute DTI variables"

    sct_dmri_compute_dti -i dmri_crop_moco.nii.gz -bval bvals_concat.txt -bvec bvecs_concat.txt

    echo "Compute FA,MD,RD within the white matter for all slices"

    sct_extract_metric -i dti_FA.nii.gz -perslice 0 -method map -l 51 -o FA_in_wm_spine.csv

    sct_extract_metric -i dti_MD.nii.gz -perslice 0 -method map -l 51 -o MD_in_wm_spine.csv

    sct_extract_metric -i dti_RD.nii.gz -perslice 0 -method map -l 51 -o RD_in_wm_spine.csv

  else

  echo "There was no label file provided"

  fi

  echo "Goodbye cruel world"

done

exit
