clusters=dlmread('fsl_clusters.txt','\t',1,0);
%for binary mask execute
%cluster --in=test.nii --thresh=1 > fsl_clusters.txt
voxelCoords=clusters(:,7:9)

image=spm_select(1,'image','Select an image to present');
spm_check_registration(image)

V=spm_vol(image)

for i=1:size(voxelCoords,1)
set_position_vox(voxelCoords(i,:),V)
pause(5)
end