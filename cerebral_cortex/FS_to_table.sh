#!/bin/bash

#mri_segstats --sum & asegstats2table --meas=mean
#Left hemi
ls -d * | xargs -I {} singularity exec /opt/software/bids_freesurfer.simg mri_segstats --annot {} lh aparc.a2009s --i {}/surf/lh.smoothedR1.mgh --sum {}/stats/lh.aparc.a2009s.qR1.stats
 singularity exec /opt/software/bids_freesurfer.simg asegstats2table --statsfile=lh.aparc.a2009s.qR1.stats --subjects $(cat mp2rage_list.txt) --tablefile lh.aparc.a2009s.qR1.csv --meas=mean --skip --all-segs --delimiter comma

#Right hemi
ls -d * | xargs -I {} singularity exec /opt/software/bids_freesurfer.simg mri_segstats --annot {} rh aparc.a2009s --i {}/surf/rh.smoothedR1.mgh --sum {}/stats/rh.aparc.a2009s.qR1.stats
 singularity exec /opt/software/bids_freesurfer.simg asegstats2table --statsfile=rh.aparc.a2009s.qR1.stats --subjects $(cat mp2rage_list.txt) --tablefile rh.aparc.a2009s.qR1.csv --meas=mean --skip --all-segs --delimiter comma

#modify column prefixes
sed '1s/[^,]*/rh_&/g' rh.aparc.a2009s.qR1.csv > rh.aparc.a2009s.qR1_changed_column_names.csv
sed '1s/[^,]*/lh_&/g' lh.aparc.a2009s.qR1.csv > lh.aparc.a2009s.qR1_changed_column_names.csv

#merge two csv files
awk 'BEGIN{FS=OFS=","} NR==1 {$1="participant"} 1' rh.aparc.a2009s.qR1_changed_column_names.csv > rh.aparc.a2009s.qR1_changed_column_names_1.csv
awk 'BEGIN{FS=OFS=","} NR==1 {$1="participant"} 1' lh.aparc.a2009s.qR1_changed_column_names.csv > lh.aparc.a2009s.qR1_changed_column_names_1.csv

join -t ',' -1 1 -2 1 -a 1 -a 2 -o auto lh.aparc.a2009s.qR1_changed_column_names_1.csv  rh.aparc.a2009s.qR1_changed_column_names_1.csv > R1_merged.csv
