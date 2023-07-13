function set_position_vox(vox,V)
M   = V.mat;
vox_mm = M(1:3,:)*[vox';1];
spm_orthviews('Reposition',vox_mm');
end