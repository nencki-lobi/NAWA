#!/bin/bash

find /home/pjakuszyk/archive/seropositive_project -type f -name "stats_basal_ganglia_NDI.csv" -exec rm {} \;

for participantdir in `cat $1`; do

    cd $participantdir
    participant=$(basename $participantdir)

    date=$(date)
    
    echo "Now processing participant $participant"
    
    cd Brain/T1
  
    if [ -e ../FLAIR/FLAIR_lesion_mask.nii.gz ]
    then

        echo "The lesion mask exists"
    
        echo "Run FSL First"
    
        run_first_all -b -a T1_to_MNI.mat -v -i T1_filled_bet_fixed.nii.gz -o basal_ganglia

    else

        echo "There is no lesion mask"
  
        echo "Run FSL First"
    
        run_first_all -b -a T1_to_MNI.mat -v -i T1_bet_biascorr.nii.gz -o basal_ganglia
    fi

    echo "Extract structures from the firstseg.nii.gz"
    fslmaths basal_ganglia_all_fast_firstseg.nii.gz -thr 9.5 -uthr 10.5 -bin left_thalamus.nii.gz
    fslmaths basal_ganglia_all_fast_firstseg.nii.gz -thr 48.5 -uthr 49.5 -bin right_thalamus.nii.gz
    
    fslmaths basal_ganglia_all_fast_firstseg.nii.gz -thr 10.5 -uthr 11.5 -bin left_caudate.nii.gz
    fslmaths basal_ganglia_all_fast_firstseg.nii.gz -thr 49.5 -uthr 50.5 -bin right_caudate.nii.gz

    fslmaths basal_ganglia_all_fast_firstseg.nii.gz -thr 11.5 -uthr 12.5 -bin left_putamen.nii.gz
    fslmaths basal_ganglia_all_fast_firstseg.nii.gz -thr 50.5 -uthr 51.5 -bin right_putamen.nii.gz

    fslmaths basal_ganglia_all_fast_firstseg.nii.gz -thr 12.5 -uthr 13.5 -bin left_pallidum.nii.gz
    fslmaths basal_ganglia_all_fast_firstseg.nii.gz -thr 51.5 -uthr 52.5 -bin right_pallidum.nii.gz

    fslmaths basal_ganglia_all_fast_firstseg.nii.gz -thr 16.5 -uthr 17.5 -bin left_hippocampus.nii.gz
    fslmaths basal_ganglia_all_fast_firstseg.nii.gz -thr 52.5 -uthr 53.5 -bin right_hippocampus.nii.gz

    fslmaths basal_ganglia_all_fast_firstseg.nii.gz -thr 17.5 -uthr 18.5 -bin left_amygdala.nii.gz
    fslmaths basal_ganglia_all_fast_firstseg.nii.gz -thr 53.5 -uthr 54.5 -bin right_amygdala.nii.gz

    fslmaths basal_ganglia_all_fast_firstseg.nii.gz -thr 25.5 -uthr 26.5 -bin left_accumbens.nii.gz
    fslmaths basal_ganglia_all_fast_firstseg.nii.gz -thr 57.5 -uthr 58.5 -bin right_accumbens.nii.gz

    echo "Register segmented structures to DWI; binarize them and extract NDI values"
    
    
    structures=("left_thalamus" "right_thalamus" "left_caudate" "right_caudate" "left_putamen" "right_putamen" "left_pallidum" "right_pallidum" "left_hippocampus" "right_hippocampus" "left_amygdala" "right_amygdala" "left_accumbens" "right_accumbens")

    ndi_values=()
    
    for structure in "${structures[@]}"
    do
        flirt -in ${structure}.nii.gz -ref ../DWI/mean_b0.nii.gz -applyxfm -init T1_to_b0.mat -out ../DWI/${structure}_in_DWI.nii.gz -interp trilinear
        fslmaths ../DWI/${structure}_in_DWI.nii.gz -thr 0.9 -bin ../DWI/${structure}_in_DWI_bin.nii.gz
        
        # Store mean neurite density in NAWM in the array
        ndi_value=$(fslstats ../DWI/NODDI_ficvf.nii.gz -k ../DWI/${structure}_in_DWI_bin.nii.gz -M)
        ndi_values+=("$ndi_value")

    done
    
    echo "participant,left_thalamus_NDI,right_thalamus_NDI,left_caudate_NDI,right_caudate_NDI,left_putamen_NDI,right_putamen_NDI,left_pallidum_NDI,right_pallidum_NDI,left_hippocampus_NDI,right_hippocampus_NDI,left_amygdala_NDI,right_amygdala_NDI,left_accumbens_NDI,right_accumbens_NDI" > stats_basal_ganglia_NDI.csv

    # Access the NDI values from the associative array and append to the CSV file
    # Access the NDI values from the array and append to the CSV file
    echo "$participant,${ndi_values[0]},${ndi_values[1]},${ndi_values[2]},${ndi_values[3]},${ndi_values[4]},${ndi_values[5]},${ndi_values[6]},${ndi_values[7]},${ndi_values[8]},${ndi_values[9]},${ndi_values[10]},${ndi_values[11]},${ndi_values[12]},${ndi_values[13]}" >> stats_basal_ganglia_NDI.csv

    #Find a file matches recursively in directory, concat them and drop duplicate headers

    cd /home/pjakuszyk/archive/seropositive_project

    find . -type f -name 'stats_basal_ganglia_NDI.csv' -exec cat {} \; > stats_combo_ndi.csv; awk '{if (!($0 in x)) {print $0; x[$0]=1} }' stats_combo_ndi.csv > stats_basal_ganglia_NDI_all.csv
            
done

exit
