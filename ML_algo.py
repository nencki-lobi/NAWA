#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 13:16:01 2023

@author: pawel
"""

import os
import nibabel as nib

#########LOADING DATA#########
val_dir = "/Volumes/ms/ML/LD_data/Validation"
train_dir = "/Volumes/ms/ML/LD_data/Train"

train_flair_dir = os.path.join(train_dir, 'FLAIR')
train_mask_dir = os.path.join(train_dir, 'lesion_masks')

val_flair_dir = os.path.join(val_dir, 'FLAIR')
val_mask_dir = os.path.join(val_dir, 'lesion_masks')

train_flair_images = []
train_masks = []

val_flair_images = []
val_masks = []


# Load FLAIR images
#Train
for filename in os.listdir(train_flair_dir):
    if filename.endswith('.nii.gz'):
        train_flair_path = os.path.join(train_flair_dir, filename)
        try:
            flair_img = nib.load(train_flair_path)
            flair_data = flair_img.get_fdata()
            train_flair_images.append(flair_data)
        except nib.filebasedimages.ImageFileError:
            print(f"Error loading file: {train_flair_path}")
            continue
        
#Validation
list_val = []
for filename in os.listdir(val_flair_dir):
    if filename.endswith('.nii.gz'):
        val_flair_path = os.path.join(val_flair_dir, filename)
        list_val.append(val_flair_path)
        try:
            flair_img = nib.load(val_flair_path)
            flair_data = flair_img.get_fdata()
            val_flair_images.append(flair_data)
        except nib.filebasedimages.ImageFileError:
            print(f"Error loading file: {val_flair_path}")
            continue
        
# Load masks
#Train
train_mask_list = []
for filename in os.listdir(train_mask_dir):
    if filename.endswith('.nii.gz'):
        train_mask_path = os.path.join(train_mask_dir, filename)
        train_mask_list.append(train_mask_path)
        try:
            mask_img = nib.load(train_mask_path)
            mask_data = mask_img.get_fdata()
            train_masks.append(mask_data)
        except nib.filebasedimages.ImageFileError:
            print(f"Error loading file: {train_mask_path}")
            continue

#Validation
val_mask_list = []
for filename in os.listdir(val_mask_dir):
    if filename.endswith('.nii.gz'):
        val_mask_path = os.path.join(val_mask_dir, filename)
        val_mask_list.append(val_mask_path)
        try:
            mask_img = nib.load(val_mask_path)
            mask_data = mask_img.get_fdata()
            val_masks.append(mask_data)
        except nib.filebasedimages.ImageFileError:
            print(f"Error loading file: {val_mask_path}")
            continue

####NORMALIZATION#######
import numpy as np

#Train
train_normalized_FLAIR = []

# Iterate over the FLAIR images
for image in train_flair_images:
    # Compute the minimum and maximum intensity values
    image_min = np.min(image)
    image_max = np.max(image)
    
    # Apply min-max scaling
    normalized_image = (image - image_min) / (image_max - image_min)
    
    train_normalized_FLAIR.append(normalized_image)

val_normalized_FLAIR = []

#Validation
# Iterate over the FLAIR images
for image in val_flair_images:
    # Compute the minimum and maximum intensity values
    image_min = np.min(image)
    image_max = np.max(image)
    
    # Apply min-max scaling
    normalized_image = (image - image_min) / (image_max - image_min)
    
    val_normalized_FLAIR.append(normalized_image)

######Convolutional Neural Network#######
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv3D, MaxPooling3D, UpSampling3D, Dropout, BatchNormalization, Flatten, Dense


# Reshape the training and validation sets
train_normalized_FLAIR = np.expand_dims(train_normalized_FLAIR, axis=-1)
train_masks = np.expand_dims(train_masks, axis=-1)
val_normalized_FLAIR = np.expand_dims(val_normalized_FLAIR, axis=-1)
val_masks = np.expand_dims(val_masks, axis=-1)


# Get the new input shape
val_input_shape = val_normalized_FLAIR.shape[1:]
val_input_shape_masks = val_masks.shape[1:]
train_input_shape = train_normalized_FLAIR.shape[1:]
train_input_shape_masks = train_masks.shape[1:]

input_shape = train_masks.shape[1:]
'''
#Ensure the masks are binary
# Check uniqueness of values in training masks
for i, mask in enumerate(train_masks):
    unique_values = np.unique(mask)
    if len(unique_values) != 2:
        print("Non-binary mask found in training set at index", i)
        print("Filename:", train_mask_list[i])

# Check uniqueness of values in validation masks
for i, mask in enumerate(val_masks):
    unique_values = np.unique(mask)
    if len(unique_values) != 2:
        print("Non-binary mask found in validation set at index", i)
        print("Filename:", val_mask_list[i])

## The are some masks that deviate from binary

# Check for values smaller than 1 and greater than 0 in masks
for i, mask in enumerate(train_masks):
    unique_values = np.unique(mask)
    non_binary_values = unique_values[(unique_values < 1) | (unique_values > 0)]
    if len(non_binary_values) > 0:
        print(f"Non-binary values found in train mask {i + 1}:")
        print(non_binary_values)

for i, mask in enumerate(val_masks):
    unique_values = np.unique(mask)
    non_binary_values = unique_values[(unique_values < 1) | (unique_values > 0)]
    if len(non_binary_values) > 0:
        print(f"Non-binary values found in val mask {i + 1}:")
        print(non_binary_values)

'''

model = Sequential()
model.add(Conv3D(32, kernel_size=(3, 3, 3), activation='relu', padding='same', input_shape=input_shape))
model.add(Conv3D(64, kernel_size=(3, 3, 3), activation='relu', padding='same'))
model.add(Conv3D(128, kernel_size=(3, 3, 3), activation='relu', padding='same'))
model.add(Conv3D(1, kernel_size=(1, 1, 1), activation='sigmoid', padding='valid'))


# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
num_epochs = 10
batch_size = 11
model.fit(train_normalized_FLAIR, train_masks, validation_data=(val_normalized_FLAIR, val_masks), epochs=num_epochs, batch_size=batch_size)



