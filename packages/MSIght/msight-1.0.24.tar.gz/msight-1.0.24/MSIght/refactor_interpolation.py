# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 17:05:38 2024

@author: lafields2
"""

import pyimzml.ImzMLParser
import tifffile
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os


def interpolate_MSI(filename,image_path,msi_image,smoothed_image,output_directory,sample_name):
    """
    Interpolates an MSI image to match the dimensions of a corresponding H&E image.

    Parameters
    ----------
    filename : str
        Path to the .imzML file containing MSI data.

    image_path : str
        Path to the corresponding H&E image file (TIFF format).

    msi_image : numpy.ndarray
        The MSI image to be resized.

    smoothed_image : numpy.ndarray
        The smoothed and binarized H&E image used for cropping.

    output_directory : str
        Directory where the resized MSI image will be saved.

    sample_name : str
        Name used for labeling the saved output file.

    Returns
    -------
    cropped_image : numpy.ndarray
        The cropped H&E image after binarization and thresholding.

    resized_msi_image : numpy.ndarray
        The resized MSI image matching the cropped H&E image's dimensions.

    Notes
    -----
    - Extracts image dimensions from the TIFF file and the .imzML file.
    - Applies a binary mask to the smoothed H&E image.
    - Determines cropping boundaries based on tissue presence.
    - Resizes the MSI image to match the cropped H&E image's dimensions using linear interpolation.
    - Saves the resized MSI image as a PNG file.
    """
    parser = pyimzml.ImzMLParser.ImzMLParser(filename)
    # Get dimensions
    x_dimension = parser.imzmldict['max count of pixels x']
    y_dimension = parser.imzmldict['max count of pixels y']
    x_resolution = None
    y_resolution = None
    tif_file = image_path
    with tifffile.TiffFile(tif_file) as tif: # Read the TIFF file and get metadata
        x_dimension = tif.pages[0].shape[1]
        y_dimension = tif.pages[0].shape[0]
    binarized_image = smoothed_image
    binarized_image[binarized_image > 0] = 1  # Ensure the image is binary (0 or 255)
    # Calculate row and column sums
    row_sum = np.sum(binarized_image, axis=1)  # Sum along rows
    col_sum = np.sum(binarized_image, axis=0)  # Sum along columns
    crop_threshold = 15
    # Determine crop boundaries
    top_crop = np.argmax(row_sum > crop_threshold)          # Top boundary
    bottom_crop = len(row_sum) - np.argmax(row_sum[::-1] > crop_threshold)  # Bottom boundary
    left_crop = np.argmax(col_sum > crop_threshold)         # Left boundary
    right_crop = len(col_sum) - np.argmax(col_sum[::-1] > crop_threshold)  # Right boundary
    cropped_image = binarized_image[top_crop:bottom_crop, left_crop:right_crop] # Crop the image
    dimensions = cropped_image.shape
    dimensions = cropped_image.shape
    x_dimension = dimensions[1]
    y_dimension = dimensions[0]
    resized_msi_image = cv2.resize(msi_image, (x_dimension, y_dimension), interpolation=cv2.INTER_LINEAR) # Resize MSI image to match dimensions of microscopy image
    plt.figure(figsize=(10, 8))
    plt.imshow(resized_msi_image, cmap='viridis')
    plt.colorbar(label='Intensity')
    title = 'Resized MSI image with linear interpolation'
    plt.title(title)
    #fig_outpath = output_directory + '\\' + sample_name + '_MSI_composite_image_all_mz.png'
    fig_outpath = os.path.join(output_directory, f"{sample_name}_MSI_composite_image_all_mz.png")
    plt.savefig(fig_outpath,bbox_inches='tight')
    return cropped_image,resized_msi_image

def interpolate_and_visualize(filename, image_path, msi_image, smoothed_image, output_directory, sample_name, original_areas_to_zoom):
    """
    Interpolates an MSI image to match the H&E image dimensions and visualizes different interpolation methods.

    Parameters
    ----------
    filename : str
        Path to the .imzML file containing MSI data.

    image_path : str
        Path to the corresponding H&E image file (TIFF format).

    msi_image : numpy.ndarray
        The MSI image to be resized.

    smoothed_image : numpy.ndarray
        The smoothed and binarized H&E image used for cropping.

    output_directory : str
        Directory where the visualization output will be saved.

    sample_name : str
        Name used for labeling the saved output file.

    original_areas_to_zoom : dict
        Dictionary containing areas to zoom in as tuples (x1, y1, x2, y2).

    Returns
    -------
    cropped_image : numpy.ndarray
        The cropped H&E image after binarization and thresholding.

    resized_msi_image : numpy.ndarray
        The resized MSI image matching the cropped H&E image's dimensions.

    Notes
    -----
    - Extracts image dimensions from the .imzML file and the TIFF file.
    - Binarizes the H&E image and determines cropping boundaries.
    - Adjusts zoom areas to match the resized MSI image.
    - Compares multiple interpolation methods: Bilinear, Bicubic, Nearest Neighbor, and Lanczos.
    - Displays and saves the visualization as a PNG file.
    """
    parser = pyimzml.ImzMLParser.ImzMLParser(filename)
    original_msi_width = parser.imzmldict['max count of pixels x']
    original_msi_height = parser.imzmldict['max count of pixels y']
    with tifffile.TiffFile(image_path) as tif: # Read the TIFF file and get metadata
        x_dimension = tif.pages[0].shape[1]
        y_dimension = tif.pages[0].shape[0]
    binarized_image = smoothed_image
    binarized_image[binarized_image > 0] = 1 
    row_sum = np.sum(binarized_image, axis=1)
    col_sum = np.sum(binarized_image, axis=0)
    crop_threshold = 15
    top_crop = np.argmax(row_sum > crop_threshold)
    bottom_crop = len(row_sum) - np.argmax(row_sum[::-1] > crop_threshold)
    left_crop = np.argmax(col_sum > crop_threshold)
    right_crop = len(col_sum) - np.argmax(col_sum[::-1] > crop_threshold)
    cropped_image = binarized_image[top_crop:bottom_crop, left_crop:right_crop]
    dimensions = cropped_image.shape
    x_dimension = dimensions[1]
    y_dimension = dimensions[0]
    # Calculate scaling factors
    scale_x = x_dimension / original_msi_width
    scale_y = y_dimension / original_msi_height
    # Adjust the original zoom areas to match the resized image
    adjusted_areas_to_zoom = {
        name: (
            int(x1 * scale_x), int(y1 * scale_y),
            int(x2 * scale_x), int(y2 * scale_y)
        )
        for name, (x1, y1, x2, y2) in original_areas_to_zoom.items()}
    interpolation_methods = {
        'Bilinear': cv2.INTER_LINEAR,
        'Bicubic': cv2.INTER_CUBIC,
        'NearestNeighbor': cv2.INTER_NEAREST,
        'Lanczos': cv2.INTER_LANCZOS4}
    fig, axes = plt.subplots(len(adjusted_areas_to_zoom), len(interpolation_methods), figsize=(20, 10))
    for col, (method_name, interpolation) in enumerate(interpolation_methods.items()):
        if method_name == 'Original':
            resized_msi_image = msi_image
        else:
            resized_msi_image = cv2.resize(msi_image, (x_dimension, y_dimension), interpolation=interpolation)
        for row, area_name in enumerate(adjusted_areas_to_zoom):
            x1, y1, x2, y2 = adjusted_areas_to_zoom[area_name]
            zoomed_image = resized_msi_image[y1:y2, x1:x2]
            ax = axes[row, col]
            img_plot = ax.imshow(zoomed_image, cmap='jet', aspect='auto')
            ax.imshow(zoomed_image, cmap='jet', aspect='auto')
            ax.set_title(f"{method_name} - {area_name}")
            ax.axis('off')
            plt.colorbar(img_plot, ax=ax, orientation='vertical')
    plt.suptitle('Interpolation Methods Comparison')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    #fig_outpath = output_directory + '\\' + sample_name + '_interpolation_comparison.png'
    fig_outpath = os.path.join(output_directory, f"{sample_name}_interpolation_comparison.png")
    plt.savefig(fig_outpath, bbox_inches='tight')
    plt.show()
    return cropped_image, resized_msi_image