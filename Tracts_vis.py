#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 12:36:20 2023

@author: paweljakuszyk
"""
import os
import nibabel as nib
import numpy as np
from dipy.io.streamline import load_tractogram, save_tractogram
from dipy.viz import window, actor
from dipy.io.stateful_tractogram import StatefulTractogram
from PIL import Image
from dipy.tracking.streamline import transform_streamlines
import colorsys
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from PIL import Image, ImageDraw, ImageFont

path_to_master_dir='/Volumes/ms/seropositive_project/participants/001_MS_F_TP1/Brain/DWI/'

path_to_tck='/Volumes/ms/seropositive_project/participants/001_MS_F_TP1/Brain/DWI/tck_for_vis/TOM_trackings/'

path_to_nii='/Volumes/ms/seropositive_project/participants/001_MS_F_TP1/Brain/DWI/tractseg_output/TOM/'

path_to_write='/Volumes/ms/seropositive_project/tract_figures/group_comparisons/'



# Create the folder if it doesn't exist
if not os.path.exists(path_to_write):
    os.makedirs(path_to_write)

    
# Load binary brain mask
mask = nib.load(path_to_master_dir + 'dwi_mask_upsampled.nii.gz')

mask_data = mask.get_fdata()

affine_mask = mask.affine
####Make figures
# Get a list of all .tck files in the folder
tck_files = [f for f in os.listdir(path_to_tck) if f.endswith('.tck')]

#To acess color:
#color = colors_dict['CC_6.tck']
#Define sifnificant tracts to visualize
MS_NMOSD_NAWM_significant_tracts = ['CC_6', 'CST_left', 'ICP_left', 'ILF_left', 'MCP', 'POPT_left']

MS_HC_NAWM_significant_tracts = ["AF_left", "AF_right", "CC_1", "CC_2", "CC_3", "CC_4", "CC_5", "CC_6", "CC_7",
   "CG_left", "CG_right", "CST_left", "CST_right", "FPT_left", "FPT_right", "ICP_left",
    "IFO_left", "IFO_right", "ILF_left", "ILF_right", "MCP", "OR_left", "POPT_left",
    "POPT_right", "SLF_III_left", "SLF_III_right", "SLF_II_left", "SLF_II_right", "SLF_I_left",
    "SLF_I_right", "ST_PREM_left", "ST_PREM_right", "T_PAR_left", "UF_left", "UF_right"]

MS_HC_LD_significant_tracts = ["AF_left", "AF_right", "ATR_left", "ATR_right", "CC_2", "CC_3", "CC_4", "CC_5", "CC_6",
    "CC_7", "CG_left", "CG_right", "CST_left", "CST_right", "FPT_left", "FPT_right", "IFO_left",
    "IFO_right", "ILF_left", "ILF_right", "MCP","OR_right", "POPT_left", "POPT_right", "SLF_III_left",
    "SLF_III_right", "SLF_II_left", "SLF_II_right", "SLF_I_left", "SLF_I_right", "STR_left",
    "STR_right", "ST_FO_left", "ST_PREM_left", "ST_PREM_right", "T_OCC_right", "T_PAR_left",
    "T_PAR_right", "T_PREM_left", "T_PREM_right", "UF_left"]

NMOSD_HC_LD_significant_tracts = ["CST_left", "CST_right", "IFO_right", "ILF_left", "ILF_right", "STR_left", "STR_right",
    "T_OCC_left", "T_PAR_left"]

NMOSD_MS_LD_significant_tracts = ['CC_6']



all_significant_tracts = list(set(MS_NMOSD_NAWM_significant_tracts + MS_HC_NAWM_significant_tracts + MS_HC_LD_significant_tracts + NMOSD_HC_LD_significant_tracts + NMOSD_MS_LD_significant_tracts))

NAWM_sig_tracts = list(set(MS_NMOSD_NAWM_significant_tracts + MS_HC_NAWM_significant_tracts))
LD_sig_tracts = list(set(MS_HC_LD_significant_tracts + NMOSD_HC_LD_significant_tracts + NMOSD_MS_LD_significant_tracts))

#generate colors for tracts
def generate_contrasting_colors(num_colors):
    colors = []
    for i in range(num_colors):
        hue = (i * 360 / num_colors) % 360
        saturation = 100  # Adjust as desired
        luminance = 50 + (i % 2) * 20  # Adjust as desired for varying luminance
        rgb = colorsys.hls_to_rgb(hue / 360, luminance / 100, saturation / 100)
        colors.append(rgb)
    return colors

num_colors = 46
colors_list = generate_contrasting_colors(num_colors)
colors_dict = dict(zip(all_significant_tracts, colors_list))


###Load tracts
# Iterate through each .tck file
MS_NMOSD_NAWM_tracts = {}  # Dictionary to store the loaded tracts
for tck_file in MS_NMOSD_NAWM_significant_tracts:
    tract = path_to_tck + tck_file + '.tck'
    # Load the tract
    tractogram = load_tractogram(tract, mask)  
    #Get tract name without .tck
    tck_name = os.path.splitext(tck_file)[0]
    # Store the tract in the dictionary
    MS_NMOSD_NAWM_tracts[tck_name] = tractogram
    
# Load tracts for MS_HC_NAWM_significant_tracts
MS_HC_NAWM_tracts = {}
for tck_file in MS_HC_NAWM_significant_tracts:
    tract = path_to_tck + tck_file + '.tck'
    tractogram = load_tractogram(tract, mask)
    tck_name = os.path.splitext(tck_file)[0]
    MS_HC_NAWM_tracts[tck_name] = tractogram

# Load tracts for MS_HC_LD_significant_tracts
MS_HC_LD_tracts = {}
for tck_file in MS_HC_LD_significant_tracts:
    tract = path_to_tck + tck_file + '.tck'
    tractogram = load_tractogram(tract, mask)
    tck_name = os.path.splitext(tck_file)[0]
    MS_HC_LD_tracts[tck_name] = tractogram

# Load tracts for NMOSD_HC_LD_significant_tracts
NMOSD_HC_LD_tracts = {}
for tck_file in NMOSD_HC_LD_significant_tracts:
    tract = path_to_tck + tck_file + '.tck'
    tractogram = load_tractogram(tract, mask)
    tck_name = os.path.splitext(tck_file)[0]
    NMOSD_HC_LD_tracts[tck_name] = tractogram

# Load tracts for NMOSD_MS_LD_significant_tracts
NMOSD_MS_LD_tracts = {}
for tck_file in NMOSD_MS_LD_significant_tracts:
    tract = path_to_tck + tck_file + '.tck'
    tractogram = load_tractogram(tract, mask)
    tck_name = os.path.splitext(tck_file)[0]
    NMOSD_MS_LD_tracts[tck_name] = tractogram


#Create vizualization
stream_width = 6


####MS_NMOSD_NAWM
scene = window.Scene()
# Create an isosurface of the binary mask image to form the "glass brain"
vol_actor = actor.contour_from_roi(mask_data, affine=affine_mask, opacity=0.1, color=(244, 244, 244))
# Add the isosurface to the visualization window
scene.add(vol_actor)

# Stream actors using the tracts from the list
stream_actors = []
for tract in MS_NMOSD_NAWM_significant_tracts:
    streamlines = MS_NMOSD_NAWM_tracts[tract].streamlines
    color = colors_dict[tract]
    stream_actor = actor.line(streamlines, color, linewidth=stream_width, depth_cue=True, fake_tube=False)
    scene.add(stream_actor)
    stream_actors.append(stream_actor)

# Uncomment the line below to show to display the window
#window.show(scene, size=(800, 800), reset_camera=False)
scene.set_camera(position=(-5.94, 301.48, 49.25), focal_point=(-2.63, 20.69, -7.20), view_up=(-0.04, -0.20, 0.98))
window.record(scene, out_path=path_to_write+'MS_NMOSD_NAWM_front.png', size=(800, 800), magnification=2)

scene.set_camera(position=(341.83, 58.75, -10.27), focal_point=(-2.63, 20.69, -7.20), view_up=(0.00, 0.06, 1.00))
window.record(scene, out_path=path_to_write+'MS_NMOSD_NAWM_RH.png', size=(800, 800), magnification=2)

scene.set_camera(position=(-340.76, -38.83, -54.52), focal_point=(-2.63, 20.69, -7.20), view_up=(-0.13, -0.06, 0.99))
window.record(scene, out_path=path_to_write+'MS_NMOSD_NAWM_LH.png', size=(800, 800), magnification=2)

#scene.camera_info()

####MS_NMOSD_NAWM
scene = window.Scene()
# Create an isosurface of the binary mask image to form the "glass brain"
vol_actor = actor.contour_from_roi(mask_data, affine=affine_mask, opacity=0.1, color=(244, 244, 244))
# Add the isosurface to the visualization window
scene.add(vol_actor)


# Uncomment the line below to show to display the window
#window.show(scene, size=(800, 800), reset_camera=False)
scene.set_camera(position=(-5.94, 301.48, 49.25), focal_point=(-2.63, 20.69, -7.20), view_up=(-0.04, -0.20, 0.98))
window.record(scene, out_path=path_to_write+'HC_NMOSD_NAWM_front.png', size=(800, 800), magnification=2)

scene.set_camera(position=(341.83, 58.75, -10.27), focal_point=(-2.63, 20.69, -7.20), view_up=(0.00, 0.06, 1.00))
window.record(scene, out_path=path_to_write+'HC_NMOSD_NAWM_RH.png', size=(800, 800), magnification=2)

scene.set_camera(position=(-340.76, -38.83, -54.52), focal_point=(-2.63, 20.69, -7.20), view_up=(-0.13, -0.06, 0.99))
window.record(scene, out_path=path_to_write+'HC_NMOSD_NAWM_LH.png', size=(800, 800), magnification=2)

#scene.camera_info()

######HC_MS_NAWM
scene = window.Scene()
# Create an isosurface of the binary mask image to form the "glass brain"
vol_actor = actor.contour_from_roi(mask_data, affine=affine_mask, opacity=0.1, color=(244, 244, 244))
# Add the isosurface to the visualization window
scene.add(vol_actor)

# Stream actors using the tracts from the list
stream_actors = []
for tract in MS_HC_NAWM_significant_tracts:
    streamlines = MS_HC_NAWM_tracts[tract].streamlines
    color = colors_dict[tract]
    stream_actor = actor.line(streamlines, color, linewidth=stream_width, depth_cue=True, fake_tube=False)
    scene.add(stream_actor)
    stream_actors.append(stream_actor)

# Uncomment the line below to show the window
# window.show(scene, size=(800, 800), reset_camera=False)

scene.set_camera(position=(-5.94, 301.48, 49.25), focal_point=(-2.63, 20.69, -7.20), view_up=(-0.04, -0.20, 0.98))
window.record(scene, out_path=path_to_write + 'HC_MS_NAWM_front.png', size=(800, 800), magnification=2)

scene.set_camera(position=(341.83, 58.75, -10.27), focal_point=(-2.63, 20.69, -7.20), view_up=(0.00, 0.06, 1.00))
window.record(scene, out_path=path_to_write + 'HC_MS_NAWM_RH.png', size=(800, 800), magnification=2)

scene.set_camera(position=(-340.76, -38.83, -54.52), focal_point=(-2.63, 20.69, -7.20), view_up=(-0.13, -0.06, 0.99))
window.record(scene, out_path=path_to_write + 'HC_MS_NAWM_LH.png', size=(800, 800), magnification=2)


####LD######

######MS_HC_LD_tracts
scene = window.Scene()
# Create an isosurface of the binary mask image to form the "glass brain"
vol_actor = actor.contour_from_roi(mask_data, affine=affine_mask, opacity=0.1, color=(244, 244, 244))
# Add the isosurface to the visualization window
scene.add(vol_actor)

# Stream actors using the tracts from the list
stream_actors = []
for tract in MS_HC_LD_significant_tracts:
    streamlines = MS_HC_LD_tracts[tract].streamlines
    color = colors_dict[tract]
    stream_actor = actor.line(streamlines, color, linewidth=stream_width, depth_cue=True, fake_tube=False)
    scene.add(stream_actor)
    stream_actors.append(stream_actor)

# Uncomment the line below to show the window
# window.show(scene, size=(800, 800), reset_camera=False)

scene.set_camera(position=(-5.94, 301.48, 49.25), focal_point=(-2.63, 20.69, -7.20), view_up=(-0.04, -0.20, 0.98))
window.record(scene, out_path=path_to_write + 'MS_HC_LD_front.png', size=(500, 500), magnification=2)

scene.set_camera(position=(341.83, 58.75, -10.27), focal_point=(-2.63, 20.69, -7.20), view_up=(0.00, 0.06, 1.00))
window.record(scene, out_path=path_to_write + 'MS_HC_LD_RH.png', size=(500, 500), magnification=2)

scene.set_camera(position=(-340.76, -38.83, -54.52), focal_point=(-2.63, 20.69, -7.20), view_up=(-0.13, -0.06, 0.99))
window.record(scene, out_path=path_to_write + 'MS_HC_LD_LH.png', size=(500, 500), magnification=2)


######NMOSD_HC_LD_tracts
scene = window.Scene()
# Create an isosurface of the binary mask image to form the "glass brain"
vol_actor = actor.contour_from_roi(mask_data, affine=affine_mask, opacity=0.1, color=(244, 244, 244))
# Add the isosurface to the visualization window
scene.add(vol_actor)

# Stream actors using the tracts from the list
stream_actors = []
for tract in NMOSD_HC_LD_significant_tracts:
    streamlines = NMOSD_HC_LD_tracts[tract].streamlines
    color = colors_dict[tract]
    stream_actor = actor.line(streamlines, color, linewidth=stream_width, depth_cue=True, fake_tube=False)
    scene.add(stream_actor)
    stream_actors.append(stream_actor)

# Uncomment the line below to show the window
# window.show(scene, size=(800, 800), reset_camera=False)

scene.set_camera(position=(-5.94, 301.48, 49.25), focal_point=(-2.63, 20.69, -7.20), view_up=(-0.04, -0.20, 0.98))
window.record(scene, out_path=path_to_write + 'NMOSD_HC_LD_front.png', size=(500, 500), magnification=2)

scene.set_camera(position=(341.83, 58.75, -10.27), focal_point=(-2.63, 20.69, -7.20), view_up=(0.00, 0.06, 1.00))
window.record(scene, out_path=path_to_write + 'NMOSD_HC_LD_RH.png', size=(500, 500), magnification=2)

scene.set_camera(position=(-340.76, -38.83, -54.52), focal_point=(-2.63, 20.69, -7.20), view_up=(-0.13, -0.06, 0.99))
window.record(scene, out_path=path_to_write + 'NMOSD_HC_LD_LH.png', size=(500, 500), magnification=2)

######NMOSD_MS_LD_tracts
scene = window.Scene()
# Create an isosurface of the binary mask image to form the "glass brain"
vol_actor = actor.contour_from_roi(mask_data, affine=affine_mask, opacity=0.1, color=(244, 244, 244))
# Add the isosurface to the visualization window
scene.add(vol_actor)

# Stream actors using the tracts from the list
stream_actors = []
for tract in NMOSD_MS_LD_significant_tracts:
    streamlines = NMOSD_MS_LD_tracts[tract].streamlines
    color = colors_dict[tract]
    stream_actor = actor.line(streamlines, color, linewidth=stream_width, depth_cue=True, fake_tube=False)
    scene.add(stream_actor)
    stream_actors.append(stream_actor)

# Uncomment the line below to show the window
# window.show(scene, size=(800, 800), reset_camera=False)

scene.set_camera(position=(-5.94, 301.48, 49.25), focal_point=(-2.63, 20.69, -7.20), view_up=(-0.04, -0.20, 0.98))
window.record(scene, out_path=path_to_write + 'NMOSD_MS_LD_front.png', size=(500, 500), magnification=2)

scene.set_camera(position=(341.83, 58.75, -10.27), focal_point=(-2.63, 20.69, -7.20), view_up=(0.00, 0.06, 1.00))
window.record(scene, out_path=path_to_write + 'NMOSD_MS_LD_RH.png', size=(500, 500), magnification=2)

scene.set_camera(position=(-340.76, -38.83, -54.52), focal_point=(-2.63, 20.69, -7.20), view_up=(-0.13, -0.06, 0.99))
window.record(scene, out_path=path_to_write + 'NMOSD_MS_LD_LH.png', size=(500, 500), magnification=2)



##Combine image triplets into one .PNG per tract
# Path to the directory containing the image files
img_dir = path_to_write

# Loop through each file in the directory
for filename in os.listdir(img_dir):
    if filename.endswith('.png'):
        # Split the filename into base name and suffix
        basename, suffix = filename.rsplit('_', 1)
        #print(basename)
        # Check if the suffix is axial, sagittal, or coronal
        if suffix in ('front.png', 'RH.png', 'LH.png'):
            #print(basename)
            # Get the corresponding filenames for the other two views
            axial_filename = os.path.join(img_dir, basename+'_LH.png')
            sagittal_filename = os.path.join(img_dir, basename+'_front.png')
            coronal_filename = os.path.join(img_dir, basename+'_RH.png')
            # Check if the other two views exist
            if (os.path.exists(axial_filename) and
                os.path.exists(sagittal_filename) and
                os.path.exists(coronal_filename)):
                # Open the images
                axial_img = Image.open(axial_filename)
                sagittal_img = Image.open(sagittal_filename)
                coronal_img = Image.open(coronal_filename)
                # Combine the images horizontally
                combined_img = Image.new('RGB', (axial_img.width + sagittal_img.width + coronal_img.width, axial_img.height))
                combined_img.paste(axial_img, (0, 0))
                combined_img.paste(sagittal_img, (axial_img.width, 0))
                combined_img.paste(coronal_img, (axial_img.width + sagittal_img.width, 0))
                # Save the combined image
                combined_filename = os.path.join(img_dir, basename+'_combined.png')
                combined_img.save(combined_filename)

##Make color legend

##Take apart NAWM and LD compared tracts for two separate legends
NAWM_sig_tracts = list(set(MS_NMOSD_NAWM_significant_tracts + MS_HC_NAWM_significant_tracts))
LD_sig_tracts = list(set(MS_HC_LD_significant_tracts + NMOSD_HC_LD_significant_tracts + NMOSD_MS_LD_significant_tracts))

NAWM_dict = {key: value for key, value in colors_dict.items() if key in NAWM_sig_tracts}
LD_dict = {key: value for key, value in colors_dict.items() if key in LD_sig_tracts}
# Sort the dictionary by tract names in alphabetical order
NAWM_sorted_tracts_colors = {k: v for k, v in sorted(NAWM_dict.items(), key=lambda item: item[0])}
LD_sorted_tracts_colors = {k: v for k, v in sorted(LD_dict.items(), key=lambda item: item[0])}

##NAWM legend
# Create a list of tract names and colors
tract_names = list(NAWM_sorted_tracts_colors.keys())
tract_colors = [color[:3] for color in NAWM_sorted_tracts_colors.values()]

# Create a figure and axis for the legend
fig, ax = plt.subplots(facecolor='black', figsize=(2,16))

# Set text color to white
plt.rcParams['text.color'] = 'white'

# Plot a color bar with the tract names and colors
patches = [Patch(color=[r, g, b, 1.0], label=name) for name, (r, g, b) in zip(tract_names, tract_colors)]
ax.legend(handles=patches, loc="center", title="White matter tract", frameon=False)

# Adjust spacing and margins
plt.subplots_adjust(top=0.919, bottom=0.081, left=0.079, right=0.921, hspace=0.2, wspace=0.2)

# Remove the axis labels and ticks
ax.set_axis_off()

# Display the legend
plt.savefig(path_to_write+'NAWM_legend.png', dpi=300)



##LD legend
# Create a list of tract names and colors
tract_names = list(LD_sorted_tracts_colors.keys())
tract_colors = [color[:3] for color in LD_sorted_tracts_colors.values()]

# Create a figure and axis for the legend
fig, ax = plt.subplots(facecolor='black', figsize=(2,16))

# Set text color to white
plt.rcParams['text.color'] = 'white'

# Plot a color bar with the tract names and colors
patches = [Patch(color=[r, g, b, 1.0], label=name) for name, (r, g, b) in zip(tract_names, tract_colors)]
ax.legend(handles=patches, loc="center", title="White matter tract", frameon=False)

# Adjust spacing and margins
plt.subplots_adjust(top=0.919, bottom=0.081, left=0.079, right=0.921, hspace=0.2, wspace=0.2)

# Remove the axis labels and ticks
ax.set_axis_off()

# Display the legend
plt.savefig(path_to_write+'LD_legend.png', dpi=300)




###Final NAWM plot
# Load the two images to be stacked
image1 = Image.open(path_to_write+'HC_MS_NAWM_combined.png')
image2 = Image.open(path_to_write+'HC_NMOSD_NAWM_combined.png')
image3 = Image.open(path_to_write+'MS_NMOSD_NAWM_combined.png')

# Create a new image with the desired dimensions
width = max(image1.width, image2.width, image3.width)
height = image1.height + image2.height + image3.height
stacked_image = Image.new('RGB', (width, height))

# Paste the images onto the stacked image
stacked_image.paste(image1, (0, 0))
stacked_image.paste(image2, (0, image1.height))
stacked_image.paste(image3, (0, image1.height + image2.height))

# Load the legend image
legend_image = Image.open(path_to_write+'NAWM_legend.png')

# Resize image3 to 200x1000 pixels
legend_image = legend_image.resize((1000, 4800))

# Calculate the new dimensions for the final figure
final_width = width + legend_image.width
final_height = max(height, legend_image.height)

# Create a new image with the desired dimensions
final_image = Image.new('RGB', (final_width, final_height), (255, 255, 255))

# Paste the stacked image and legend image onto the final image
final_image.paste(stacked_image, (0, 0))
final_image.paste(legend_image, (width, (final_height - legend_image.height) // 2))

# Add titles to the individual images
# Assuming you have text for titles: title1, title2, title3

font = ImageFont.truetype("Arial", 100) # Specify your desired font and size

draw = ImageDraw.Draw(final_image)
draw.text((image1.width/2, 20), "HC-MS", font=font, fill=(255, 255, 255))  # Position and text for title1
draw.text((40, 20), "A", font=font, fill=(255, 255, 255))
draw.text((image1.width/2, image1.height + 20), "NMOSD-HC", font=font, fill=(255, 255, 255))  # Position and text for title2
draw.text((40, image1.height + 20), "B", font=font, fill=(255, 255, 255))
draw.text((image1.width/2, image1.height*2 + 20), "NMOSD-MS", font=font, fill=(255, 255, 255))  # Position and text for title3
draw.text((40, image1.height*2  + 20), "C", font=font, fill=(255, 255, 255))

# Save the final image
final_image = final_image.resize((3600, 3000))

final_image.save(path_to_write+'NAWM_tracts_plot_fixed.png', dpi=(300, 300))



###Final LD plot
# Load the two images to be stacked
image1 = Image.open(path_to_write+'MS_HC_LD_combined.png')
image2 = Image.open(path_to_write+'NMOSD_HC_LD_combined.png')
image3 = Image.open(path_to_write+'NMOSD_MS_LD_combined.png')

# Create a new image with the desired dimensions
width = max(image1.width, image2.width, image3.width)
height = image1.height + image2.height + image3.height
stacked_image = Image.new('RGB', (width, height))

# Paste the images onto the stacked image
stacked_image.paste(image1, (0, 0))
stacked_image.paste(image2, (0, image1.height))
stacked_image.paste(image3, (0, image1.height + image2.height))

# Load the legend image
legend_image = Image.open(path_to_write+'LD_legend.png')

# Resize image3 to 200x1000 pixels
legend_image = legend_image.resize((600, 3000))

# Calculate the new dimensions for the final figure
final_width = width + legend_image.width
final_height = max(height, legend_image.height)

# Create a new image with the desired dimensions
final_image = Image.new('RGB', (final_width, final_height), (255, 255, 255))

# Paste the stacked image and legend image onto the final image
final_image.paste(stacked_image, (0, 0))
final_image.paste(legend_image, (width, (final_height - legend_image.height) // 2))

# Add titles to the individual images
# Assuming you have text for titles: title1, title2, title3

font = ImageFont.truetype("Arial", 65) # Specify your desired font and size

draw = ImageDraw.Draw(final_image)
draw.text((image1.width/2, 20), "HC-MS", font=font, fill=(255, 255, 255))  # Position and text for title1
draw.text((40, 20), "A", font=font, fill=(255, 255, 255))
draw.text((image1.width/2, image1.height + 20), "NMOSD-HC", font=font, fill=(255, 255, 255))  # Position and text for title2
draw.text((40, image1.height + 20), "B", font=font, fill=(255, 255, 255))
draw.text((image1.width/2, image1.height*2 + 20), "NMOSD-MS", font=font, fill=(255, 255, 255))  # Position and text for title3
draw.text((40, image1.height*2  + 20), "C", font=font, fill=(255, 255, 255))

# Save the final image
final_image.save(path_to_write+'LD_tracts_plot_fixed.png', dpi=(300, 300))



