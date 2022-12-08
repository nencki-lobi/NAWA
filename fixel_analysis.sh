#!/bin/bash

sudo docker run -v /home/pjakuszyk/:/home/pjakuszyk/ -it vnmd/mrtrix3tissue_5.2.8

#with the 3tissue container we get the ss3t_csd_beta1 command to use single shell 3 tissue deconvolution, however in this container instead of 'for_each' command is changed to  'foreach'.

#Get oout of the work folder and into the project's folder

cd ../home/pjakuszyk/seropositive_project/participants

#This forum post is very important as to why we are using multi tissue pipline and 2 shell (0 and 2500) with SS3T-CSD - https://3tissue.github.io/doc/ss3t-csd.html
#https://community.mrtrix.org/t/single-shell-vs-single-tissue/5761/7

#Computing (average) tissue response functions

foreach * : dwi2response dhollander IN/Brain/DWI/dwi_singleshell_2500.mif IN/Brain/DWI/response_wm.txt IN/Brain/DWI/response_gm.txt IN/Brain/DWI/response_csf.txt

#Average the response functions obtained from all subjects for each tissue type:

responsemean */Brain/DWI/response_wm.txt ../group_average_response_wm.txt
responsemean */Brain/DWI/response_gm.txt ../group_average_response_gm.txt
responsemean */Brain/DWI/response_csf.txt ../group_average_response_csf.txt

#Upsampling DW images

foreach * : mrgrid IN/Brain/DWI/dwi_singleshell_2500.mif regrid -vox 1.25 IN/Brain/DWI/dwi_denoised_unringed_preproc_unbiased_upsampled.mif

#Compute a whole brain mask from the upsampled DW images:

foreach * : dwi2mask IN/Brain/DWI/dwi_denoised_unringed_preproc_unbiased_upsampled.mif IN/Brain/DWI/dwi_mask_upsampled.mif

#Fibre Orientation Distribution estimation (multi-tissue single shell spherical deconvolution)

foreach * : ss3t_csd_beta1 IN/Brain/DWI/dwi_denoised_unringed_preproc_unbiased_upsampled.mif ../../../../group_average_response_wm.txt IN/Brain/DWI/wmfod.mif ../../../../group_average_response_gm.txt IN/Brain/DWI/gm.mif  ../../../../group_average_response_csf.txt IN/Brain/DWI/csf.mif -mask IN/Brain/DWI/dwi_mask_upsampled.mif -force

#Joint bias field correction and intensity normalisation

foreach * : mtnormalise IN/Brain/DWI/wmfod.mif IN/Brain/DWI/wmfod_norm.mif IN/Brain/DWI/gm.mif IN/Brain/DWI/gm_norm.mif IN/Brain/DWI/csf.mif IN/Brain/DWI/csf_norm.mif -mask IN/Brain/DWI/dwi_mask_upsampled.mif

#Generate a study-specific unbiased FOD template
#Typically, subjects are chosen so the generated template is representative of your population (e.g. similar number of patients and controls,
#though avoid patients with excessive abnormalities compared to the rest of the population).
#To build a template, put all FOD images in a single folder and put a set of corresponding mask images
#(with the same prefix as the FOD images) in another folder (using masks speeds up registration significantly):

mkdir -p ../template_test/fod_input
mkdir ../template_test/mask_input

#So I will manually choose 10 participants from each group for the template. I will avoid all the participants (especially MS subjects) with excessive WM lesion load.
#names of the participants to keep for the template are stored in participatnt_list_fixel_template.txt

#Fist create symbolic link to all participants
foreach * : ln -sr IN/Brain/DWI/wmfod_norm.mif ../template/fod_input/PRE.mif
foreach * : ln -sr IN/Brain/DWI/dwi_mask_upsampled.mif ../template/mask_input/PRE.mif

#Find recursively an remove participants for fixel template
for i in `cat participant_list_fixel_template.txt`; do
    find /home/pjakuszyk/seropositive_project/template -maxdepth 3  -name ${i}.mif -exec rm -rf {} \;
done

#Run the template building script as follows:

population_template template/fod_input -mask_dir template/mask_input template/wmfod_template.mif -voxel_size 1.25

#Register the FOD image from each subject to the FOD template:

foreach * : mrregister IN/Brain/DWI/wmfod_norm.mif -mask1 IN/Brain/DWI/dwi_mask_upsampled.mif ../template/wmfod_template.mif -nl_warp IN/Brain/DWI/subject2template_warp.mif IN/Brain/DWI/template2subject_warp.mif

#Compute the template mask (intersection of all subject masks in template space)
#To warp all masks into template space:

foreach * : mrtransform IN/Brain/DWI/dwi_mask_upsampled.mif -warp IN/Brain/DWI/subject2template_warp.mif -interp nearest -datatype bit IN/Brain/DWI/dwi_mask_in_template_space.mif

#Compute the template mask as the intersection of all warped masks:

mrmath */Brain/DWI/dwi_mask_in_template_space.mif min ../template/template_mask.mif -datatype bit

#Compute a white matter template analysis fixel mask

fod2fixel -mask ../template/template_mask.mif -fmls_peak_value 0.06 ../template/wmfod_template.mif ../template/fixel_mask

#You can manipulate the peak value threshold to obtain more fixels but be careful, to not get false positives
#You can check the number of fixels with:
mrinfo -size ../template/fixel_mask/directions.mif
#It should contain several hundreds of thousands of fixels

#Warp FOD images to template space without FOD reorientation, as reorientation will be performed in a separate subsequent step (after fixel segmentation):

foreach * : mrtransform IN/Brain/DWI/wmfod_norm.mif -warp IN/Brain/DWI/subject2template_warp.mif -noreorientation IN/Brain/DWI/fod_in_template_space_NOT_REORIENTED.mif

#Here we segment each FOD lobe to identify the number and orientation of fixels in each voxel. The output also contains the apparent fibre density (AFD) value per fixel (estimated as the FOD lobe integral):

foreach * : fod2fixel -mask ../template/template_mask.mif IN/Brain/DWI/fod_in_template_space_NOT_REORIENTED.mif IN/Brain/DWI/fixel_in_template_space_NOT_REORIENTED -afd fd.mif

#Here we reorient the fixels of all subjects in template space based on the local transformation at each voxel in the warps used previously:

foreach * : fixelreorient IN/Brain/DWI/fixel_in_template_space_NOT_REORIENTED IN/Brain/DWI/subject2template_warp.mif IN/Brain/DWI/fixel_in_template_space

#Assign subject fixels to template fixels

foreach * : fixelcorrespondence IN/Brain/DWI/fixel_in_template_space/fd.mif ../template/fixel_mask ../template/fd PRE.mif

#Compute the fibre cross-section (FC) metric

foreach * : warp2metric IN/Brain/DWI/subject2template_warp.mif -fc ../template/fixel_mask ../template/fc IN.mif

#However, for group statistical analysis of FC we recommend calculating the log(FC) to ensure data are centred around zero and normally distributed. Here, we create a separate fixel directory to store the log(FC) data and copy the fixel index and directions file across:

mkdir ../template/log_fc
cp ../template/fc/index.mif ../template/fc/directions.mif ../template/log_fc
foreach * : mrcalc ../template/fc/IN.mif -log ../template/log_fc/IN.mif

#Compute a combined measure of fibre density and cross-section (FDC)

mkdir ../template/fdc
cp ../template/fc/index.mif ../template/fdc
cp ../template/fc/directions.mif ../template/fdc
foreach * : mrcalc ../template/fd/IN.mif ../template/fc/IN.mif -mult ../template/fdc/IN.mif

#Perform whole-brain fibre tractography on the FOD template

cd ../template
tckgen -angle 22.5 -maxlen 250 -minlen 10 -power 1.0 wmfod_template.mif -seed_image template_mask.mif -mask template_mask.mif -select 20000000 -cutoff 0.06 tracks_20_million.tck

#Perform SIFT to reduce tractography biases in the whole-brain tractogram:

tcksift tracks_20_million.tck wmfod_template.mif tracks_2_million_sift.tck -term_number 2000000

#Generation of the fixel-fixel connectivity matrix based on the whole-brain streamlines tractogram is performed as follows:
#For this you have to change the container to mrtrix3/mrtrix3 because the 3tss software verison does not contain the fixelconnectivity command

fixelconnectivity fixel_mask/ tracks_2_million_sift.tck matrix/

#Smoothing of fixel data is performed based on the sparse fixel-fixel connectivity matrix:

fixelfilter fd smooth fd_smooth -matrix matrix/
fixelfilter log_fc smooth log_fc_smooth -matrix matrix/
fixelfilter fdc smooth fdc_smooth -matrix matrix/

#Statistical analysis using CFE is performed separately for each metric (FD, log(FC), and FDC) as follows:

######FD######
#HC - SM
fixelcfestats fd_smooth/ files.txt design_matrix.txt HC_SM_contrast.txt matrix/ stats_fd_HC_SM/

fixelcfestats fd_smooth/ files_HC_SM.txt design_matrix_HC_SM.txt contrast_HC_SM_2.txt matrix/ stats_fd_HC_SM_2/ -nshuffles 500

#SM - HC
fixelcfestats fd_smooth/ files.txt design_matrix.txt SM_HC_contrast.txt matrix/ stats_fd_SM_HC/
#HC - AQP4
fixelcfestats fd_smooth/ files.txt design_matrix.txt HC_AQP4_contrast.txt matrix/ stats_fd_HC_AQP4/
#AQP4 - SM
fixelcfestats fd_smooth/ files.txt design_matrix.txt AQP4_SM_contrast.txt matrix/ stats_fd_AQP4_SM/


#####FC########
#HC - SM
fixelcfestats log_fc_smooth/ files.txt design_matrix.txt HC_SM_contrast.txt matrix/ stats_log_fc_HC_SM/ -nshuffles 500


######FDC#######
#HC - SM
fixelcfestats fdc_smooth/ files.txt design_matrix.txt HC_SM_contrast.txt matrix/ stats_fdc_HC_SM/ -nshuffles 500

#HC - AQP4
fixelcfestats fdc_smooth/ files.txt design_matrix.txt HC_AQP4_contrast.txt matrix/ stats_fdc_HC_AQP4/ -nshuffles 500

#AQP4-SM
fixelcfestats fdc_smooth/ files.txt design_matrix.txt AQP4_SM_contrast.txt matrix/ stats_fdc_AQP4_SM/ -nshuffles 500

#To calculate percentage decrease effect size for FC, FDC
#If there is a column in the design matrix that contains the value 1 for all subjects in the control group and 0 for all other subjects, and if any & all nuisance regressors were de-meaned
#prior to inserting them into the design matrix, then the relevant beta coefficient image provided by fixelcfestats (e.g. stats_fd/beta0.mif) can be interpreted directly as the control group mean.

mrcalc stats_fdc_HC_SM/abs_effect.mif stats_fdc_HC_SM/beta0.mif -div 100 -mult stats_fdc_HC_SM/percentage_effect.mif


##Make max FD per voxel
for_each * : fixel2voxel IN max fd_max/IN

for_each * : mrconvert IN PRE.nii.gz

mrregister  /usr/local/fsl/data/standard/FSL_HCP1065_FA_1mm.nii.gz -nl_warp template2standard_warp.mif standard2template_warp.mif

mrtransform  /usr/local/fsl/data/ -warp Istandard2template_warp.mif atlas_in_fod_template.nii.gz

echo "participant,fd_max" > stats_fd_max.csv
for i in `cat ../../../participant_list.txt`; do
    echo "Current participant : ${i}"
    participant=${i}
    fd_max=$(fslstats ${i}_noNAN.nii.gz -k ../../template2atlas/CC_in_fod_template_bin.nii.gz -M)
    echo "$participant,$fd_max" >> stats_fd_max.csv
done





#https://community.mrtrix.org/t/what-does-fixelcfestats-exactly-do/2052
