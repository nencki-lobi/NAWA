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

  cd tractseg_output

  Tractometry -i TOM_trackings_NAWM/ -o Tractometry_NAWM_NODDI_ND.csv -e endings_segmentations/ -s ../NODDI_ficvf.nii

  if [ -f Tractometry_NAWM_NODDI_ND.csv ]; then

    echo "Finished tractometry for $participant on $date" >> $projectdir/TractSeg_NAWM.log

  else

    echo "Something went wrong for $participant - check it manually" >> $projectdir/TractSeg_NAWM.log

  fi

done

exit
