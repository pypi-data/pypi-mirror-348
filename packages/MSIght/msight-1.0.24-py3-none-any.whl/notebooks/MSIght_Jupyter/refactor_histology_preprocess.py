# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 17:08:52 2024

@author: lafields2
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def load_he_image(image_path): # Load the H&E image
    """
    Loads an H&E image from the specified file path.
    
    Parameters
    ----------
    image_path : str
        Path to the H&E image file.
    
    Returns
    -------
    image : numpy.ndarray
        The loaded image as a BGR array.
    
    Notes
    -----
    - Uses OpenCV to read the image, returning it in BGR format.
    - The image can be converted to other color formats using OpenCV functions as needed.
    """
    image = cv2.imread(image_path)
    return image

def foreground_mask_make(image):
    """
    Creates a foreground mask by isolating tissue regions from an H&E image using HSV color thresholding.

    Parameters
    ----------
    image : numpy.ndarray
        The input image in BGR format.

    Returns
    -------
    foreground_mask : numpy.ndarray
        A binary mask where the tissue regions are white (255) and the background is black (0).

    Notes
    -----
    - Converts the image to HSV color space using OpenCV.
    - Applies a color threshold to separate the background from the tissue.
    - Inverts the background mask to obtain the foreground (tissue) mask.
    - Threshold values can be adjusted for better segmentation depending on the sample.
    """
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # Convert the image to HSV color space
    lower_bound = np.array([0, 0, 0])  # Adjust as needed
    upper_bound = np.array([180, 50, 255])  # Adjust as needed
    background_mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
    foreground_mask = cv2.bitwise_not(background_mask) # Invert the mask to get the foreground (i.e., the tissue)
    return foreground_mask

def foreground_extract(image,foreground_mask):
    """
    Extracts the foreground (tissue region) from an H&E image using a binary mask.

    Parameters
    ----------
    image : numpy.ndarray
        The input image from which the background should be removed.

    foreground_mask : numpy.ndarray
        A binary mask where the tissue regions are white (255) and the background is black (0).

    Returns
    -------
    foreground_image : numpy.ndarray
        The extracted foreground image with the background removed.

    Notes
    -----
    - Uses OpenCV's `cv2.bitwise_and` to apply the foreground mask.
    - Pixels outside the foreground mask are set to black (0).
    - Ensure the mask and the input image have the same dimensions.
    """
    foreground_image = cv2.bitwise_and(image, image, mask=foreground_mask) #Apply the foreground mask to the original image to remove the background
    return foreground_image

def red_channel_extract(foreground_image):
    """
    Extracts the red channel from the foreground image.

    Parameters
    ----------
    foreground_image : numpy.ndarray
        The input image from which the red channel will be extracted. 
        Expected to be in BGR format.

    Returns
    -------
    red_channel : numpy.ndarray
        A 2D array representing the red channel of the input image.

    Notes
    -----
    - Assumes the input image is in BGR format.
    - Extracts the third channel (index 2) corresponding to the red channel.
    """
    red_channel = foreground_image[:, :, 2] # Extract the red channel from the foreground image
    return red_channel

def bin_he_image(threshold_value,red_channel):
    """
    Binarizes the red channel of an H&E image using a specified threshold.

    Parameters
    ----------
    threshold_value : int
        The threshold value (0-255) used for binarization.

    red_channel : numpy.ndarray
        The extracted red channel from the H&E image.

    Returns
    -------
    thresholded_image : numpy.ndarray
        A binary image where pixels above the threshold are set to 255 (white) and others to 0 (black).

    Notes
    -----
    - Uses OpenCV's `cv2.threshold` for binarization.
    - Ensure the input red channel is a 2D array of type `numpy.ndarray`.
    """
    _, thresholded_image = cv2.threshold(red_channel, threshold_value, 255, cv2.THRESH_BINARY)
    return thresholded_image

def smooth_he_image(thresholded_image):
    """
    Applies Gaussian smoothing to a binarized H&E image.

    Parameters
    ----------
    thresholded_image : numpy.ndarray
        The binarized H&E image to be smoothed.

    Returns
    -------
    smoothed_image : numpy.ndarray
        The smoothed binary image after applying Gaussian blur.

    Notes
    -----
    - Uses OpenCV's `cv2.GaussianBlur` with a kernel size of (5, 5).
    - The standard deviation for the Gaussian kernel is set to 0 (calculated automatically).
    - Smoothing reduces noise and sharp edges in the binarized image.
    """
    smoothed_image = cv2.GaussianBlur(thresholded_image, (5, 5), 0)
    return smoothed_image

def preprocess_he(image_path,threshold_value,sample_name,output_directory):
    """
    Preprocesses an H&E image by extracting the tissue region, binarizing, and smoothing it.

    Parameters
    ----------
    image_path : str
        Path to the input H&E image file.

    threshold_value : int
        Threshold value (0-255) for binarization of the red channel.

    sample_name : str
        Name used for labeling the saved output file.

    output_directory : str
        Directory where the processed image will be saved.

    Returns
    -------
    final_he_image : numpy.ndarray
        The preprocessed H&E image after binarization and smoothing.

    Notes
    -----
    - Applies several preprocessing steps:
        1. Loads the H&E image.
        2. Creates a foreground mask using HSV thresholding.
        3. Extracts the tissue region using the mask.
        4. Extracts the red channel from the tissue region.
        5. Binarizes the red channel using the given threshold.
        6. Applies Gaussian smoothing to reduce noise.
    - Displays each preprocessing step for visualization.
    - Saves the final processed image as a PNG file.
    """
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
    #fig_outpath = output_directory + '\\' + sample_name + '_HE_processed_image.png'
    fig_outpath = os.path.join(output_directory,f"{sample_name}_HE_processed_image.png")
    plt.savefig(fig_outpath,bbox_inches='tight')
    return final_he_image