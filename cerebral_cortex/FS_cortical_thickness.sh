#!/bin/bash

LOGFILE="/Volumes/Lacie2/freesurfer_output/cortical_thickness_logfile.log"
SUBJECTS_DIR="/Volumes/Lacie2/freesurfer_output"

# Loop over participants from the input file
for participant in $(cat "$1"); do

  # Define the participant-specific directory
  PARTICIPANT_DIR="$SUBJECTS_DIR/$participant"

  # Loop through hemispheres (lh = left hemisphere, rh = right hemisphere)
  for hemi in lh rh; do

    # Run the mris_anatomical_stats command
    sudo FREESURFER_HOME=$FREESURFER_HOME SUBJECTS_DIR=$SUBJECTS_DIR \
      mris_anatomical_stats -f "$PARTICIPANT_DIR/aparc_tablefile_DK_atlas_${hemi}.log" \
      -a "$PARTICIPANT_DIR/label/${hemi}.aparc.annot" -b "$participant" "$hemi"
    
    # Check if the command succeeded
    if [ $? -eq 0 ]; then
      echo "$(date): SUCCESS - Processed $participant $hemi successfully." >> "$LOGFILE"
    else
      echo "$(date): FAILURE - Error processing $participant $hemi." >> "$LOGFILE"
    fi

  done
done
