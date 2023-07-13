V=spm_vol('C_mask.nii');
img=spm_read_vols(V);

[x,y,z]=ind2sub(size(img),find(img>0));

[idx,C]=kmeans([x,y,z],3);

img(:)=0;
Csub=round(C);
Cind=sub2ind(size(img),Csub(:,1),Csub(:,2),Csub(:,3))
img(Cind)=1;

%scatter3(x, y, z, 15, idx, 'filled');

V.fname='C_mask_split.nii'
spm_write_vol(V,img)