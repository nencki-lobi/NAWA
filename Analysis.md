Helpful UNIX shit
=================

To create multiple sub-folders
------------------------------

mkdir -p parentfolder/{subfolder1,subfolder2,subfolder3}

**mkdir -p
Subject/{Brain/{T1,SWI,DWI,FLAIR,PSIR,QSM,MWF,MP2RAGE},Spine/{T1,T2,T2_nice,DWI,GRE_ME}}**

\#\#Set function for creating pilot directory

**make() {mkdir -p \$/{Brain/{T1,subject
SWI,DWI,FLAIR,PSIR,QSM,MWF,MP2RAGE},Spine/{T1,T2,T2_nice,DWI,GRE_ME}};}**

\#copy converted nifti files into specific directories:

copynii () {cp /Users/paweljakuszyk/Desktop/Pilots/\$dcm}

Convert all participants dicom to nii.gz and copy them to the participants folder:
----------------------------------------------------------------------------------

**dcm2niix -o
/Users/paweljakuszyk/Desktop/NAWA_PARTICIPANTS/004_NMO_M\_TP1 -z y -d 9
/Users/paweljakuszyk/Desktop/NAWA_dicom/004_NMO_M\_TP1/ &**

Remove all scout, localizer and .json files:
--------------------------------------------

When inside the subjects folder:

**rm \*.json; rm \*Scout\*; rm \*ocalizer\*;**

Move files to their destination directories:
--------------------------------------------

When inside the subjects folder:

**mv \*QSM\*.nii.gz Brain/QSM**; **mv \*swi\*.nii.gz Brain/SWI; mv
\*diff\* Brain/DWI; mv \*t1_mpr_iso\* Brain/T1; mv \*spc_da-fl\*
Brain/FLAIR; mv \*spc_ir\* Brain/PSIR; mv \*DWI\* Spine/DWI; mv
\*GRE-ME\* Spine/GRE_ME; mv \*GRE-T1w\* Spine/GRE_T1w; mv \*T1w\*
Spine/T1; mv \*T2w\* Spine/T2;mv \*ViSTa\* Brain/MWF; mv \*t2_tse_sag\*
Spine/T2_nice;**

Two steps combined:

**rm \*.json; rm \*Scout\*; rm \*ocalizer\*; mv \*QSM\*.nii.gz
Brain/QSM**; **mv \*swi\*.nii.gz Brain/SWI; mv \*diff\* Brain/DWI; mv
\*t1_mpr_iso\* Brain/T1; mv \*spc_da-fl\* Brain/FLAIR; mv \*spc_ir\*
Brain/PSIR; mv \*DWI\* Spine/DWI; mv \*GRE-ME\* Spine/GRE_ME; mv
\*mp2rage_offline\* Brain/MP2RAGE; mv \*T1w\* Spine/T1; mv \*T2w\*
Spine/T2; mv \*ViSTa\* Brain/MWF; mv \*t2_tse_sag\* Spine/T2_nice;**

Potentially useful
==================

Model fitting NODDI toolbox 
---------------------------

(http://nitrc.org/projects/noddi_toolbox)

FSL Maths Commands
------------------

The information below comes from "fslmaths --help". I put it here to
make it easier to find for people like me, who tend to believe that
everything can be found through Google.

**Usage: fslmaths \[-dt \<datatype\>\] \<first_input\> \[operations and
inputs\] \<output\> \[-odt \<datatype\>\]**

**Datatype information:**

-dt sets the datatype used internally for calculations (default float
for all except double images)

-odt sets the output datatype (default as original image)

Possible datatypes are: char short int float double

Additionally "-dt input" will set the internal datatype to that of the
original image

**Binary operations (image-image or image-number):**

(inputs can be either an image or a number)

-add : add following input to current image

-sub : subtract following input from current image

-mul : multiply current image by following input

-div : divide current image by following input

Examples:

fslmaths image0 -sub image1 imdiff

How to transform a mask with FLIRT from one space to another?
-------------------------------------------------------------

Transforming masks with FSL requires a little extra care. To steps are
needed: **(i) transform the mask into the new space, and (ii)
rethreshold the transformed image to make it into a binary mask again.**

Masks can be transformed from one space to another by using either one
of the command line tools flirt or applywarp, or the ApplyXFM GUI.

The threshold used (with fslmaths) should be set depending on the
intended use of the output mask. These guidelines should help in
determining the correct value to use:

-   a threshold near 1 (say 0.9) is conservative

    -   only voxels in the new space that overlap by 90% with the
        > original mask will be included in the new binary mask

-   a threshold near 0 (say 0.1) is liberal

    -   any voxel in the new space that overlaps by 10% or more with the
        > original mask will be included in the new binary mask

-   a threshold of 0.5 will (approximately) preserve the size of the
    > original mask

    -   any voxel in the new space that overlaps by 50% or more with the
        > original mask will be included in the new binary mask

The best choice of threshold will depend on the application in which the
mask is being used. For example, if the mask is being used to quantify
values within an ROI and it is important to not include contamination
from surrounding areas, then a high threshold should be used.
Alternatively, if the mask is being used to define an exclusion ROI then
it may be better to have a liberal border, which can be achieved with a
low threshold.

Example 1: transforming a mask from standard space to highres space
(linear registration)

-   flirt -in standard_mask -ref highres -applyxfm -init
    > standard2highres.mat -out highres_mask\
    > fslmaths highres_mask -thr 0.9 -bin highres_mask Note that in this
    > case either flirt, applywarp or the ApplyXFM GUI could have been
    > used for the first step.

Example 2: transforming a mask from standard space to highres space
(nonlinear registration)

-   applywarp -i standard_mask -r highres -w standard2highres_warp -out
    > highres_mask\
    > fslmaths highres_mask -thr 0.9 -bin highres_mask Note that in this
    > case the applywarp command must be used since there is a nonlinear
    > transformation (warp) involved. It is also necessary to have the
    > warp in the correct direction (standard2highres_warp and not
    > highres2standard_warp), but if only the opposite direction is
    > available (e.g. highres2standard_warp) then this can be inverted
    > using the invwarp command.

Example 3: transforming a mask between different resolution versions of
standard space (e.g. 3mm to 2mm)

-   flirt -in mask3mm -ref \$FSLDIR/data/standard/MNI152_T1_2mm
    > -applyxfm -usesqform -out mask2mm\
    > fslmaths mask2mm -thr 0.5 -bin highres_mask Note that in this case
    > the flirt command line must be used since the -usesqform flag
    > aligns the images based on standard space coordinates, and not
    > using a prior transformation matrix or warp.

In each case the transformation (flirt, applywarp or ApplyXFM GUI)
forces the output to be floating point, even when the input is integer.
Thresholding and binarising is done by fslmaths in the second call.

**Simple applying transformation to mask created in FLAIR to be
registered to FLAIR\***

**Nearest neighbour interpolation!**

**flirt -in
Desktop/pilot/sub-MsPilot1_acq-flair-spc_T1w_mask_hyperintense.nii.gz
-ref Desktop/NAWA/NIFTI/FLAIR/FLAIR_star_FLAIR_toMAG.nii.gz -out
Desktop/NAWA/NIFTI/FLAIR/FLAIR_star_FLAIR_toMAG_mask.nii.gz -init
Desktop/NAWA/NIFTI/Magnitude/FLAIR_toMAG_12DOF.mat -applyxfm -interp
nearestneighbour**

A mask (such as a lesion mask) should be binary, that is, it should
contain ONLY 0's and 1's. This is because statistical programs for
evaluating lesion masks, along with various image math procedures often
assume the values are 0's and 1's. So, we want to make sure the masks
remain binary.

Some tools, like MRIcron, offer a smoothing option for masks. The
problem is that smoothing may be accomplished by softening the edges
which means that those values are interpolated (i.e., 1's are replaced
with values like 0.5, 0.3 etc). In addition, if you register your mask
to a different image space you can introduce interpolated values if you
fail to use *Nearest Neighbour* interpolation. You should go through the
[[Hidden Problems
Section]{.ul}](https://neuroimaging-core-docs.readthedocs.io/en/latest/pages/image_processing_tips.html#check-hidden-problems)
below, before registering a mask. In this section, I offer several tools
for improving masks without compromising their binary nature.

**Ensure Masks are Binary**

If you reslice a mask into a different space, you should do so with
*Nearest Neighbour* interpolation. Otherwise, values at the edges of the
mask may be interpolated between 1 and 0. Smoothing a mask may result in
the same problem. To ensure masks are binary, use fslmaths. -bin sets
all values above 0 to 1. -odt char sets the bitdepth to 8-bits:

fslmaths lesion -bin lesion -odt char

**fslmaths Desktop/NAWA/NIFTI/FLAIR/FLAIR_star_FLAIR_toMAG_mask.nii.gz
-thr 0.5 -bin
Desktop/NAWA/NIFTI/FLAIR/FLAIR_star_FLAIR_toMAG_mask.nii.gz -odt char**

Check that a mask contains correct values (-M Mean of non-zero voxels
should be 1. -S Standard deviation of non-zero voxels should be 0:

fslstats lesion -M -S

1.000000 0.000000

**fslstats Desktop/NAWA/NIFTI/FLAIR/FLAIR_star_FLAIR_toMAG_mask.nii.gz
-M -S**

### **Erode**

Remove islands and spikes by eroding the edges of the lesion mask.
[[erode.sh]{.ul}](https://bitbucket.org/dpat/tools/raw/master/LIBRARY/erode.sh)
is a bit less complex to call than the fslmaths command. In the command
below, we do one iteration of the erosion and do it in 3D (default is
2D):

**erode.sh lesion 1 3D**

Warning

Be Careful with erosion! If you run too many iterations on a small mask,
the mask will disappear! You might want to make a backup copy of your
mask first.\\

Dilate

Fill tiny holes in the mask by dilating the edges of the lesion mask.
dilate.sh is a bit less complex to call than the fslmaths command. In
the command below, we do one iteration of the dilation and do it in 3D
(default is 2D):

**dilate.sh lesion 1 3D**

**APPLYXFM -not currently used**

To apply a saved transformation to another image use:

**flirt -in newvol -ref refvol -out outvol -init invol2refvol.mat
-applyxfm**

Note that the previous transformation matrix is used with the -init
command and that the size of the otput volume is determined by refvol
although its contents are **not** used.

Orientation swap for wrongly aligned images: 
--------------------------------------------

Usage: fslswapdim \<input\> \<a\> \<b\> \<c\> \[output\]

where a,b,c represent the new x,y,z axes in terms of the

old axes. They can take values of -x,x,y,-y,z,-z

or RL,LR,AP,PA,SI,IS (in the case of nifti inputs)

e.g. fslswapdim invol y x -z outvol

or **fslswapdim invol RL PA IS outvol**

where the latter will convert to axial slicing

(to match the avg152 images)

How to create an MP2RAGE UNI image from two inversion images?
-------------------------------------------------------------

[[https://github.com/Gilles86/pymp2rage/blob/master/notebooks/MP2RAGE%20and%20T1%20fitting.ipynb]{.ul}](https://github.com/Gilles86/pymp2rage/blob/master/notebooks/MP2RAGE%20and%20T1%20fitting.ipynb)

docker run -p 8888:8888 -v /Users/paweljakuszyk/Desktop/P2_MP2RAGE:/data
jupyter/pymp2rage

fitter = pymp2rage.MP2RAGE(MPRAGE_tr=5000.0,

invtimesAB=\[0.64, 2.5\],

flipangleABdegree=\[4,5\],

nZslices=176,

FLASH_tr=\[0.00298, 0.00298\],

inv1=\'/data/IT1_cubric_mp2rage_20210518122119_9.nii\',

inv1ph=\'/data/IT1_pha.nii\',

inv2=\'/data/IT2_cubric_mp2rage_20210518122119_9.nii\',

inv2ph=\'/data/IT2_pha.nii\')

**UNI image denoising:**

[[https://github.com/benoitberanger/mp2rage]{.ul}](https://github.com/benoitberanger/mp2rage)

Results are not good, a lot of noise realted artefacts is visible in the
brain tissue and image quality is not satisfactory.

**Potentially usefull SPM toolboxes:**

### **ALI - Automated Lesion Identification**

### **Clinical Toolbox**

### **EMS - Expectation Maximization Segmentation**

Spinal cord toolbox

Registering DTI to FMRIB58 (MNI152) and back:
---------------------------------------------

After creating the tensors, we want to convert the FA, MD, and RD images
into standard space so that we can utilize a brain atlas for ROI
selection.

We will first convert the FA image to MNI standard space using FSL\'s
FLIRT and FNIRT tools.

To do this, we will utilize the FMRIB58_FA_2mm.nii.gz image contained
within the fsl/data/standard/ directory. For ease of use in this
tutorial, we have also included this image file in our tutorial download
folder.

Copy the FMRIB58_FA_2mm.nii.gz image into the same directory as the
tensor files calculated in the step above, and then run the following
FLIRT command:

**flirt -in Pilot_6\_FA.nii -ref
\${FSLDIR}/data/standard/FMRIB58_FA_2mm.nii.gz -out Pilot_6\_FA_flirt
-omat Pilot_6\_FA_flirt.mat**

Then, run the following FNIRT command:

**fnirt \--ref=\${FSLDIR}/data/standard/FMRIB58_FA_2mm.nii.gz
\--in=Pilot_6\_FA.nii \--aff=Pilot_6\_FA_flirt.mat
\--cout=Pilot_6\_FA_fnirt_transf \--config=FA_2\_FMRIB58_2mm**

We will then apply the fnirt transformatin matrix created by the command
above to the s01_FA.nii, s01_MD.nii, and s01_RD.nii images by entering
the following commands, one at a time:

**applywarp \--ref=\${FSLDIR}/data/standard/FMRIB58_FA_1mm.nii.gz
\--in=Pilot_1\_FA.nii \--warp=Pilot_1\_FA_fnirt_transf
\--out=Pilot_1\_FA_FMRIB58.nii.gz; applywarp
\--ref=\${FSLDIR}/data/standard/FMRIB58_FA_1mm.nii.gz
\--in=Pilot_1\_MD.nii \--warp=Pilot_1\_FA_fnirt_transf
\--out=Pilot_1\_MD_FMRIB58.nii.gz; applywarp
\--ref=\${FSLDIR}/data/standard/FMRIB58_FA_1mm.nii.gz
\--in=Pilot_1\_RD.nii \--warp=Pilot_1\_FA_fnirt_transf
\--out=Pilot_1\_RD_FMRIB58.nii.gz**

Create SWI+R2\* relaxometry and QSM
===================================

Prepare data:
-------------

Merge magnitude and phase nifti echo files in time:

For QSM:

**fslmerge -t magnitude.nii.gz \*\_e?.nii.gz;**

**fslmerge -t phase.nii.gz \*\_e?\_ph.nii.gz;**

For SWI:

**fslmerge -t magnitude.nii.gz
\*\_swi_highres_multiecho\_\*\_e?.nii.gz;**

**fslmerge -t phase.nii.gz
\*\_swi_highres_multiecho\_\*\_e?\_ph.nii.gz;**

? zastępuje pojedynczy znak, \* więcej znaków

Create SWI:
-----------

[[https://github.com/korbinian90/CLEARSWI.jl]{.ul}](https://github.com/korbinian90/CLEARSWI.jl)

Start Julia in the directory where merged phase and magnitude files are
stored:

This is a simple multi-echo case without changing default behavior

To see filtered phase:

Set writesteps to the path, where intermediate steps should be saved,
e.g. writesteps=\"/tmp/clearswi_steps\". If set to nothing, intermediate
steps won\'t be saved.

**using CLEARSWI**

**TEs = \[9.22,16.44,24.98\]** - na pacs są informacje dotyczące
parametrów sekwencji (e.g. TE, TR). TEs SWI_HIGH_RES =
\[9.22,16.44,24.98\]

**mag =readmag(\"magnitude.nii.gz\");**

**phase = readphase(\"phase.nii.gz\");**

**data = Data(mag, phase, mag.header, TEs);**

**swi = calculateSWI(data);**

**savenii(swi, \"SWI.nii.gz\"; header=mag.header);**

### R2\* relaxometry:

\#Load package:

**using MriResearchTools**

\#Create a T2\* map:

**t2s = NumART2star(mag, TEs);**

\#Invert it to get the R2\* map:

**r2s = r2s_from_t2s(t2s);**

\#Save both of them:

**savenii(t2s, \"t2s_map.nii.gz\"; header=mag.header);**

**savenii(r2s, \"r2s_map.nii.gz\"; header=mag.header);**

### Calculate R2\* relaxation in the basal ganglia:

Make a basal ganglia mask by segmenting using T1 nad fsl_first (putamen,
caudate and pallidum):

**run_first_all -i \*t1_mpr_iso\_\*.nii.gz -s
L_Caud,L_Pall,L_Puta,R_Caud,R_Pall,R_Puta -o basal_ganglia_seg.nii.gz**

Binarize the mask:

**fslmaths basal_ganglia_seg_all_none_firstseg.nii.gz -bin
basal_ganglia_mask.nii.gz**

Register the mask to R2\* map (basically magnitude header):

Bet T1, correct it for field bias and do the neck cleanup:

**bet \*t1_mpr_iso\_\*.nii.gz T1_bet_biascorr.nii.gz -f 0.5 -B;**

\#Always check your bet results and just -f value accordingly!

**mrview \*t1_mpr_iso\_\*.nii.gz -overlay.load T1_bet_biascorr.nii.gz
&;**

Bet the magnitude image:

**../SWI/;**

**bet magnitude.nii.gz magnitude_bet.nii.gz -f 0.5 -R;**

**mrview magnitude.nii.gz -overlay.load magnitude_bet.nii.gz&;**

**../T1/;**

Register the magnitude image to T1:

**flirt -in ../SWI/magnitude_bet.nii.gz -ref T1_bet_biascorr.nii.gz
-omat mag_to_t1.mat -dof 6 -cost normmi;**

\#To invert a saved transformation:

**convert_xfm -omat t1_to_mag.mat -inverse mag_to_t1.mat;**

\#Use the .mat file to register the basal ganglia mask to R2s space:

**flirt -in basal_ganglia_mask.nii.gz -ref ../SWI/magnitude_bet.nii.gz
-out ../SWI/basal_ganlgia_mask_2\_mag.nii.gz -init t1_to_mag.mat
-applyxfm -interp nearestneighbour;**

**mrview magnitude_bet.nii.gz -overlay.load
basal_ganlgia_mask_2\_mag.nii.gz&;**

\#Extract the mean R2\* in the basal ganglia:

**../SWI/;**

**echo R2 in the basal ganglia;**

**fslstats r2s_map.nii.gz -k basal_ganlgia_mask_2\_mag.nii.gz -M;**

**../T1/;**

### Calculate R2\* relaxation in lesions:

Bet FLAIR:

**../FLAIR/;**

**bet \*t2_spc_da-fl_sag_p2_iso\*.nii.gz FLAIR_bet.nii.gz -f 0.5 -R;**

\#Always check your bet results and just -f value accordingly!

**mrview \*t2_spc_da-fl_sag_p2_iso\*.nii.gz -overlay.load
FLAIR_bet.nii.gz &;**

**../SWI/;**

Register the FLAIR to magnitude:

**flirt -in ../FLAIR/FLAIR_bet.nii.gz -ref magnitude_bet.nii.gz -out
FLAIR_to_mag.nii.gz -omat FLAIR_to_mag.mat -dof 6 -cost normmi**

Use the .mat file to register FLAIR lesion mask to R2s space:

**flirt -in ../FLAIR/FLAIR_lesion_mask.nii.gz -ref magnitude_bet.nii.gz
-out lesion_mask_2\_mag.nii.gz -init FLAIR_to_mag.mat -applyxfm -interp
nearestneighbour;**

\#Extract the mean R2\* in the lesioned WM:

**echo R2 in lesioned WM;**

**fslstats r2s_map.nii.gz -k lesion_mask_2\_mag.nii.gz -M;**

### R2\* in NAWM from JHU atlas:

Bet the magnitude image:

**../SWI/;**

**bet magnitude.nii.gz magnitude_bet.nii.gz -f 0.5 ;**

**mrview magnitude.nii.gz -overlay.load magnitude_bet.nii.gz&;**

**../T1/;**

**Register the magnitude image to T1:**

**flirt -in ../SWI/magnitude_bet.nii.gz -ref T1_bet_biascorr.nii.gz
-omat mag_to_t1.mat -dof 6 -cost normmi;**

Invert the transformation:

**convert_xfm -inverse mag_to_t1.mat -omat T1_to_mag.mat**

Concat the matrices (you should have the b0_to_T1.mat from DTI section):

convert_xfm -omat \'\'transf_A\_to_C.mat\'\' -concat
\'\'transf_B\_to_C.mat\'\' \'\'transf_A\_to_B.mat\'\'

**convert_xfm -omat b0_to_mag.mat -concat T1_to_mag.mat b0_to_T1.mat**

Use the acquired matrix to transform NAWM without OR into MWF space:

**flirt -in ../DWI/NAWM_atlas.nii.gz -ref ../SWI/magnitude_bet.nii.gz
-applyxfm -init b0_to_mag.mat -out ../SWI/NAWM_atlas_in_mag.nii.gz
-interp nearestneighbour**

\#Use fsl stats:

**../SWI/**

**echo mean R2 in NAWM Atlas;**

**fslstats r2s_map.nii.gz -k NAWM_atlas_in_mag.nii.gz -M;**

### R2\* in NAWM from Tractseg MWF:

Bet the magnitude image:

**../SWI/;**

**bet magnitude.nii.gz magnitude_bet.nii.gz -f 0.5;**

**mrview magnitude.nii.gz -overlay.load magnitude_bet.nii.gz&;**

**../T1/;**

**Register the magnitude image to T1:**

**flirt -in ../SWI/magnitude_bet.nii.gz -ref T1_bet_biascorr.nii.gz
-omat mag_to_t1.mat -dof 6 -cost normmi;**

Invert the transformation:

**convert_xfm -inverse mag_to_t1.mat -omat T1_to_mag.mat**

Concat the matrices (you should have the b0_to_T1.mat from DTI section):

convert_xfm -omat \'\'transf_A\_to_C.mat\'\' -concat
\'\'transf_B\_to_C.mat\'\' \'\'transf_A\_to_B.mat\'\'

**convert_xfm -omat b0_to_mag.mat -concat T1_to_mag.mat b0_to_T1.mat**

Use the acquired matrix to transform NAWM without OR into MWF space:

**flirt -in ../DWI/NAWM_TractSeg.nii.gz -ref ../SWI/magnitude_bet.nii.gz
-applyxfm -init b0_to_mag.mat -out ../SWI/NAWM_TractSeg_in_mag.nii.gz
-interp nearestneighbour**

\#Use fsl stats:

**../SWI/**

**echo mean R2 in NAWM TractSeg;**

**fslstats r2s_map.nii.gz -k NAWM_TractSeg_in_mag.nii.gz -M;**

Create QSM:
-----------

Use LBV and MEDI algorithms.

[[https://sepia-documentation.readthedocs.io/en/latest/gui/Sepia-One-stop-QSM-processing.html]{.ul}](https://sepia-documentation.readthedocs.io/en/latest/gui/Sepia-One-stop-QSM-processing.html)

Echo times: \[4.65,9.15,13.65,18.15,22.65\]

![](media/image1.png){width="3.2038374890638672in"
height="3.1614588801399823in"}

FLAIR\*
=======

Create a FLAIR\* image which is a combined image of FLAIR and SWI used
to assess central vein sign.

Brain extraction
----------------

By default bet just calls the bet2 program for simple brain extraction.
However, it also allows various additional behaviour. The basic usage
is:

**bet \<input\> \<output\> \[options\]**

Bet FLAIR:

**bet pilot7dcm_t2_spc_da-fl_sag_p2_iso_20210806093159_6.nii.gz
FLAIR_bet.nii.gz -f 0.5**

Bet Magnitude:

**bet magnitude.nii.gz magnitude_bet.nii.gz -f 0.5;**

**mrview magnitude.nii.gz -overlay.load magnitude_bet.nii.gz &;**

Bet SWI:

**bet SWI.nii.gz SWI_bet.nii.gz -f 0.3 -R;**

**mrview SWI.nii.gz -overlay.load SWI_bet.nii.gz &;**

Lower -f values give larger brain estimate (leaves more brain)

Always check your bet results and just -f value accordingly!

Registration
------------

Register FLAIR to MAG (you should already have it from the previous
step)

**flirt -in FLAIR/FLAIR_bet.nii.gz -ref SWI/magnitude_bet.nii.gz -out
FLAIR/FLAIR_to_MAG.nii.gz -omat FLAIR/FLAIR_to_MAG.mat -dof 6 -cost
normmi**

Multiply SWI and FLAIR
----------------------

**fslmaths SWI_bet.nii.gz -mul ../FLAIR/FLAIR_to_mag.nii.gz
../FLAIR/FLAIR_star.nii.gz;**

**fsleyes ../FLAIR/FLAIR_star.nii.gz;**

So far the best result comes from registering FLAIR to Magnitude (cost
norm mut info, 6 DOF) and then multiplying the result by SWI.

Lesion volume estimation \[in mm3\]
===================================

**How can I calculate the number of voxels in a mask?**
-------------------------------------------------------

Let's say you have two masks in an image, labeled A and B. Mask A is
composed of 1's, and Mask B is composed of 2's. If these masks are saved
into one image called ROIs.nii.gz, and they were created from a template
called ROI_Template.nii.gz, you can use the command:

fslstats ROIs.nii.gz ROI_Template.nii.gz -V

Which will return two numbers per mask. The first number is the number
of voxels, and the second number is the volume, in cubic millimeters.
For example, if one of my masks was 9 voxels large and the other one was
15 voxels, with a 2x2x2mm resolution (or 8 cubic millimeters per voxel),
the output would look like this:

9 72.000000 15 120.000000

-v : output \<voxels\> \<volume\>

**-V : output \<voxels\> \<volume\> (for nonzero voxels)**

**fslstats FLAIR_lesion_mask.nii.gz -V;**

For the right volume we need to have a binary mask!

WM GM segmentation volume estimations

### Cluster Count

It can be difficult to determine whether a lesion mask is one big volume
or whether little islands have broken off.
[[cluster_count.sh]{.ul}](https://bitbucket.org/dpat/tools/raw/master/LIBRARY/cluster_count.sh)
tells you how many separate clusters are in the mask, how big they are
and the center of each one. In general, I can't imagine why you'd want
to keep clusters of less than about 10 voxels. In the command below we
ask how many clusters are in lesion_mask.nii.gz and we set connectivity
to 6.

Connectivity can be set at 6, 18 or 26, but always defaults to 26.

-   If the connectivity is set to 6, then voxels only belong to a single
    > cluster if their faces are in contact.

-   If the connectivity is set to 18, then voxels belong to a single
    > cluster if their faces OR edges are in contact.

-   And, if the connectivity is set to 26 (the default if you don't
    > specify a number), then voxels belong to a single cluster if their
    > faces, edges or corners are in contact.

So, setting the connectivity to 6 ensures the greatest possible number
of clusters will be counted:

**cluster_count.sh lesion 6**

Calculating subcortical structures volume
=========================================

Segmentation using FIRST

The simplest way to perform segmentation using FIRST is to use the
run_first_all script which segments all the subcortical structures,
producing mesh and volumetric outputs (applying boundary correction). It
uses default settings for each structure which have been optimised
empirically.

run_first_all

This script will run lower-level utilities (including first_flirt,
run_first and first) on all the structures, with the settings (number of
modes and boundary correction) tuned to be optimal for each structure.
Both mesh (vtk) and volumetric (nifti) outputs are generated. Corrected
and uncorrected volumetric representations of the native mesh are
generated. The final stage of the script ensures that there is no
overlap between structures in the 3D image, which can occur even when
there is no overlap of the meshes, as can be seen in the individual,
uncorrected segmentation images in the 4D image file.

Example usage:

**run_first_all -i t1_image -o output_name**

**run_first_all -i scans_t1_mpr_iso_20210723114038_5.nii -o
Pilot_6\_seg.nii.gz**

The argument -i specifies the original T1-weighted structural image
(only T1-weighted images can be used).

The argument -o specifies the filename for the output image basename.
run_first_all will include the type of boundary correction into the
final file name. For example, the command above would produce
output_name_all_fast_firstseg.nii.gz and
output_name_all_fast_origsegs.nii.gz.

Output

output_name_all_fast_firstseg.nii.gz : This is a single image showing
the segmented output for all structures. The image is produced by
filling the estimated surface meshes and then running a step to ensure
that there is no overlap between structures. The output uses the CMA
standard labels (the colour table is built into FSLView). If another
boundary correction method is specified, the name fast in this filename
will change to reflect the boundary correction that is used. Note that
if only one structure is specified then this file will be called
output_name-struct_corr.nii.gz instead (e.g. sub001-L_Caud_corr.nii.gz).

output_name_all_fast_origsegs.nii.gz : This is a 4D image containing the
individual structure segmentations, converted directly from the native
mesh representation and without any boundary correction. For each
structure there is an individual 3D image where the interior is labeled
according to the CMA standard labels while the boundary uses these label
values plus 100. Note that if only one structure is specified then this
file will be called output_name-struct_first.nii.gz instead (e.g.
sub001-L_Caud_first.nii.gz).

output_name_first.vtk : This is the mesh representation of the final
segmentation. It can be directly viewed in FSLView using 3D mode.

output_name_first.bvars: Do not delete this file. It contains the mode
parameters and the model used. This file, along with the appropriate
model files, can be used to reconstruct the other outputs. The mode
parameters are what FIRST optimizes. This output can be used be used
later as to perform vertex analysis or as a shape prior to segment other
shapes.

Options

-m specifies the boundary correction method. The default is auto, which
chooses different options for different structures using the settings
that were found to be empirically optimal for each structure. Other
options are: fast (using FAST-based, mixture-model, tissue-type
classification); thresh (thresholds a simple single-Gaussian intensity
model); or none.

-s allows a restricted set of structures (one or more) to be selected.
For more than one structure the list must be comma separated with no
spaces. The list of possible structures is: L_Accu L_Amyg L_Caud L_Hipp
L_Pall L_Puta L_Thal R_Accu R_Amyg R_Caud R_Hipp R_Pall R_Puta R_Thal
BrStem.

-b specifies that the input image is brain extracted - important when
calculating the registration.

-a specifies a pre-calculated registration matrix (from running
first_flirt) to be used instead of calculating the registration again.

Then calculate the volume of a desired structure using fslstats:
----------------------------------------------------------------

Volumetric Analysis

Currently, to perform volumetric analysis it is necessary to determine
the label number of the structure of interest and use fslstats to
measure the volume. Other software (e.g. SPSS or MATLAB) needs to be
used to analyse the volume measurements.

To find the label number, load the output_name\_\*\_firstseg.nii.gz
image into FSLView, click on a voxel in the structure of interest and
the label number will be the number in the Intensity box. Alternatively,
you can find the number from the [[CMA standard
labels]{.ul}](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FIRST/UserGuide#Labels).

Once you have the label number you can measure the volume using fslstats
with the threshold options to select out just the single label number
(by using -l and -u with -/+0.5 from the desired label number). For
example, if the label number is 17 (Left Hippocampus) then you can use
the following command:

fslstats output_name_all_fast_firstseg -l 16.5 -u 17.5 -V where the
first number of the output is the number of voxels and the second is the
volume in mm^3^.

For thalamus volume calculation:

Left thalamus:

**fslstats output_fast_firstseg.nii.gz -l 9.5 -u 10.5 -V**

Right thalamus:

**fslstats output_fast_firstseg.nii.gz -l 48.5 -u 49.5 -V**

Labels
------

10 Left-Thalamus-Proper 40

11 Left-Caudate 30

12 Left-Putamen 40

13 Left-Pallidum 40

16 Brain-Stem /4th Ventricle 40

17 Left-Hippocampus 30

18 Left-Amygdala 50

26 Left-Accumbens-area 50

49 Right-Thalamus-Proper 40

50 Right-Caudate 30

51 Right-Putamen 40

52 Right-Pallidum 40

53 Right-Hippocampus 30

54 Right-Amygdala 50

58 Right-Accumbens-area 50

Brain volumetrics - calculated with freesurfer
==============================================

Before we get to calculate brain volumetric we have to account for T1
black holes (old demyelinated WM tissue that appears dark on T1), which
may cause problems with overestimation of certain brain structures like
cortex or basal ganglia. In order to do that we have to fill in the
black hole tissue in T1 with the intensity values interpolated from the
surrounding normal-appearing WM tissue.

**cd T1;**

\#Bet T1 and at the same time perform bias field correction:

**bet \*t1_mpr_iso\*.nii.gz T1_bet_biascorr.nii.gz -f 0.2 -B; mrview
\*t1_mpr_iso\_\*.nii.gz -overlay.load T1_bet_biascorr.nii.gz &;**

\#Segment T1 with fsl fast in order to obtain WM mask:

**fast T1_bet_biascorr.nii.gz; fslmaths T1_bet_biascorr_pve_2.nii.gz
-thr 0.95 -bin WM_mask.nii.gz;**

**../FLAIR;**

\#Bet FLAIR:

**bet \*t2_spc_da-fl_sag_p2_iso\*nii.gz FLAIR_bet.nii.gz -f 0.5 -R;
mrview \*t2_spc_da-fl_sag_p2_iso\*.nii.gz -overlay.load FLAIR_bet.nii.gz
&;**

\#Register FLAIR to T1:

**flirt -in FLAIR_bet.nii.gz -ref ..T1/T1_bet_biascorr.nii.gz -omat
FLAIR_to_t1.mat -dof 6 -cost normmi;**

\#Use the generated matrix to register Flair lesion mask to T1

**flirt -in FLAIR_lesion_mask.nii.gz -ref ../T1/T1_bet_biascorr.nii.gz
-out ../T1/FLAIR_lesion_mask_in_T1.nii.gz -init FLAIR_to_t1.mat
-applyxfm -interp nearestneighbour;**

**../T1;**

\#Perform the lesion filling

**lesion_filling -i \*mpr_iso\_\*.nii.gz -l
FLAIR_lesion_mask_in_T1.nii.gz -w WM_mask.nii.gz -o T1_filled.nii.gz;**

\#Always check the results. Especially problematic lesion placement is
near the ventricles and basal ganglia where the right correction is
crucial

We will generate all of the images mentioned above with the command
recon-all, which only requires a T1-weighted anatomical image with good
contrast between the white matter and the grey matter. If you are in the
Cannabis directory, navigate to sub-101's anatomical directory by typing
cd sub-101/ses-BL/anat. You can then run recon-all with the following
command:

**recon-all -s sub-101 -i sub-101_ses-BL_T1w.nii.gz -all**

The -s option specifies the subject name, which you can set to whatever
you want. The -i option points to the anatomical image that you will
analyze; and the -all option will run all of the preprocessing steps on
your data. Except for when you are re-running a recon-all command after
[[editing the
data]{.ul}](https://andysbrainbook.readthedocs.io/en/latest/FreeSurfer/FS_ShortCourse/FS_12_FailureModes.html#fs-12-failuremodes),
you will always want to use the -all option.

As the command is running, the output will be placed in a directory
called \$SUBJECTS_DIR. By default, \$SUBJECTS_DIR is a variable that
points to the directory \$FREESURFER_HOME/subjects, in which
\$FREESURFER_HOME is another variable pointing to the directory in which
FreeSurfer was installed - such as /usr/local/freesurfer. In other
words, the output of this recon-all command will be in
/usr/local/freesurfer/subjects.

**Note**

**If you get a permission error when running recon-all, type the
following: Sudo chmod -R a+w \$SUBJECTS_DIR And then rerun the recon-all
command.**

I also recommend adding the qcache option, which will smooth the data at
different levels and store them in the subject's output directory. These
will be useful for [[group level
analyses]{.ul}](https://andysbrainbook.readthedocs.io/en/latest/FreeSurfer/FS_ShortCourse/FS_08_GroupAnalysis.html#fs-08-groupanalysis),
which we will cover in a future tutorial. If you've already run the
recon-all preprocessing on your subjects, you can run qcache with the
following command:

**recon-all -s \<subjectName\> -qcache**

Which should take about 10 minutes per subject.

**FreeSurfer** A file named aseg.stats is created inside the directory
"/stats" and during recon-all processing, this file contains the summary
of all VOIs of the segmented image. For this study, the volumes "brain
segmentation volume","total gray matter volume",and "total cerebral
white matter volume" were used

Run Freesurfer as a standalone shell container on Calcus:
---------------------------------------------------------

First you have to define environmental variables in the shell script,
they will bind selected folders (make sure they exist) to the
singularity and let you use them while running it. Additionally this
variable will specify the freesurfer license directory and file, which
is needed to run freesurfer software (make sure you have license.txt in
the right directory).

In order to access your shell script type:

**nano .bash_profile**

This will direct you to the shell script file, which can be edited. You
should paste the following code into it (the paths should be changed
according to your preference and the location of license.txt):

**export
SINGULARITY_BINDPATH=\"/home/user/data:/data:ro,/home/user/output:/out,/home/user/license.txt:/opt/freesurfer/license.txt"**

Once pasted, press ctrl+x in order exit the shell script and confirm
changes by pressing "y" and enter.

Next, a shell restart is required for the changes to take effect:

**. \~/.bash_profile**

Run the singularity:

**singularity shell /opt/software/bids_freesurfer.simg**

You are now within a singularity shell where all freesurfer commands
should be operational e.g.:

**recon-all -s sub_X -i input_T1.nii.gz -sd /home/user/output/ -all**

The -sd argument is needed to specify the output as freesurfer's default
output folder will not be available on Calcus \--ALTERNATIVE\-- every
time you run the container you can override default freesurfer's subject
directory and run everything normally:

**export SUBJECTS_DIR=/home/pjakuszyk/output**

### Calculate cortical thickness based on the output from the recon-all command.

**It has to be calculated for the left and right hemisphere separately
and the average is taken into account.**

[[https://surfer.nmr.mgh.harvard.edu/fswiki/mris_anatomical_stats]{.ul}](https://surfer.nmr.mgh.harvard.edu/fswiki/mris_anatomical_stats)

**mris_anatomical_stats \[options\] \<subjectname\> \<hemi\>
\[\<surfacename\>\]**

For left hemisphere:

**mris_anatomical_stats -log Pilot_5\_cortical_thickness_lh.log Pilot_5
lh**

For right hemisphere:

**mris_anatomical_stats -log Pilot_5\_cortical_thickness_rh.log Pilot_5
rh**

SIENAX - Single-Time-Point Estimation - ultimately we use freesurfer
====================================================================

Usage

A default SIENAX analysis is run by typing:

**sienax \<input\>**

The input filename must not contain directory names - i.e. all must be
done within the current directory.

Other options are:

-o \<output-dir\> : set output directory (the default output is
\<input\>\_sienax)

-d : debug (don\'t delete intermediate files)

-B \"bet options\" : if you want to change the BET defaults, put BET
options inside double-quotes after using the -B flag. For example, to
increase the size of brain estimation, use: -B \"-f 0.3\"

-2: two-class segmentation (don\'t segment grey and white matter
separately) - use this if here is poor grey/white contrast

-t2: tell FAST that the input images are T2-weighted and not T1

-t \<t\>: ignore from t (mm) upwards in MNI152/Talairach space - if you
need to ignore the top part of the head (e.g. if some subjects have the
top missing and you need consistency across subjects)

-b \<b\>: ignore from b (mm) downwards in MNI152/Talairach space; b
should probably be -ve

-r: tell SIENAX to estimate \"regional\" volumes as well as global; this
produces peripheral cortex GM volume (3-class segmentation only) and
ventricular CSF volume

-lm \<mask\>: use a lesion (or lesion+CSF) mask to remove incorrectly
labelled \"grey matter\" voxels

-S \"FAST options\" : if you want to change the segmentation defaults,
put FAST options inside double-quotes after using the -S flag. For
example, to increase the number of segmentation iterations use: -S \"-i
20\"

What the script does

sienax carries out the following steps:

Run bet on the single input image, outputting the extracted brain, and
the skull image. If you need to call BET with a different threshold than
the default of 0.5, use -f \<threshold\>.

Run pairreg (which uses the brain and skull images to carry out
constrained registration); the MNI152 standard brain is the target
(reference), using brain and skull images derived from the MNI152. Thus,
as with two-time-point atrophy, the brain is registered (this time to
the standard brain), again using the skull as the scaling constraint.
Thus brain tissue volume (estimated below) will be relative to a
\"normalised\" skull size. (Ignore the \"WARNING: had difficulty finding
robust limits in histogram\" message; this appears because FLIRT isn\'t
too happy with the unusual histograms of skull images, but is nothing to
worry about in this context.) Note that all later steps are in fact
carried out on the original (but stripped) input image, not the
registered input image; this is so that the original image does not need
to be resampled (which introduces blurring). Instead, to make use of the
normalisation described above, the brain volume (estimated by the
segmentation step described below) is scaled by a scaling factor derived
from the normalising transform, before being reported as the final
normalised brain volume.

A standard brain image mask, (derived from the MNI152 and slightly
dilated) is transformed into the original image space (by inverting the
normalising transform found above) and applied to the brain image. This
helps ensure that the original brain extraction does not include
artefacts such as eyeballs.

Segmentation is now run on the masked brain using fast. If there is
reasonable grey-white contrast, grey matter and white matter volumes are
reported separately, as well as total brain volume (this is the default
behaviour). Otherwise (i.e. if sienax was called with the -2 option),
just brain/CSF/background segmentation is carried out, and only brain
volume is reported. Before reporting, all volumes are scaled by the
normalising scaling factor, as described above, so that all subjects\'
volumes are reported relative to a normalised skull size.

The main files created in the SIENAX output directory are:

report.sienax the SIENAX log, including the final volume estimates.

report.html a webpage report including images showing various stages of
the analysis, the final result and a description of the SIENAX method.

I_render a colour-rendered image showing the segmentation output
superimposed on top of the original image.

DWI 
===

MRTRIX tutorial
---------------

Overview
--------

MRtrix uses its own format for storing and displaying imaging data. If
you've already gone through the tutorials on the major fMRI software
packages, such as SPM, FSL, and AFNI, you may remember that all of them
can read and write images in NIFTI format. (AFNI by default will write
files in its own BRIK/HEAD format unless you specify that your output
should have a .nii extension, but it is the sole exception.) MRtrix is
also able to read raw data in NIFTI format, but will output its files in
MRtrix format, labeled with a .mif extension.

To see how this works, navigate to the folder sub-CON02/ses-preop/dwi,
which contains your diffusion data. One of the first steps for
preprocessing your data is converting the diffusion data to a format
that MRtrix understands; we will use the command mrconvert to combine
the raw diffusion data with its corresponding .bval and .bvec files, so
that we can use the combined file for future preprocessing steps:

**mrconvert \*AP\*14\*.nii.gz dwi.mif -fslgrad \*AP\*.bvec \*AP\*.bval**

This command requires three arguments: The input, which is the raw **DWI
file in the AP directory**; an output file, which we will call
sub-02_dwi.mif to make it more compact and easier to read; and -fslgrad,
which requires the corresponding .bvec and .bval files (in that order).

**Note that, since this is a 4-dimensional dataset, the last dimension
is time; in other words, this file contains 102 volumes, each one with
dimensions of 96 x 96 x 60 voxels. The last dimension of the Voxel size
field - which in this case has a value of 8.7 - indicates the time it
took to acquire each volume. This time is also called the repetition
time, or TR.**

Preprocessing:
--------------

dwi_denoise

The first preprocessing step we will do is denoise the data by using
MRtrix's dwidenoise command. This requires an input and an output
argument, and you also have the option to output the noise map with the
-noise option. For example:

**dwidenoise dwi.mif dwi_den.mif -noise noise.mif**

This command should take a couple of minutes to run.

One quality check is to see whether the residuals load onto any part of
the anatomy. If they do, that may indicate that the brain region is
disproportionately affected by some kind of artifact or distortion. To
calculate this residual, we will use another MRtrix command called
mrcalc:

**mrcalc dwi.mif dwi_den.mif -subtract residual.mif;**

**mrview residual.mif &**

You can then inspect the residual map with mrview:

It is common to see a grey outline of the brain, as in the figure above.
However, everything within the grey matter and white matter should be
relatively uniform and blurry; if you see any clear anatomical
landmarks, such as individual gyri or sulci, that may indicate that
those parts of the brain have been corrupted by noise. If that happens,
you can increase the extent of the denoising filter from the default of
5 to a larger number, such as 7; e.g.,

**dwidenoise your_data.mif your_data_denoised_7extent.mif -extent 7
-noise noise.mif**

mri_degibbs

An optional preprocessing step is to run mri_degibbs, which removes
[[Gibbs' ringing
artifacts]{.ul}](http://mriquestions.com/gibbs-artifact.html) from the
data. These artifacts look like ripples in a pond, and are most
conspicuous in the images that have a b-value of 0. Look at your
diffusion data first with mrview, and determine whether there are any
Gibbs artifacts; if there are, then you can run mrdegibbs by specifying
both an input file and output file, e.g.:

**mrdegibbs dwi_den.mif dwi_den_unr.mif;**

**mrview dwi_den.mif&; mrview dwi_den_unr.mif&;**

As always, inspect the data both before and after with mrview to
determine whether the preprocessing step made the data better, worse, or
had no effect.

If you don't see any Gibbs artifacts in your data, then I would
recommend omitting this step; we won't be using it for the rest of the
tutorial.

Extracting the Reverse Phase-Encoded Images
-------------------------------------------

Most diffusion datasets are composed of two separate imaging files: One
that is acquired with a primary phase-encoding direction, and one that
is acquired with a reverse phase-encoding direction. The primary
phase-encoding direction is used to acquire the majority of the
diffusion images at different b-values. The reverse-phase encoded file,
on the other hand, is used to unwarp any of the distortions that are
present in the primary phase-encoded file.

To understand how this works, imagine that you are using a blow dryer on
your hair. Let's say that you have the blow dryer pointed at the back of
your head, and it blows your hair forward, onto the front of your face;
let's call this the posterior-to-anterior (PA) phase-encoding direction.
Right now your hair looks like a mess, and you want to undo the effects
of the air blowing from the back of your head to the front of your head.
So you point the blow dryer at the front of your face, and it blows your
hair back. If you take the average between the two of those blow
dryings, your hair should be back in its normal position.

Similarly, we use both phase-encoding directions to create a sort of
average between the two. We know that both types of phase-encoding will
introduce two separate and opposite distortions into the data, but we
can use unwarping to cancel them out.

Our first step is to convert the reverse phase-encoded NIFTI file into
.mif format. We will also add its b-values and b-vectors into the
header:

**mrconvert \*PA\*12.nii.gz PA.mif;**

**mrconvert PA.mif -fslgrad \*PA\*.bvec \*PA\*.bval - \| mrmath - mean
mean_b0_PA.mif -axis 3**

Next, we extract the b-values from the primary phase-encoded image, and
then combine the two with mrcat:

**dwiextract dwi_den_unr.mif - -bzero \| mrmath - mean mean_b0_AP.mif
-axis 3;**

**mrcat mean_b0_AP.mif mean_b0_PA.mif -axis 3 b0_pair.mif**

This will create a new image, "b0_pair.mif", which contains both of the
average b=0 images for both phase-encoded images.

**Putting It All Together: Preprocessing with dwipreproc**
----------------------------------------------------------

We now have everything we need to run the main preprocessing step, which
is called by dwipreproc. For the most part, this command is a wrapper
that uses FSL commands such as topup and eddy to unwarp the data and
remove eddy currents. For this tutorial, we will use the following line
of code:

**dwifslpreproc dwi_den_unr.mif dwi_den_preproc.mif -nocleanup -pe_dir
AP -rpe_pair -se_epi b0_pair.mif -eddy_options \" \--slm=linear
\--data_is_shelled\"**

The first arguments are the input and output; the second option,
-nocleanup, will keep the temporary processing folder which contains a
few files we will examine later. -pe_dir AP signalizes that the primary
phase-encoding direction is anterior-to-posterior, and -rpe_pair
combined with the -se_epi options indicates that the following input
file (i.e., "b0_pair.mif") is a pair of spin-echo images that were
acquired with reverse phase-encoding directions. Lastly, -eddy_options
specifies options that are specific to the FSL command eddy. You can
visit the [[eddy user
guide]{.ul}](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/eddy/UsersGuide) for
more options and details about what they do. For now, we will only use
the options \--slm=linear (which can be useful for data that was
acquired with less than 60 directions) and \--data_is_shelled (which
indicates that the diffusion data was acquired with multiple b-values).

This command can take several hours to run, depending on the speed of
your computer. For an iMac with 8 processing cores, it takes roughly 2
hours. When it has finished, examine the output to see how eddy current
correction and unwarping have changed the data; ideally, you should see
more signal restored in regions such as the orbitofrontal cortex, which
is particularly susceptible to signal dropout:

**mrview \*\_preproc.mif -overlay.load dwi.mif**

This command will display the newly preprocessed data, with the original
diffusion data overlaid on top of it and colored in red. To see how the
eddy currents were unwarped, open the Overlays tab and click on the box
next to the image sub-02_dwi.mif. You should see a noticeable difference
between the two images, especially in the frontal lobes of the brain
near the eyes, which are most susceptible to eddy currents.

Checking for Corrupt Slices
---------------------------

One of the options in the dwifslpreproc command, "-nocleanup", retained
a directory with the string "tmp" in its title. Within this folder is a
file called dwi_post_eddy.eddy_outlier_map, which contains strings of
0's and 1's. Each 1 represents a slice that is an outlier, either
because of too much motion, eddy currents, or something else.

The following code, run from the dwi directory, will navigate into the
"tmp" folder and calculate the percentage of outlier slices:

**cd dwifslpreproc-tmp-\***

**totalSlices=\`mrinfo dwi.mif \| grep Dimensions \| awk \'{print \$6 \*
\$8}\'\`**

**totalOutliers=\`awk \'{ for(i=1;i\<=NF;i++)sum+=\$i } END { print sum
}\' dwi_post_eddy.eddy_outlier_map\`**

**echo \"If the following number is greater than 10, you may have to
discard this subject because of too much motion or corrupted slices\"**

**echo \"scale=5; (\$totalOutliers / \$totalSlices \* 100)/1\" \| bc \|
tee percentageOutliers.txt**

**cd ..**

The first two lines navigate into the "tmp" directory and calculate the
total number of slices by multiplying the number of slices for a single
volume by the total number of volumes in the dataset. The total number
of 1's in the outlier map is then calculated, and the percentage of
outlier slices is generated by dividing the number of outlier slices by
the total number of slices. If this number is greater than 10 - i.e., if
more than 10 percent of the slices are flagged as outliers - you should
consider removing the subject from further analyses.

**Generating a Mask**
---------------------

As with fMRI analysis, it is useful to create a mask to restrict your
analysis only to brain voxels; this will speed up the rest of your
analyses.

To do that, it can be useful to run a command beforehand called
dwibiascorrect. This can remove inhomogeneities detected in the data
that can lead to a better mask estimation. However, it can in some cases
lead to a worse estimation; as with all of the preprocessing steps, you
should check it before and after each step:

**dwibiascorrect ants \*\_preproc.mif den_preproc_unbiased.mif -bias
bias.mif**

Note

The command above uses the -ants option, which requires that ANTs be
installed on your system. I recommend this program, but in case you are
unable to install it, you can replace it with the -fsl option.

You are now ready to create the mask with dwi2mask, which will restrict
your analysis to voxels that are located within the brain:

**dwi2mask den_preproc_unbiased.mif mask.mif;**

\#Check the output of this command by typing:

**mrview mask.mif;**

MRtrix's dwi2mask command works well in most scenarios. However, you can
see from the above image that there are a few holes in the mask within
the brainstem and the cerebellum. You may be uninterested in these
regions, but it is still a good idea to make sure the mask doesn't have
any holes anywhere.

To that end, you could use a command such as FSL's bet2. For example,
you could use the following code to convert the unbiased
diffusion-weighted image to NIFTI format, create a mask with bet2, and
then convert the mask to .mif format:

**mrconvert sub-02_den_preproc_unbiased.mif sub-02_unbiased.nii**

**bet2 sub-02_unbiased.nii sub-02_masked.nii -m -f 0.7**

**mrconvert sub-02_masked.nii mask.nii**

You may have to experiment with the fractional intensity threshold
(specified by -f) in order to generate a mask that you are satisfied
with.

You can check you bvals with:

**mrinfo \*\_den_preproc_unbiased.mif -shell_bvalues;**

**mrinfo \*\_den_preproc_unbiased.mif -shell_sizes;**

Select b values from preprocessed data (close to 1000) before fitting the tensor.
---------------------------------------------------------------------------------

**dwiextract -shell 0,1250 den_preproc_unbiased.mif
dwi_bval1245-55.mif**

DWI to Tensor
-------------

[[https://mrtrix.readthedocs.io/en/latest/reference/commands/dwi2tensor.html]{.ul}](https://mrtrix.readthedocs.io/en/latest/reference/commands/dwi2tensor.html)

**dwi2tensor -mask mask.mif \*\_bval1245-55.mif DTI.nii.gz**

Tensor to Metric
----------------

[[https://mrtrix.readthedocs.io/en/latest/reference/commands/tensor2metric.html?highlight=FA]{.ul}](https://mrtrix.readthedocs.io/en/latest/reference/commands/tensor2metric.html?highlight=FA)

**tensor2metric -fa FA.nii.gz -rd RD.nii.gz -adc MD.nii.gz DTI.nii.gz**

Make a mean b0 image:
---------------------

Create a mean b0 image form the DWI data that will represent almost a T2
weighted image an will help with coregistration:

**dwiextract den_preproc_unbiased.mif - -bzero \| mrmath - mean
mean_b0.mif -axis 3;**

\#Convert mean b0 image to nifti:

**mrconvert mean_b0.mif mean_b0.nii.gz;**

There are two parts to this command, separated by a pipe ("\|"). The
left half of the command, dwiextract, takes the preprocessed
diffusion-weighted image as an input, and the -bzero option extracts the
B0 images; the solitary - argument indicates that the output should be
used as input for the second part of the command, to the right of the
pipe. mrmath then takes these output B0 images and computes the mean
along the 3rd axis, or the time dimension. In other words, if we start
with an index of 0, then the number 3 indicates the 4th dimension, which
simply means to average over all of the volumes.

**Create ROIs from an Atlas**
-----------------------------

After converting the FA, MD, and RD images to MNI158 standard space, we
then need to select the ROIs that we will be using to analyze these
images.

There are many different ways to create ROIs, but we will be using an
atlas-based method.

We will be using FSL\'s JHU White Matter Tractography Atlas. This atlas
is located in the FSL directory under /usr/local/fsl/data/atlases/

If you are unsure of FSL\'s location on your computer, type \"which
fsl\" in the command line. This will tell you the location of the
folder, within which the /data/atlases/ folders will be.

There is a list of available regions and corresponding atlas codes in
the atlases folder (JHU-labels.xml and JHU-tracts.xml). This folder also
contains a sub-folder, JHU, which contains the atlas we will be using
(JHU-ICBM-labels-1mm.nii.gz). Copy this atlas into the directory
containing the FA/MD/RD images.

**cd ../T1;**

**cp \$FSLDIR/data/atlases/JHU/JHU-ICBM-labels-2mm.nii.gz .**

![](media/image2.png){width="6.267716535433071in"
height="4.916666666666667in"}

For our example, we will be using the splenium as our ROI (atlas code
\"5\").

To create the corpus callosum, corticospinal tract and optic radiation
ROI, enter the following command:

**fslmaths JHU-ICBM-labels-2mm.nii.gz -thr 3 -uthr 5
Corpus_Callosum.nii.gz; fslmaths JHU-ICBM-labels-2mm.nii.gz -thr 7 -uthr
8 Cortico_Spinal_Tract.nii.gz; fslmaths JHU-ICBM-labels-2mm.nii.gz -thr
29 -uthr 30 Optic_Radiation.nii.gz;**

JHU atlas to DTI Registration:
------------------------------

The nonlinear registration tool in FSL (called FNIRT) can only register
images of the same modality. Hence we will need to register the
T1-weighted image to the T1-weighted MNI template (MNI152_T1). In order
to run the nonlinear registration successfully we also need to
initialise it by a linear (12 DOF) registration, to get the orientation
and size of the image close enough for the nonlinear registration.
Furthermore, the nonlinear registration does not use the brain extracted
version, but the original (non-brain-extracted) image, so that any
errors in brain extraction do not influence the local registration,
whereas the linear registration does use the brain extracted versions
(as was done above).

Bet T1, correct it for field bias and do the neck cleanup(you should
already have it from the previous steps):

**bet T1.nii T1_bet_biascorr.nii.gz -f 0.5 -B**

To register the T1-weighted image to standard space requires the
following commands to be run:

**flirt -in T1_bet_biascorr.nii.gz -ref
\$FSLDIR/data/standard/MNI152_T1_2mm_brain.nii.gz -dof 12 -omat
T1_to_MNI.mat;**

**fnirt \--in=\*t1_mpr_iso\*.nii.gz \--aff=T1_to_MNI.mat
\--config=T1_2\_MNI152_2mm.cnf \--iout=T1toMNInonlin
\--cout=T1toMNI_coef \--fout=T1toMNI_warp;**

\#Invert warp:

**invwarp -r T1_bet_biascorr.nii.gz -w T1toMNI_warp.nii.gz -o
MNItoT1_warp;**

\#Register B0 to T1:

**flirt -in ../DWI/mean_b0.nii.gz -ref T1_bet_biascorr.nii.gz -omat
b0_to_T1.mat -dof 6;**

\#Invert mat:

**convert_xfm -omat T1_to_b0.mat -inverse b0_to_T1.mat;**

\#These two (**T1_to_b0.mat** and **MNItoT1_warp**) can now be used to
bring the selected tracts into DTI space with the command

**applywarp -r ../DWI/mean_b0.nii.gz -i Corpus_Callosum.nii.gz -w
MNItoT1_warp.nii.gz \--postmat=T1_to_b0.mat -o
JHU_Corpus_Callosum_in_b0.nii.gz;**

**applywarp -r ../DWI/mean_b0.nii.gz -i Cortico_Spinal_Tract.nii.gz -w
MNItoT1_warp.nii.gz \--postmat=T1_to_b0.mat -o
JHU_Cortico_Spinal_Tract_in_b0.nii.gz;**

**applywarp -r ../DWI/mean_b0.nii.gz -i Optic_Radiation.nii.gz -w
MNItoT1_warp.nii.gz \--postmat=T1_to_b0.mat -o
JHU_Optic_Radiation_in_b0.nii.gz;**

\#Binarise the masks:

**fslmaths JHU_Corpus_Callosum_in_b0.nii.gz -thr 0.5 -bin
../DWI/JHU_Corpus_Callosum_in_b0_bin.nii.gz;**

**fslmaths JHU_Cortico_Spinal_Tract_in_b0.nii.gz -thr 0.5 -bin
../DWI/JHU_Cortico_Spinal_Tract_in_b0_bin.nii.gz;**

**fslmaths JHU_Optic_Radiation_in_b0.nii.gz -thr 0.5 -bin
../DWI/JHU_Optic_Radiation_in_b0_bin.nii.gz;**

\#Use fsl stats to get mean DTI values in selected tracts:

**../DWI/;**

**echo FA;**

**echo mean FA in Corpus Callosum JHU;**

**fslstats FA.nii.gz -k JHU_Corpus_Callosum_in_b0_bin.nii.gz -M;**

**echo mean FA in Cortico Spinal Tract JHU;**

**fslstats FA.nii.gz -k JHU_Cortico_Spinal_Tract_in_b0_bin.nii.gz -M;**

**echo mean FA in Optic Radiation JHU;**

**fslstats FA.nii.gz -k JHU_Optic_Radiation_in_b0_bin.nii.gz -M;**

**echo MD;**

**echo mean MD in Corpus Callosum JHU;**

**fslstats MD.nii.gz -k JHU_Corpus_Callosum_in_b0_bin.nii.gz -M;**

**echo mean MD in Cortico Spinal Tract JHU;**

**fslstats MD.nii.gz -k JHU_Cortico_Spinal_Tract_in_b0_bin.nii.gz -M;**

**echo mean MD in Optic Radiation JHU;**

**fslstats MD.nii.gz -k JHU_Optic_Radiation_in_b0_bin.nii.gz -M;**

**echo RD;**

**echo mean RD in Corpus Callosum JHU;**

**fslstats RD.nii.gz -k JHU_Corpus_Callosum_in_b0_bin.nii.gz -M;**

**echo mean RD in Cortico Spinal Tract JHU;**

**fslstats RD.nii.gz -k JHU_Cortico_Spinal_Tract_in_b0_bin.nii.gz -M;**

**echo mean RD in Optic Radiation JHU;**

**fslstats RD.nii.gz -k JHU_Optic_Radiation_in_b0_bin.nii.gz -M;**

Make a mask of all NAWM apart from the optic radiation:
-------------------------------------------------------

Bet T1, correct it for field bias and do the neck cleanup (you should
already have it from the previous section):

**bet T1.nii T1_bet_biascorr.nii.gz -f 0.5 -B**

Segment T1 to get binary, thresholded (0.95 to avoid partial volume
effect) WM mask:

**../T1/;**

**fast T1_bet_biascorr.nii.gz; fslmaths T1_bet_biascorr_pve_2.nii.gz
-thr 0.95 -bin WM_mask.nii.gz;**

Register B0 to T1 (you should already have it from the previous
section):

**flirt -in ../DWI/mean_b0.nii.gz -ref T1_bet_biascorr.nii.gz -omat
b0_to_T1.mat -dof 6**

Invert the transformation:

**convert_xfm -inverse b0_to_T1.mat -omat T1_to_b0.mat**

Take T1 white matter into B0:

**flirt -in WM_mask.nii.gz -ref ../DWI/mean_b0.nii.gz -applyxfm -init
T1_to_b0.mat -out ../DWI/WM_in_DWI.nii.gz -interp nearestneighbour**

Co-register T2 FLAIR with B0 (by registering FLAIR to T1 and
concatenating matrices):

**flirt -in ../FLAIR/FLAIR_bet.nii.gz -ref T1_bet_biascorr.nii.gz -omat
FLAIR_to_T1.mat -dof 6**

convert_xfm -omat \'\'transf_A\_to_C.mat\'\' -concat
\'\'transf_B\_to_C.mat\'\' \'\'transf_A\_to_B.mat\'\'

**convert_xfm -omat FLAIR_to_b0.mat -concat T1_to_b0.mat
FLAIR_to_T1.mat**

Take lesion mask into B0 space:

**flirt -in ../FLAIR/FLAIR_lesion_mask.nii.gz -ref ../DWI/mean_b0.nii.gz
-applyxfm -init FLAIR_to_b0.mat -out ../DWI/lesions_in_b0.nii.gz -interp
nearestneighbour;**

Get DTI values for the lesioned WM:

Use fsl stats:

**../DWI/**

**echo mean FA in lesioned WM;**

**fslstats FA.nii.gz -k lesions_in_b0.nii.gz -M;**

**echo mean MD in lesioned WM;**

**fslstats MD.nii.gz -k lesions_in_b0.nii.gz -M;**

**echo mean RD in lesioned WM;**

**fslstats RD.nii.gz -k lesions_in_b0.nii.gz -M;**

**../T1/;**

\#Subtract lesion mask from white matter B0 (fsl maths):

**fslmaths ../DWI/lesions_in_b0.nii.gz -binv -mul
../DWI/WM_in_DWI.nii.gz ../DWI/WM_nolesion_b0.nii.gz**

\#Subtract optic radiation mask from white matter B0 (fsl maths):

**fslmaths ../DWI/JHU_Optic_Radiation_in_b0_bin -binv -mul
../DWI/WM_nolesion_b0.nii.gz ../DWI/NAWM_atlas.nii.gz**

\#Subtract optic radiation mask from white matter B0 (fsl maths)- in
case when pateint had no lesions:

**fslmaths ../DWI/JHU_Optic_Radiation_in_b0_bin -binv -mul
../DWI/WM_in_DWI.nii.gz ../DWI/NAWM_atlas.nii.gz**

\#Use fsl stats:

**../DWI/**

**echo mean FA in NAWM;**

**fslstats FA.nii.gz -k NAWM_atlas.nii.gz -M;**

**echo mean MD in NAWM;**

**fslstats MD.nii.gz -k NAWM_atlas.nii.gz -M;**

**echo mean RD in NAWM;**

**fslstats RD.nii.gz -k NAWM_atlas.nii.gz -M;**

**Create ROI from TractSeg (automatic neural network based tool to segment tracts in subjects native space)**
-------------------------------------------------------------------------------------------------------------

### In order to perform automatic tract segmentation we need to perform a constrained spherical deconvolution of the preprocessed DWI data:

**dwi2response dhollander den_preproc_unbiased.mif wm.txt gm.txt csf.txt
-voxels voxels.mif**

Let's unpack what this command does. First, it uses an algorithm to
deconvolve the fiber orientation distributions (FODs) - in other words,
it tries to decompose the diffusion signal into a set of smaller
individual fiber orientations. You have several algorithms to choose
from, but the most common are tournier and dhollander. The tournier
algorithm is used for single-shell data and for a single tissue type
(e.g., white matter). The dhollander algorithm can be used for either
single- or multi-shell data, and for multiple tissue types. Estimating
the FOD for each tissue type will later help us do anatomically
constrained tractography.

The next argument specifies your input data, and the resulting response
functions for the different tissue types. The order matters; you can
call the output files whatever you want, but it makes the most sense to
label them as some kind of variation on the phrases "white matter",
"grey matter", and "cerebrospinal fluid" (here, labeled as "wm.txt",
"gm.txt", and "csf.txt"). The last option, "-voxels", specifies an
output dataset that shows which voxels from the image were used to
construct the basis functions for each tissue type. This dataset can be
viewed by typing the following:

**mrview preproc_unbiased.mif -overlay.load voxels.mif**

Fiber Orientation Density (FOD)

We will now use the basis functions generated above to create **Fiber
Orientation Densities**, or FODs. These are estimates of the amount of
diffusion in each of three orthogonal directions. As described in the
[[introductory
chapter]{.ul}](https://andysbrainbook.readthedocs.io/en/latest/MRtrix/MRtrix_Course/MRtrix_00_Diffusion_Overview.html#mrtrix-00-diffusion-overview),
these are analogous to the tensors that are used in traditional
diffusion studies. However, MRtrix allows for the estimation of multiple
crossing fibers within a single voxel, and can resolve the diffusion
signal into multiple directions.

To do this, we will use the command dwi2fod to apply the basis functions
to the diffusion data. The "-mask" option specifies which voxels we will
use; this is simply to restrict our analysis to brain voxels and reduce
the computing time. The ".mif" files specified after each basis function
will output an FOD image for that tissue type:

**dwi2fod msmt_csd den_preproc_unbiased.mif -mask mask.mif wm.txt
wmfod.mif gm.txt gmfod.mif csf.txt csffod.mif**

Now we have obtained the FOD file for WM (wmfod.mif), which we need in
order to calculate the peaks of a spherical harmonic function in each
voxel. We do it by:

**sh2peaks wmfod.mif peaks.nii.gz**

Lastly we use the peaks.nii.gz as an input for TractSeg for tract
segmentation.

**TractSeg -i peaks.nii.gz**

The binary masks of tracts are then saved in the TractSeg output
directory.

Bundle names:

**0: AF_left (Arcuate fascicle)**

**1: AF_right**

**2: ATR_left (Anterior Thalamic Radiation)**

**3: ATR_right**

**4: CA (Commissure Anterior)**

**5: CC_1 (Rostrum)**

**6: CC_2 (Genu)**

**7: CC_3 (Rostral body (Premotor))**

**8: CC_4 (Anterior midbody (Primary Motor))**

**9: CC_5 (Posterior midbody (Primary Somatosensory))**

**10: CC_6 (Isthmus)**

**11: CC_7 (Splenium)**

**12: CG_left (Cingulum left)**

**13: CG_right**

**14: CST_left (Corticospinal tract)**

**15: CST_right**

**16: MLF_left (Middle longitudinal fascicle)**

**17: MLF_right**

**18: FPT_left (Fronto-pontine tract)**

**19: FPT_right**

**20: FX_left (Fornix)**

**21: FX_right**

**22: ICP_left (Inferior cerebellar peduncle)**

**23: ICP_right**

**24: IFO_left (Inferior occipito-frontal fascicle)**

**25: IFO_right**

**26: ILF_left (Inferior longitudinal fascicle)**

**27: ILF_right**

**28: MCP (Middle cerebellar peduncle)**

**29: OR_left (Optic radiation)**

**30: OR_right**

**31: POPT_left (Parieto‐occipital pontine)**

**32: POPT_right**

**33: SCP_left (Superior cerebellar peduncle)**

**34: SCP_right**

**35: SLF_I\_left (Superior longitudinal fascicle I)**

**36: SLF_I\_right**

**37: SLF_II_left (Superior longitudinal fascicle II)**

**38: SLF_II_right**

**39: SLF_III_left (Superior longitudinal fascicle III)**

**40: SLF_III_right**

**41: STR_left (Superior Thalamic Radiation)**

**42: STR_right**

**43: UF_left (Uncinate fascicle)**

**44: UF_right**

**45: CC (Corpus Callosum - all)**

**46: T_PREF_left (Thalamo-prefrontal)**

**47: T_PREF_right**

**48: T_PREM_left (Thalamo-premotor)**

**49: T_PREM_right**

**50: T_PREC_left (Thalamo-precentral)**

**51: T_PREC_right**

**52: T_POSTC_left (Thalamo-postcentral)**

**53: T_POSTC_right**

**54: T_PAR_left (Thalamo-parietal)**

**55: T_PAR_right**

**56: T_OCC_left (Thalamo-occipital)**

**57: T_OCC_right**

**58: ST_FO_left (Striato-fronto-orbital)**

**59: ST_FO_right**

**60: ST_PREF_left (Striato-prefrontal)**

**61: ST_PREF_right**

**62: ST_PREM_left (Striato-premotor)**

**63: ST_PREM_right**

**64: ST_PREC_left (Striato-precentral)**

**65: ST_PREC_right**

**66: ST_POSTC_left (Striato-postcentral)**

**67: ST_POSTC_right**

**68: ST_PAR_left (Striato-parietal)**

**69: ST_PAR_right**

**70: ST_OCC_left (Striato-occipital)**

**71: ST_OCC_right**

Combine lh and rh Optic Radiation and Cortico Spinal tracts:

**cd** **tractseg_output/bundle_segmentations/;**

**fslmaths OR_left.nii.gz -add OR_right.nii.gz
../../OR_TractSeg.nii.gz;**

**fslmaths CST_left.nii.gz -add CST_right.nii.gz
../../CST_TractSeg.nii.gz;**

**\...;**

Obtain DTI values from selected tractseg ROIs:

**echo FA;**

**echo mean FA in Corpus Callosum TractSeg;**

**fslstats FA.nii.gz -k tractseg_output/bundle_segmentations/CC.nii.gz
-M;**

**echo mean FA in Cortico Spinal Tract TractSeg;**

**fslstats FA.nii.gz -k CST_TractSeg.nii.gz -M;**

**echo mean FA in Optic Radiation TractSeg;**

**fslstats FA.nii.gz -k OR_TractSeg.nii.gz -M;**

**echo MD;**

**echo mean MD in Corpus Callosum TractSeg;**

**fslstats MD.nii.gz -k tractseg_output/bundle_segmentations/CC.nii.gz
-M;**

**echo mean MD in Cortico Spinal Tract TractSeg;**

**fslstats MD.nii.gz -k CST_TractSeg.nii.gz -M;**

**echo mean MD in Optic Radiation TractSeg;**

**fslstats MD.nii.gz -k OR_TractSeg.nii.gz -M;**

**echo RD;**

**echo mean RD in Corpus Callosum TractSeg;**

**fslstats RD.nii.gz -k tractseg_output/bundle_segmentations/CC.nii.gz
-M;**

**echo mean RD in Cortico Spinal Tract TractSeg;**

**fslstats RD.nii.gz -k CST_TractSeg.nii.gz -M;**

**echo mean RD in Optic Radiation TractSeg;**

**fslstats RD.nii.gz -k OR_TractSeg.nii.gz -M;**

Concat all tractseg output tracts to create WM mask:

**cd tractseg_output/bundle_segmentations/**

**ls \> list_all.txt;**

**awk \'{print \"-add \" \$0;}\' list_all.txt \> list_add.txt;**

**sed \'/list/d\' list_add.txt \> list_clean.txt;**

**sed \'s/-add AF_left.nii.gz/AF_left.nii.gz/\' list_clean.txt \>
ready_to_merge.txt;**

**fslmaths \$(cat ready_to_merge.txt) ../../WM_mask_TractSeg.nii.gz;**

**../../;**

\#Binarise mask:

**fslmaths WM_mask_TractSeg.nii.gz -thr 0.5 -bin
WM_mask_TractSeg_bin.nii.gz;**

\#Subtract Optic Radiation from the WM mask:

**fslmaths OR_TractSeg.nii.gz -binv -mul WM_mask_TractSeg_bin.nii.gz
WM_mask_no_OR_TractSeg_bin.nii.gz;**

**\#in case there were no lesions**

**\#fslmaths OR_TractSeg.nii.gz -binv -mul WM_mask_TractSeg_bin.nii.gz
NAWM_TractSeg.nii.gz;**

\#Subtract lesion mask from WM mask:

**fslmaths lesions_in_b0.nii.gz -binv -mul
WM_mask_no_OR_TractSeg_bin.nii.gz NAWM_TractSeg.nii.gz;**

\#Use fsl stats:

**echo mean FA in NAWM TractSeg;**

**fslstats FA.nii.gz -k NAWM_TractSeg.nii.gz -M;**

**echo mean MD in NAWM TractSeg;**

**fslstats MD.nii.gz -k NAWM_TractSeg.nii.gz -M;**

**echo mean RD in NAWM TractSeg;**

**fslstats RD.nii.gz -k NAWM_TractSeg.nii.gz -M;**

**MD units explanation:**

[[http://dti-tk.sourceforge.net/pmwiki/pmwiki.php?n=Documentation.Diffusivity]{.ul}](http://dti-tk.sourceforge.net/pmwiki/pmwiki.php?n=Documentation.Diffusivity)

**Calculate NODDI parameters:**
-------------------------------

What is NODDI and how to get the toolbox?

<http://mig.cs.ucl.ac.uk/index.php?n=Tutorial.NODDImatlab>

Parepare necessary files:

When in DWI folder:

**\#brain mask file to restrict model fit only to selected voxels**

**mrconvert mask.mif mask.nii**

**\#preprocessed DWI image**

**mrconvert den_preproc_unbiased.mif den_preproc_unbiased.nii**

**\#the right bval and bvec files from the main Anterior-Posterior
encoding direction**

**echo \*AP\*.bvec \*AP\*.bval**

When ready open **matlab** and run:

Navigate to the subject's DWI directory:

**cd
/Users/paweljakuszyk/Desktop/NAWA_PARTICIPANTS/001_MS_F\_TP1/Brain/DWI**

Then run:

**CreateROI(\'den_preproc_unbiased.nii\', \'mask.nii\',
\'NODDI_roi.mat\');**

The second argument specifies the ROI mask which defines the foreground
voxels for model fitting. In practice, the mask should generally be
inclusive of the entire brain. For the purpose of this tutorial, we will
start with a region consisting of just a single axial slice. The third
argument specifies the name of the mat file for outputting the resulting
data formatted for subsequent analysis. The NODDI model fitting involves
non-linear optimization and hence is computational intensive. For
efficiency, always create a good brain mask that excludes voxels that do
not need to be fitted.

**NOTE**: The 4-D DWI volumes and the 3-D ROI mask volume can be in the
NIfTI or Analyze formats. But the files should NOT be gizipped, i.e.,
with gz as a suffix (e.g. nii.gz or img.gz)

Convert the FSL bval/bvec files into the required format with the
function FSL2Protocol:

**protocol = FSL2Protocol(\' \*AP\*.bvec', '\*AP\*.bval\', 10);**

The third argument "10" is meant to round up all the bvals in range
(0-10) to 0 in order to avoid crashing when fitting the model.

Create the NODDI model structure with the function MakeModel:

**noddi = MakeModel(\'WatsonSHStickTortIsoV_B0\');**

\'WatsonSHStickTortIsoV_B0\' is the internal name for the NODDI model.
The structure noddi holds the details of the NODDI model relevant for
the subsequent fitting. For most users, the default setting should
suffice.

Run the NODDI fitting with the function batch_fitting, if you have the
parallel computing toolbox, or batch_fitting_single, if you do not:

**batch_fitting(\'NODDI_roi.mat\', protocol, noddi,
\'FittedParams.mat\', 8);**

The first three arguments to the function are explained in the previous
steps. The fourth argument specifies the mat file name to store the
estimated NODDI parameters. The final argument sets the number of
computing cores to use for running the fitting in parallel. This
argument is optional. If not specified, the function will let Matlab
choose the default setting. On a 8-core machine, the fitting should
finish in around 15 minutes. - bullshit it will take at least several
hours (possibly due to the new matlab realease cockcing it up).

If a run is interrupted by an unexpected system reboot or crash, or by a
necessary stoppage, simply repeat the same command again. It will resume
the interrupted run from the last voxel for which the estimated
parameters are saved.(**NEW**)

The usage for batch_fitting_single is similar:

**batch_fitting_single(\'NODDI_roi.mat\', protocol, noddi,
\'FittedParams.mat\');**

Similar to batch_fitting, this function supports the resumption of an
interrupted fitting run.(**NEW**)

Convert the estimated NODDI parameters into volumetric parameter maps:

**SaveParamsAsNIfTI(\'FittedParams.mat\', \'NODDI_roi.mat\',
\'mask.nii\', \'Subject_ID\');**

This function converts the fitted parameters (1st argument) into NIfTI
formatted volumes with the same spatial dimension as the original image,
specified by the brain mask (3rd argument). The function also requires
as input the roi file (2nd argument). In addition, you also need to
specify a prefix to the output volumes with the final argument.

If you use this function with a FittedParams.mat from an interrupted
fitting run, from Version 1.04, the function will abort and will advise
you to re-run the interrupted run.

At this point, you should find the following output volumes:

-   Neurite density (or intra-cellular volume fraction):
    > example_ficvf.nii

-   Orientation dispersion index (ODI): example_odi.nii

-   CSF volume fraction: example_fiso.nii

-   Fibre orientation: example_fibredirs\_{x,y,z}vec.nii

-   Fitting objective function values: example_fmin.nii

-   Concentration parameter of Watson distribution used to compute ODI:
    > example_kappa.nii

-   Error code: example_error_code.nii (**NEW**) Nonzero values indicate
    > fitting errors.

**Create cortical ribbon mask and extract mean diffusivity (MD):**
------------------------------------------------------------------

mris_volmask - computes a volumetric mask based on the white and pial
surfaces. The mask contains 4 labels, namely LEFT_WHITE, LEFT_GREY,
RIGHT_WHITE, RIGHT_GREY, which are computed based on the white and pial
surfaces.

**mris_volmask \[ options \] subject**

**mris_volmask \--save_ribbon Pilot_X**

This creates two cortical ribbon masks in the Freesurfers subject
directory lh/rh.ribbon.mgz and those masks are in the subject's T1
space.

**/Applications/freesurfer/7.1.1/subjects/Pilot_x/mri**

Convert mgz to nifti:

**mrconvert rh.ribbon.mgz rh.ribbon.nii.gz; mrconvert lh.ribbon.mgz
lh.ribbon.nii.gz;**

Combine lh and rh cortical ribbon masks:

**fslmaths rh.ribbon.nii.gz -add lh.ribbon.nii.gz
cort.ribbon.mask.nii.gz**

Reorient the mask to standard space:

**fslreorient2std cort.ribbon.mask.nii.gz cort.ribbon.mask.2std.nii.gz**

Move it to participants folder (only for me because it happens on a
different PC).

**mv cort.ribbon.mask.2std.nii.gz
../../../../../../Users/pawel/Desktop/NAWA_PARTICIPANTS/003_MS_M\_TP1/T1/cort.ribbon.mask.2std.nii.gz**

Bet T1 (you should already have it from the previous steps):

**bet scans_t1_mpr_iso_20210723114038_5.nii t1_bet.nii.gz -f 0.4**

Register cortical ribbon mask to T1 (just slight FOV change):

**flirt -in cort.ribbon.mask.2std.nii.gz** **-ref T1_bet_biascorr.nii.gz
-out cort.ribbon.mask.2T1.nii.gz -omat cort.ribbon.mask.2T1.mat -dof 6
-cost normmi -interp nearestneighbour;**

Register the T1-weighted image to mean b0 image (skip if you already
have it from the previous steps):

**flirt -in FA.nii.gz -ref T1_brain.nii.gz -out FAtoT1 -omat FAtoT1.mat
-dof 6 -cost normmi**

To invert a saved transformation:

**convert_xfm -omat T1toFA.mat -inverse FAtoT1.mat**

\#Use the .mat file to register the cortical ribbon mask to DTI space:

**flirt -in cort.ribbon.mask.2T1.nii.gz -ref ../DWI/mean_b0.nii.gz -out
../DWI/cortical.ribbon_2\_DWI.nii.gz -init T1_to_b0.mat -applyxfm
-interp nearestneighbour;**

\#Extract the mean MD in the corex:

**../DWI/;**

**echo mean MD in the cortex;**

**fslstats MD.nii.gz -k cortical.ribbon_2\_DWI.nii.gz -M;**

**echo mean FA in the cortex;**

**fslstats FA.nii.gz -k cortical.ribbon_2\_DWI.nii.gz -M;**

**echo mean RD in the cortex;**

**fslstats RD.nii.gz -k cortical.ribbon_2\_DWI.nii.gz -M;**

Spinal Cord Toolbox step by step through CSA (cross sectional area) to DWI
==========================================================================

**What do we get out of it:**

-   **mean cord area per vertebrae \[C2-C7\]**

-   **mean gm and wm area based on T2\* image \[15 slices\]**

-   **DTI measures FA,MD,AD,RD**

1.  Spinal cord segmentation **use T2**

\# Go to T2 contrast cd data/t2 \# Spinal cord segmentation. Note the
flag \"-qc\" to generate a QC report of the segmentation.

sct_propseg -i t2.nii.gz -c t2 -qc \~/qc_singleSubj

\# To check the QC report, double click on the file
qc_singleSubj/qc/index.html which has been created in your home
directory

**ALTERNATIVE -use it!!!**

\# Try cord segmentation using deep learning

**sct_deepseg_sc -i \*T2w\*.nii.gz -c t2 -ofolder deepseg -qc
../qc_spine**

\# Check QC report: Go to your browser and do \"refresh\".

\# Optional: Check results in FSLeyes (if installed). In red: PropSeg,
in green: DeepSeg. Tips: use CMD+f (or CTRL+f on Linux) to switch
overlay on/off.

**fsleyes t1.nii.gz -cm greyscale t1_seg.nii.gz -cm red -a 70.0
deepseg/t1_seg.nii.gz -cm green -a 70.0 &**

2.  Label vertebrae - we need 2 mid-vertebrae points at C3 and T2 in
    > order to register image to the template

\# Vertebral labeling

**sct_label_vertebrae -i \*T2w\*.nii.gz -s deepseg/\*T2w\_\*\_seg.nii.gz
-c t2 -qc ../qc_spine**

\# Check QC report: Go to your browser and do \"refresh\".

\# Note: Here, two files are output: t2_seg_labeled, which represents
the labeled segmentation (i.e., the value corresponds to the vertebral
level), and t2_seg_labeled_discs, which only has a single point for each
inter-vertebral disc level. The convention is: Value 3 ---\> C2-C3 disc,
Value 4 ---\> C3-C4 disc, etc.

\# Create labels at C3 and T2 mid-vertebral levels. These labels are
needed for template registration. **-**

**sct_label_utils -i \*T2w\_\*\_seg_labeled.nii.gz -vert-body 3,9 -o
t2_labels_vert.nii.gz**

**Label the discs manually for cord area estimates:**

\# You might want to completely bypass sct_label_vertebrae and do the
labeling manually. In that case, we provide a viewer to do so
conveniently. \# In the example below, we will create labels at the
inter-vertebral discs C2-C3 (value=3), C3-C4 (value=4) and C4-C5
(value=5).

**sct_label_utils -i \*T2w\_\*.nii.gz -create-viewer 2,3,4,5,6,7 -o
t2_labels_vert_CSA.nii.gz -msg \"Place labels at the centre of a cord at
the mid-vertebral level E.g. Label 2: C2, Label 7: C7.\"**

3.  Register to template

\# Register t2 to template.

**sct_register_to_template -i \_T2w\_\*.nii.gz -s
deepseg/\*T2w\_\*\_seg.nii.gz -l t2_labels_vert.nii.gz -c t2 -qc
../qc_spine**

\# **Probably better to use deepL segmentation!** Note: By default the
PAM50 template is selected. You can also select your own template using
flag -t.

4.  Warp template

\# Warp template objects (T1, cord segmentation, vertebral levels,
etc.). Here we use -a 0 because we don't need the white matter atlas at
this point.

**sct_warp_template -d T2w\_\*.nii.gz -w warp_template2anat.nii.gz -a 0
-qc ../qc_spine**

\# Note: A folder label/template/ is created, which contains template
objects in the space of the subject. The file info_label.txt lists all
template files.

5.  Compute CSA

\# Compute cross-sectional area (CSA) of spinal cord and average it
across levels C3 and C4

**sct_process_segmentation -i t2_seg.nii.gz -vert 3:4 -o csa_c3c4.csv**

\# Note: the \"-vert\" flag assumes the existence of the vertebral
labeling file:  ./label/template/PAM50_level.nii.gz.  You can point to
another vertebral level file using the flag "-vertfile"

**sct_process_segmentation -i t2_seg.nii.gz -vert 3:4 -vertfile
t2_seg_labeled.nii.gz -o csa_c3c4.csv**

Alternatively **- variable!**

**\# Aggregate CSA value per level -what we will use!**

**sct_process_segmentation -i deepseg/\*T2w\_\*\_seg.nii.gz -vert
2,3,4,5,6,7 -vertfile t2_labels_vert_CSA.nii.gz -perlevel 1 -o
csa_perlevel.csv;**

**open csa_perlevel.csv;**

\# Aggregate CSA value per slices

**sct_process_segmentation -i t2_seg.nii.gz -z 30:35 -perslice 1 -o
csa_perslice.csv**

6.  Segment GM and WM on a T2\* image

\# Go to T2\*-weighted data, which has good GM/WM contrast and high
in-plane resolution

**../GRE_ME;**

\# Spinal cord segmentation

**sct_deepseg_sc -i \*GRE-ME\_\*.nii.gz -c t2s -qc ../qc_spine**

\# Segment gray matter (check QC report afterwards)

**sct_deepseg_gm -i \*GRE-ME\_\*.nii.gz -qc ../qc_spine**

\# Subtract GM segmentation from cord segmentation to obtain WM
segmentation

**sct_maths -i \*\_seg.nii.gz -sub \*\_gmseg.nii.gz -o
t2s_wmseg.nii.gz**

7.  GM-informed template registration

\# Register template-\>t2s (using warping field generated from
template\<-\>t2 registration) \# Tips: Here we use the WM seg for the
iseg/dseg fields in order to account for both the cord and the GM shape.

**sct_register_multimodal -i
\${SCT_DIR}/data/PAM50/template/PAM50_t2s.nii.gz -iseg
\${SCT_DIR}/data/PAM50/template/PAM50_wm.nii.gz -d t2s.nii.gz -dseg
t2s_wmseg.nii.gz -param
step=1,type=seg,algo=rigid:step=2,type=seg,algo=bsplinesyn,slicewise=1,iter=3
-initwarp ../t2/warp_template2anat.nii.gz -initwarpinv
../t2/warp_anat2template.nii.gz -qc ../qc_spine**

\# rename warping fields for clarity

**mv warp\*PAM50\_\*GRE_ME\*.nii.gz warp_template2t2s.nii.gz;**

**mv warp\*GRE_ME\*PAM50\*.nii.gz warp_t2s2template.nii.gz;**

\# Warp template

**sct_warp_template -d t2s.nii.gz -w warp_template2t2s.nii.gz -qc
../qc_spine**

8.  CSA of GM and WM **-variable!**

\# Compute cross-sectional area (CSA) of the gray and white matter for
all slices in the volume.

\# Note: Here we use the flag -angle-corr 0, because we do not want to
correct the computed CSA by the cosine of the angle between the cord
centerline and the S-I axis: we assume that slices were acquired
orthogonally to the cord.

**sct_process_segmentation -i \*\_gmseg.nii.gz -o csa_gm.csv -angle-corr
0; sct_process_segmentation -i \*\_wmseg.nii.gz -o csa_wm.csv
-angle-corr 0;**

**open csa_gm.csv csa_wm.csv;**

9.  DMRI data

\# merge b0 and dwi to have a better DWI image

**sct_dmri_concat_b0_and_dwi -i \*b0\*.nii.gz \*DWI_2\*.nii.gz -bvec
\*DWI\*.bvec -bval \*DWI\*.bval -order b0 dwi -o dmri_concat.nii.gz
-obval bvals_concat.txt -obvec bvecs_concat.txt**

\# Compute mean dMRI from dMRI data

**sct_maths -i dmri_concat.nii.gz -mean t -o dmri_mean.nii.gz**

\# Segment SC on mean dMRI data

\# Note: This segmentation does not need to be accurate\-- it is only
used to create a mask around the cord

**sct_propseg -i dmri_mean.nii.gz -c dwi -qc ../qc_spine**

\# Create mask (for subsequent cropping)

**sct_create_mask -i dmri_mean.nii.gz -p centerline,dmri_mean_seg.nii.gz
-size 35mm**

\# Crop data for faster processing

**sct_crop_image -i dmri_concat.nii.gz -m mask_dmri_mean.nii.gz -o
dmri_crop.nii.gz**

\# Motion correction (moco)

**sct_dmri_moco -i dmri_crop.nii.gz -bvec bvecs_concat.txt**

10. Register template to dMRI

\# Segment SC on motion-corrected mean dwi data (check results in the QC
report)

**sct_propseg -i dmri_crop_moco_dwi_mean.nii.gz -c dwi -qc ../qc_spine**

**\#sometimes using -c t1 gives better results than dwi and sometimes it
might be better to segment DWi using deepseg:**

**\#sct_deepseg_sc -i dmri_crop_moco_dwi_mean.nii.gz -c dwi -qc
../qc_spine**

\# Register template-\>dwi via t2s to account for GM segmentation

\# Tips: In general for DWI we use the PAM50_t1 contrast, which is close
to the dwi contrast (although here we are not using type=im in -param,
so it will not make a difference).

\# Note: the flag \"-initwarpinv\" provides a transformation
dmri-\>template, in case you would like to bring all your DTI metrics in
the PAM50 space (e.g. group averaging of FA maps)

**sct_register_multimodal -i
\$SCT_DIR/data/PAM50/template/PAM50_t1.nii.gz -iseg
\$SCT_DIR/data/PAM50/template/PAM50_cord.nii.gz -d
dmri_crop_moco_dwi_mean.nii.gz -dseg dmri_crop_moco_dwi_mean_seg.nii.gz
-param
step=1,type=seg,algo=centermass:step=2,type=seg,algo=bsplinesyn,slicewise=1,iter=3
-initwarp ../GRE_ME/warp_template2t2s.nii.gz -initwarpinv
../GRE_ME/warp_t2s2template.nii.gz -qc ../qc_spine**

\# Rename warping fields for clarity

**mv warp_PAM50_t12dmri_crop_moco_dwi_mean.nii.gz
warp_template2dmri.nii.gz; mv
warp_dmri_crop_moco_dwi_mean2PAM50_t1.nii.gz
warp_dmri2template.nii.gz;**

\# Warp template

**sct_warp_template -d dmri_crop_moco_dwi_mean.nii.gz -w
warp_template2dmri.nii.gz -qc ../qc_spine**

\# Check results in the QC report

11. Compute DTI **- variables!**

\# Compute DTI metrics using dipy \[1\]

**sct_dmri_compute_dti -i dmri_crop_moco.nii.gz -bval bvals_concat.txt
-bvec bvecs_concat.txt;**

\# Tips: the flag \"-method restore\" estimates the tensor with robust
fit (RESTORE method \[2\]) \# Compute FA,MD,RD within the white matter
for all slices

**sct_extract_metric -i dti_FA.nii.gz -perslice 0 -method map -l 51 -o
FA_in_wm_spine.csv;**

**sct_extract_metric -i dti_MD.nii.gz -perslice 0 -method map -l 51 -o
MD_in_wm_spine.csv;**

**sct_extract_metric -i dti_RD.nii.gz -perslice 0 -method map -l 51 -o
RD_in_wm_spine.csv**

**open FA_in_wm_spine.csv &;open MD_in_wm_spine.csv &; open
RD_in_wm_spine.csv &**

Myelin Water Fraction (MWF)
===========================

Vista toolbox (matlab):

Run **vista_save_no_extension_name** via matlab and as the **first
dicom** load the one from participants **MWF VISTA (ViSTa3D series)
folder**, the **second** one comes from **REF_FA28 (GRE3D series)
folder**. The result will be a ready nifti file with a MWF map.

In line 124 change the output folder to a desired participant\'s folder:

**cd /Users/paweljakuszyk/Desktop/Pilots/MS_PJ/MWF/;**

Lesions MWF:
------------

Copy header information from nifti file directly converted form the
dicoms (e.g. via dc2niix), because somehow the header info is lost in
creating MWF image with matlab code.:

**fslcpgeom \*\_ViSTa_2mm\*.nii.gz vista3D.nii**

Bet the MWF (you have to review the procedure very carefully because the
extraction is slight, should be just enough to cut out the artefact
signal coming from skull and surrounding tissue), adjust the f parameter
accordingly based on visual inspection, robust option is on in order to
improve the brain extraction when the input data contains a lot of
non-brain matter - most likely when there is a lot of neck included in
the input image. By iterating in this way the centre-of-gravity should
move up each time towards the true centre, resulting in a better final
estimate. The iterations stop when the centre-of-gravity stops moving,
up to a maximum of 10 iterations:

**bet vista3D.nii MWF_bet.nii.gz -R -f 0.2; mrview MWF_bet.nii.gz&**

Register MWF to T1:

**../T1/**

**flirt -in ../MWF/MWF_bet.nii.gz -ref T1_bet_biascorr.nii.gz -out
MWF_to_T1.nii.gz -omat MWF_to_T1.mat -dof 6;**

**\#check your results**

**fsleyes T1_bet_biascorr.nii.gz MWF_to_T1.nii.gz &;**

Invert the transformation:

**convert_xfm -inverse MWF_to_T1.mat -omat T1_to_MWF.mat**

Concat the matrices (you should have the FLAIR_to_T1.mat from DTI
section):

convert_xfm -omat \'\'transf_A\_to_C.mat\'\' -concat
\'\'transf_B\_to_C.mat\'\' \'\'transf_A\_to_B.mat\'\'

**convert_xfm -omat FLAIR_to_MWF.mat -concat T1_to_MWF.mat
FLAIR_to_T1.mat**

Use the acquired matrix to transform FLAIR lesion mask into MWF space:

**flirt -in ../FLAIR/FLAIR_lesion_mask.nii.gz -ref ../MWF/vista3D.nii
-applyxfm -init FLAIR_to_MWF.mat -out
../MWF/FLAIR_lesion_mask_MWF.nii.gz -interp nearestneighbour**

**\#quick QC check**

**../MWF/**

**fsleyes vista3D.nii FLAIR_lesion_mask_MWF.nii.gz &**

**\#Use fsl stats:**

**echo mean MWF in lesions;**

**fslstats vista3D.nii -k FLAIR_lesion_mask_MWF.nii.gz -M;**

NAWM from JHU atlas MWF:
------------------------

Register MWF to T1 (you should already have it from the previous step):

**flirt -in ../MWF/MWF.nii.gz -ref T1_bet_biascorr.nii.gz -omat
MWF_to_T1.mat -dof 6**

Concat the matrices (you should have the b0_to_T1.mat from DTI section):

convert_xfm -omat \'\'transf_A\_to_C.mat\'\' -concat
\'\'transf_B\_to_C.mat\'\' \'\'transf_A\_to_B.mat\'\'

**../T1/**

**convert_xfm -omat b0_to_MWF.mat -concat T1_to_MWF.mat b0_to_T1.mat**

Use the acquired matrix to transform NAWM without OR into MWF space:

**flirt -in ../DWI/NAWM_atlas.nii.gz -ref ../MWF/MWF_bet.nii.gz
-applyxfm -init b0_to_MWF.mat -out ../MWF/NAWM_atlas_in_MWF.nii.gz
-interp nearestneighbour**

\#Use fsl stats:

**../MWF/**

**echo mean MWF in NAWM Atlas;**

**fslstats vista3D.nii -k NAWM_atlas_in_MWF.nii.gz -M;**

NAWM from Tractseg MWF:
-----------------------

Register MWF to T1 (you should already have it from the previous step):

**flirt -in ../MWF/MWF.nii.gz -ref T1_bet_biascorr.nii.gz -omat
MWF_to_T1.mat -dof 6**

Concat the matrices (you should have the b0_to_T1.mat from DTI section):

convert_xfm -omat \'\'transf_A\_to_C.mat\'\' -concat
\'\'transf_B\_to_C.mat\'\' \'\'transf_A\_to_B.mat\'\'

**convert_xfm -omat b0_to_MWF.mat -concat T1_to_MWF.mat b0_to_T1.mat**

Use the acquired matrix to transform NAWM without OR into MWF space:

**../T1/**

**flirt -in ../DWI/NAWM_TractSeg.nii.gz -ref ../MWF/MWF_bet.nii.gz
-applyxfm -init b0_to_MWF.mat -out ../MWF/NAWM_TractSeg_in_MWF.nii.gz
-interp nearestneighbour**

**\#Use fsl stats:**

**../MWF/**

**echo mean MWF in NAWM TractSeg;**

**fslstats vista3D.nii -k NAWM_TractSeg_in_MWF.nii.gz -M;**

T1 relaxometry
==============

### Calculate R1 relaxation in the basal ganglia:

Make a basal ganglia mask by segmenting using T1 nad fsl_first (putamen,
caudate and pallidum):

**run_first_all -i \*t1_mpr_iso\_\*.nii.gz -s
L_Caud,L_Pall,L_Puta,R_Caud,R_Pall,R_Puta -o basal_ganglia_seg.nii.gz**

Binarize the mask:

**fslmaths basal_ganglia_seg_all_none_firstseg.nii.gz -bin
basal_ganglia_mask.nii.gz**

Register the mask to R2\* map (basically magnitude header):

Bet T1, correct it for field bias and do the neck cleanup:

**bet \*t1_mpr_iso\_\*.nii.gz T1_bet_biascorr.nii.gz -f 0.5 -B;**

\#Always check your bet results and just -f value accordingly!

**mrview \*t1_mpr_iso\_\*.nii.gz -overlay.load T1_bet_biascorr.nii.gz
&;**

Bet the t1map (bet functions better with it rather than r1map and they
are both in the same space) image use robust option because of the noisy
maps:

**../MP2RAGE/;**

**bet t1map.nii t1map_bet.nii.gz -R -f 0.4 -R;**

**mrview t1map.nii -overlay.load t1map_bet.nii.gz &;**

**../T1/;**

\#Register the t1map image to T1:

**flirt -in ../MP2RAGE/t1map_bet.nii.gz -ref T1_bet_biascorr.nii.gz
-omat t1map_to_t1.mat -dof 6 -cost normmi;**

\#To invert a saved transformation:

**convert_xfm -omat t1_to_t1map.mat -inverse t1map_to_t1.mat;**

\#Use the .mat file to register the basal ganglia mask to R2s space:

**flirt -in basal_ganglia_mask.nii.gz -ref ../MP2RAGE/t1map_bet.nii.gz
-out ../MP2RAGE/basal_ganlgia_mask_2\_t1map.nii.gz -init t1_to_t1map.mat
-applyxfm -interp nearestneighbour;**

**../MP2RAGE/;**

**mrview t1map_bet.nii.gz -overlay.load
basal_ganlgia_mask_2\_t1map.nii.gz&;**

\#Extract the mean R1 in the basal ganglia:

**echo R1 in the basal ganglia;**

**fslstats r1map.nii -k basal_ganlgia_mask_2\_t1map.nii.gz -M;**

**../T1/;**

### Calculate R1 relaxation in lesions:

Register FLAIR to r1map by concatenating the matices:

**convert_xfm -omat FLAIR_to_t1map.mat -concat t1_to_t1map.mat
FLAIR_to_T1.mat**

Use the .mat file to register FLAIR lesion mask to R1 space:

**flirt -in ../FLAIR/FLAIR_lesion_mask.nii.gz -ref
../MP2RAGE/t1map_bet.nii.gz -out ../MP2RAGE/lesion_mask_2\_t1map.nii.gz
-init FLAIR_to_t1map.mat -applyxfm -interp nearestneighbour;**

\#Extract the mean R2\* in the lesioned WM:

**../MP2RAGE/;**

**echo R1 in lesioned WM;**

**fslstats r1map.nii -k lesion_mask_2\_t1map.nii.gz -M;**

### R1 in NAWM from JHU atlas:

Concat the matrices (you should have the b0_to_T1.mat from DTI section):

convert_xfm -omat \'\'transf_A\_to_C.mat\'\' -concat
\'\'transf_B\_to_C.mat\'\' \'\'transf_A\_to_B.mat\'\'

**convert_xfm -omat b0_to_t1map.mat -concat T1_to_t1map.mat
b0_to_T1.mat**

Use the acquired matrix to transform NAWM without OR into MWF space:

**flirt -in ../DWI/NAWM_atlas.nii.gz -ref ../MP2RAGE/t1map_bet.nii.gz
-applyxfm -init b0_to_t1map.mat -out
../MP2RAGE/NAWM_atlas_in_t1map.nii.gz -interp nearestneighbour**

\#Use fsl stats:

**../MP2RAGE/**

**echo mean R1 in NAWM Atlas;**

**fslstats r1map.nii.gz -k NAWM_atlas_in_t1map.nii.gz -M;**

### R1 in NAWM from Tractseg:

Bet the magnitude image:

**../SWI/;**

**bet magnitude.nii.gz magnitude_bet.nii.gz -f 0.5;**

**mrview magnitude.nii.gz -overlay.load magnitude_bet.nii.gz&;**

**../T1/;**

**Register the magnitude image to T1:**

**flirt -in ../SWI/magnitude_bet.nii.gz -ref T1_bet_biascorr.nii.gz
-omat mag_to_t1.mat -dof 6 -cost normmi;**

Invert the transformation:

**convert_xfm -inverse mag_to_t1.mat -omat T1_to_mag.mat**

Concat the matrices (you should have the b0_to_T1.mat from DTI section):

convert_xfm -omat \'\'transf_A\_to_C.mat\'\' -concat
\'\'transf_B\_to_C.mat\'\' \'\'transf_A\_to_B.mat\'\'

**convert_xfm -omat b0_to_mag.mat -concat T1_to_mag.mat b0_to_T1.mat**

Use the acquired matrix to transform NAWM without OR into MWF space:

**flirt -in ../DWI/NAWM_TractSeg.nii.gz -ref ../MP2RAGE/t1map_bet.nii.gz
-applyxfm -init b0_to_t1map.mat -out
../MP2RAGE/NAWM_TractSeg_in_t1map.nii.gz -interp nearestneighbour**

\#Use fsl stats:

**../MP2RAGE/**

**echo mean R1 in NAWM TractSeg;**

**fslstats r1map.nii.gz -k NAWM_TractSeg_in_t1map.nii.gz -M;**
