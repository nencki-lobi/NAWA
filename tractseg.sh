#!/bin/bash
#!/bin/bash

for participantdir in `cat $1`; do

  cd $participantdir

  cd Brain/DWI

  echo "Create  participant's log file variables"

  participant=$(basename $participantdir)

  date=$(date)

  projectdir=/home/pjakuszyk/seropositive_project

  fixeldir=/home/pjakuszyk/seropositive_project/template_random/

  echo "Processing participant: $participant"

  mrtransform $fixeldir/FC_weighted_mean_voxel_smoothed/${participant}_FC_weighted_mean_smooth.mif -warp template2subject_warp.mif -interp nearest FC_native.nii.gz

  mrtransform $fixeldir/FD_sum_voxel_smoothed/${participant}_FD_sum_smooth.mif -warp template2subject_warp.mif -interp nearest FD_native.nii.gz

  mrtransform $fixeldir/FDC_sum_voxel_smoothed/${participant}_FDC_sum_smooth.mif -warp template2subject_warp.mif -interp nearest FDC_native.nii.gz

  sh2peaks wmfod_norm.mif peaks.nii.gz

  TractSeg -i peaks.nii.gz -o tractseg_output --output_type tract_segmentation

  TractSeg -i peaks.nii.gz -o tractseg_output --output_type endings_segmentation

  TractSeg -i peaks.nii.gz -o tractseg_output --output_type TOM

  Tracking -i peaks.nii.gz -o tractseg_output --nr_fibers 5000

  cd tractseg_output

  Tractometry -i TOM_trackings/ -o Tractometry_NODDI_ND.csv -e endings_segmentations/ -s ../NODDI_ficvf.nii

  Tractometry -i TOM_trackings/ -o Tractometry_fixel_FC.csv -e endings_segmentations/ -s ../FC_native.nii.gz

  Tractometry -i TOM_trackings/ -o Tractometry_fixel_FD.csv -e endings_segmentations/ -s ../FD_native.nii.gz

  Tractometry -i TOM_trackings/ -o Tractometry_fixel_FDC.csv -e endings_segmentations/ -s ../FDC_native.nii.gz

  if [[ -f Tractometry_NODDI_ND.csv && -f Tractometry_fixel_FC.csv && -f Tractometry_fixel_FD.csv && -f Tractometry_fixel_FDC.csv ]]; then

    echo "Finished tractometry for $participant on $date" >> $projectdir/TractSeg.log

  else

    echo "Something went wrong for $participant - check it manually" >> $projectdir/TractSeg.log

  fi

done

exit
