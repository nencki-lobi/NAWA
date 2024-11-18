#!/bin/bash

# Loop over participants from the input file
for participant in $(cat "$1"); do

  # Define the participant-specific directory
  cd /Volumes/Lacie2/freesurfer_output/$participant

  # Loop through hemispheres (lh = left hemisphere, rh = right hemisphere)
  for hemi in lh rh; do
    # Input log file and output CSV file
    LOGFILE="aparc_tablefile_DK_atlas_${hemi}.log"
    OUTPUT_CSV="aparc_tablefile_DK_atlas_${hemi}.csv"
    TMP_CSV="tmp_${hemi}.csv"
    TMP_CSV_2="tmp_${hemi}_2.csv"
    TMP_CSV_3="tmp_${hemi}_3.csv"
    TMP_CSV_4="tmp_${hemi}_4.csv"

    # Write the header to the output CSV file
    echo "StructName,ThickAvg" > "$TMP_CSV"

    # Use awk to extract lines that contain the structure info and format them
    awk 'NF==10 {print $1","$5}' "$LOGFILE" >> "$TMP_CSV"

    # Use sed to delete rows 2, 3, and 4
    sed '2,4d' "$TMP_CSV" > "$TMP_CSV_2"

    # Read the file and store header and values
    awk -F, '{
        if (NR == 1) {
            next; # Skip header
        } else {
            headers = headers","$1; # Collect column names from StructName
            values = values","$2;   # Collect values from ThickAvg
        }
    } 
    END {
        print substr(headers,2) > "'$TMP_CSV_3'"; # Remove leading comma, output headers
        print substr(values,2) > "'$TMP_CSV_3'";  # Remove leading comma, output values
    }' "$TMP_CSV_2"


    awk -v hemi="$hemi" 'BEGIN{FS=OFS=","} NR==1{for (i=1; i<=NF; i++) $i=hemi "_" $i}1' "$TMP_CSV_3" > "$TMP_CSV_4"

     # Read the CSV file and add the participant name as the first column
    awk -F, 'BEGIN{OFS=","} NR==1{print "Participant," $0} NR>1{print "'$participant'," $0}' "$TMP_CSV_4" >  "$OUTPUT_CSV"

    echo "CSV file created: $OUTPUT_CSV"

    done


  join -t, -1 1 -2 1 aparc_tablefile_DK_atlas_lh.csv aparc_tablefile_DK_atlas_rh.csv > combined.csv

done



find /Volumes/Lacie2/freesurfer_output -name "combined.csv" -exec head -n 1 {} \; -quit > /Volumes/Lacie2/freesurfer_output/combined_aparc_tablefile.csv
find /Volumes/Lacie2/freesurfer_output -name "combined.csv" -exec tail -n +2 {} \; >> /Volumes/Lacie2/freesurfer_output/combined_aparc_tablefile.csv