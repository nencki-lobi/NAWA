#!/bin/bash

projectdir=/home/pjakuszyk/seropositive_project

mkdir $projectdir/bids

for i in `cat participant_list.txt`; do
    echo "Current participant : ${i}"

    if [ -e $projectdir/participants/${i}/Brain/MP2RAGE/*mp2rage_offline*nii* ]; then

    mkdir -p $projectdir/bids/${i}/anat

    participantdir=$projectdir/participants/${i}/Brain/MP2RAGE/hostrecon_XX/presurf_MPRAGEise

    cp $participantdir/UNI_corrected_MPRAGEised.nii $projectdir/bids/${i}/anat/${i}_T1w.nii

    gzip $projectdir/bids/${i}/anat/${i}_T1w.nii

    else

    echo "$i does not have an MP2RAGE image"

    fi

done
