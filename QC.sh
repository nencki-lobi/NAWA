#!/bin/bash

#Registration from template quality check

for i in `cat participant_list.txt`; do
    echo "Current participant : ${i}"
    fsleyes participants/${i}/Brain/DWI/mean_b0.nii.gz -cm greyscale participants/${i}/Brain/DWI/JHU_Corpus_Callosum_in_b0_NAWM_masked.nii.gz -cm red -a 100.0 participants/${i}/Brain/DWI/JHU_Cortico_Spinal_Tract_in_b0_NAWM_masked.nii.gz -cm blue -a 100.0  participants/${i}/Brain/DWI/JHU_Optic_Radiation_in_b0_NAWM_masked.nii.gz -cm green -a 100.0 &
    printf 'Press Enter to continue'
    read REPLY
done


#Registration from masks quality check

for i in `cat participant_list.txt`; do
  echo "Current participant : ${i}"
  if [ -e participants/${i}/Brain/FLAIR/FLAIR_lesion_mask.nii.gz ]
  then
    fsleyes participants/${i}/Brain/DWI/mean_b0.nii.gz -cm greyscale participants/${i}/Brain/DWI/NAWM_in_DWI_masked.nii.gz -cm blue -a 100.0 participants/${i}/Brain/DWI/lesions_in_DWI_masked.nii.gz -cm red -a 100.0 &
    fsleyes participants/${i}/Brain/MWF/vista3D.nii -cm greyscale participants/${i}/Brain/MWF/NAWM_in_MWF_masked.nii.gz -cm blue -a 100.0 participants/${i}/Brain/MWF/lesions_in_MWF_masked.nii.gz -cm red -a 100.0 &
    printf 'Press Enter to continue'
    read REPLY
  else
    fsleyes participants/${i}/Brain/DWI/mean_b0.nii.gz -cm greyscale participants/${i}/Brain/DWI/NAWM_in_DWI_masked.nii.gz -cm blue -a 100.0 &
    fsleyes participants/${i}/Brain/MWF/vista3D.nii -cm greyscale participants/${i}/Brain/MWF/NAWM_in_MWF_masked.nii.gz -cm blue -a 100.0 &
    printf 'Press Enter to continue'
    read REPLY
  fi
done
