# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 17:01:41 2024

@author: lafields2
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from skimage.registration import phase_cross_correlation
from skimage.transform import AffineTransform, warp
from skimage import img_as_float
from scipy.optimize import minimize
import os

def display_and_save_image(image_array, title, filename, output_directory):
    """
    Displays a binary image and saves it as a PNG file.

    Parameters
    ----------
    image_array : numpy.ndarray
        The binary image array to be displayed and saved. Assumes a 2D grayscale format.
    
    title : str
        The title to be displayed above the image when rendered.
    
    filename : str
        The name of the output file (without the file extension) used for saving the image.
    
    output_directory : str
        The path to the directory where the image will be saved.

    Returns
    -------
    None
        This function does not return any value.

    Notes
    -----
    - The image is displayed using matplotlib with the 'gray' colormap.
    - The axis is turned off for a cleaner display.
    - The output file is saved as a PNG image in the specified directory.
    - If the output directory does not exist, an error will be raised unless handled externally.
    """
    plt.figure()
    plt.imshow(image_array, cmap='gray')  # Assuming image_array is already the correct format (binary image)
    plt.title(title)
    plt.axis('off')
    #plt.savefig(f"{output_directory}/{filename}.png")
    plt.savefig(os.path.join(output_directory,f'{filename}.png'))
    plt.close()
def register_he_msi(cropped_image,resized_msi_image,msi_threshold,he_threshold,output_directory,sample_name):
    """
    Registers a cropped H&E image to a resized MSI image using affine transformation.

    Parameters
    ----------
    cropped_image : numpy.ndarray
        The cropped H&E image, expected to be grayscale or RGB.
    
    resized_msi_image : numpy.ndarray
        The resized MSI image, expected to be grayscale or RGB.

    msi_threshold : int
        Threshold value for binarizing the MSI image (0-255).
    
    he_threshold : int
        Threshold value for binarizing the H&E image (0-255).
    
    output_directory : str
        Directory where registration results will be saved.
    
    sample_name : str
        Name used to label the saved registration output files.

    Returns
    -------
    optimal_M : numpy.ndarray
        The 3x3 affine transformation matrix obtained after optimization.
    
    final_registered_image : numpy.ndarray
        The final registered binary MSI image after applying the optimal affine transformation.

    Notes
    -----
    - Converts RGB images to grayscale if needed.
    - Binarizes images using specified thresholds.
    - Uses phase cross-correlation for initial alignment.
    - Optimizes alignment using Sum of Squared Differences (SSD).
    - Saves the initial and optimized registration results as PNG files.
    - Displays intermediate binary and registered images along with SSD values.
    """
    #Make sure H&E image is grayscale
    if len(cropped_image.shape) == 3:
        fixed_gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        fixed_gray_8bit = cv2.convertScaleAbs(fixed_gray)
    else:
        fixed_gray = cropped_image
        fixed_gray_8bit = cv2.convertScaleAbs(fixed_gray)
    if len(resized_msi_image.shape) == 3:
        moving_gray = cv2.cvtColor(resized_msi_image, cv2.COLOR_BGR2GRAY)
        moving_gray_8bit = cv2.convertScaleAbs(moving_gray)
    else:
        moving_gray = resized_msi_image
        moving_gray_8bit = cv2.convertScaleAbs(moving_gray)
    # Binarize the images using a threshold
    _, fixed_binary = cv2.threshold(fixed_gray_8bit, he_threshold, 255, cv2.THRESH_BINARY)
    _, moving_binary = cv2.threshold(moving_gray_8bit, msi_threshold, 255, cv2.THRESH_BINARY)
    # Display binary images
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(fixed_binary, cmap='gray')
    plt.title('Binary Cropped Image')
    plt.subplot(1, 2, 2)
    plt.imshow(moving_binary, cmap='gray')
    plt.title('Binary MSI Image')
    plt.show()
    # Ensure images are in floating point format
    fixed_binary_float = img_as_float(fixed_binary)
    moving_binary_float = img_as_float(moving_binary)  
    def calculate_ssd(image1, image2): # Calculate SSD
        return np.sum((image1 - image2) ** 2)
    shift, error, diffphase = phase_cross_correlation(fixed_binary_float, moving_binary_float) # Perform phase cross-correlation for initial alignment
    initial_transform = AffineTransform(translation=shift)
    registered_image_initial = warp(moving_binary_float, initial_transform.inverse)
    def objective_function(params): # Optimize affine transformation
        # Create a 3x3 transformation matrix from params
        M = np.array([[params[0], params[1], params[2]],
                      [params[3], params[4], params[5]],
                      [0, 0, 1]], dtype=np.float32)
        transformed_image = warp(moving_binary_float, AffineTransform(matrix=M).inverse)
        return calculate_ssd(fixed_binary_float, transformed_image)
    initial_params = [1, 0, shift[1], 0, 1, shift[0]] # Initial affine matrix (identity + translation)
    result = minimize(objective_function, initial_params, method='Powell') # Perform optimization
    optimal_params = result.x # Extract optimal matrix
    optimal_M = np.array([[optimal_params[0], optimal_params[1], optimal_params[2]],
                          [optimal_params[3], optimal_params[4], optimal_params[5]],
                          [0, 0, 1]], dtype=np.float32)
    final_registered_image = warp(moving_binary_float, AffineTransform(matrix=optimal_M).inverse) # Apply the final affine transformation
    ssd_initial = calculate_ssd(fixed_binary_float, registered_image_initial) # Calculate SSD values
    ssd_final = calculate_ssd(fixed_binary_float, final_registered_image)
    plt.figure(figsize=(15, 10))
    plt.subplot(2, 3, 1)
    plt.imshow(fixed_binary, cmap='gray')
    plt.title('Fixed Binary Image')
    plt.axis('off')
    plt.subplot(2, 3, 2)
    plt.imshow(moving_binary, cmap='gray')
    plt.title('Moving Binary Image')
    plt.axis('off')
    plt.subplot(2, 3, 3)
    plt.imshow(registered_image_initial, cmap='gray')
    plt.title('Registered Image (Initial Phase Correlation)')
    plt.axis('off')
    plt.subplot(2, 3, 4)
    plt.imshow(final_registered_image, cmap='gray')
    plt.title('Final Registered Image (Optimized)')
    plt.axis('off')
    # Print SSD values
    print(f"SSD without optimization (original overlap): {calculate_ssd(fixed_binary_float, moving_binary_float)}")
    print(f"SSD after phase cross-correlation: {ssd_initial}")
    print(f"SSD after optimization: {ssd_final}")
    plt.show()
    display_and_save_image(registered_image_initial, 'Registered Image Initial', f'{sample_name}_initial_registration', output_directory)
    display_and_save_image(final_registered_image, 'Final Registered Image Optimized', f'{sample_name}_optimized_registration', output_directory)
    return optimal_M,final_registered_image