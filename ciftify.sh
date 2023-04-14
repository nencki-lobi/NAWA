#!/bin/bash
participantdir=$1

participant=$(basename $participantdir)
#run this container to run the script
#docker run -it --entrypoint /bin/bash -v /home/pjakuszyk:/home/pjakuszyk tigrlab/fmriprep_ciftify
ciftify_recon_all --ciftify-work-dir /home/pjakuszyk/FS_hcp/ --fs-subjects-dir /home/pjakuszyk/freesurfer_output/ --surf-reg FS --fs-license /home/pjakuszyk/license.txt $participant

#qc
cifti_vis_recon_all subject --ciftify-work-dir /home/pjakuszyk/FS_hcp $participant

exit
