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





dwiextract -shell 0,2500 den_preproc_unbiased.mif dwi_singleshell_2500.mif


for_each study/* : dwidenoise IN/dwi.mif IN/dwi_denoised.mif

for_each home/pjakuszyk/seropositive_project/participants/*/Brain/DWI -nthreads 2 -test : dwiextract -shell 0,2500 IN/den_preproc_unbiased.mif IN/dwi_singleshell_2500.mif

for_each * -nthreads 2 : dwiextract -shell 0,2500 IN/Brain/DWI/den_preproc_unbiased.mif IN/Brain/DWI/dwi_singleshell_2500.mif


for i in `cat participant_list.txt`; do
    echo "Current participant : ${i}"
    cd participants/${i}/Brain/DWI
    dwiextract -shell 0,2500 den_preproc_unbiased.mif dwi_singleshell_2500.mif
    cd ../../../../
done
