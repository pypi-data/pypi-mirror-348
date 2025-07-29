# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 17:08:52 2024

@author: lafields2
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

def load_he_image(image_path): # Load the H&E image
    image = cv2.imread(image_path)
    return image

def foreground_mask_make(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # Convert the image to HSV color space
    lower_bound = np.array([0, 0, 0])  # Adjust as needed
    upper_bound = np.array([180, 50, 255])  # Adjust as needed
    background_mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
    foreground_mask = cv2.bitwise_not(background_mask) # Invert the mask to get the foreground (i.e., the tissue)
    return foreground_mask

def foreground_extract(image,foreground_mask):
    foreground_image = cv2.bitwise_and(image, image, mask=foreground_mask) #Apply the foreground mask to the original image to remove the background
    return foreground_image

def red_channel_extract(foreground_image):
    red_channel = foreground_image[:, :, 2] # Extract the red channel from the foreground image
    return red_channel

def bin_he_image(threshold_value,red_channel):
    _, thresholded_image = cv2.threshold(red_channel, threshold_value, 255, cv2.THRESH_BINARY)
    return thresholded_image

def smooth_he_image(thresholded_image):
    smoothed_image = cv2.GaussianBlur(thresholded_image, (5, 5), 0)
    return smoothed_image

def preprocess_he(image_path,threshold_value,sample_name,output_directory):
    he_image = load_he_image(image_path)
    foreground_mask_he_image = foreground_mask_make(he_image)
    foreground_he_image = foreground_extract(he_image,foreground_mask_he_image)
    red_channel_he_image = red_channel_extract(foreground_he_image)
    thresholded_he_image = bin_he_image(threshold_value,red_channel_he_image)
    final_he_image = smooth_he_image(thresholded_he_image)
    plt.figure(figsize=(12, 10))
    plt.subplot(2, 3, 1)
    plt.title('Original Image')
    plt.imshow(cv2.cvtColor(he_image, cv2.COLOR_BGR2RGB))
    plt.subplot(2, 3, 2)
    plt.title('Foreground Mask')
    plt.imshow(foreground_mask_he_image, cmap='gray')
    plt.subplot(2, 3, 3)
    plt.title('Foreground Image')
    plt.imshow(cv2.cvtColor(foreground_he_image, cv2.COLOR_BGR2RGB))
    plt.subplot(2, 3, 4)
    plt.title('Red Channel')
    plt.imshow(red_channel_he_image, cmap='gray')
    plt.subplot(2, 3, 5)
    plt.title('Thresholded Image')
    plt.imshow(thresholded_he_image, cmap='gray')
    plt.subplot(2, 3, 6)
    plt.title('Smoothed Image')
    plt.imshow(final_he_image, cmap='gray')
    plt.tight_layout()
    fig_outpath = output_directory + '\\' + sample_name + '_HE_processed_image.png'
    plt.savefig(fig_outpath,bbox_inches='tight')
    return final_he_image