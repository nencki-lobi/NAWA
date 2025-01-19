#!/bin/bash

for participantdir in `cat $1`; do

  cd $participantdir

  #Store participant id as variable

  participant=$(basename $participantdir)

  echo "Now processing participant: $participant"

  cd Brain/DWI

  ss3t_csd_beta1 dwi_denoised_unringed_preproc_unbiased_upsampled.mif ../../../../group_average_response_wm.txt wmfod.mif ../../../../group_average_response_gm.txt gm.mif  ../../../../group_average_response_csf.txt csf.mif -mask dwi_mask_upsampled.mif -force

done

exit
