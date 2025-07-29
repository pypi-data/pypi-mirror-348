# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 17:26:18 2024

@author: lafields2
"""

import cv2
import matplotlib.pyplot as plt
import os

def manual_register_he_msi(pts_ms, pts_he,resized_msi_image,cropped_image,output_directory,sample_name):
    M, inliers = cv2.estimateAffinePartial2D(pts_ms, pts_he) # Compute the affine transformation matrix
    """
    Manually registers an MSI image to an H&E image using affine transformation.

    Parameters
    ----------
    pts_ms : numpy.ndarray
        Coordinates from the MSI image (source points).

    pts_he : numpy.ndarray
        Corresponding coordinates from the H&E image (destination points).

    resized_msi_image : numpy.ndarray
        The resized MSI image to be registered.

    cropped_image : numpy.ndarray
        The cropped and smoothed H&E image.

    output_directory : str
        Directory where the transformed MSI image will be saved.

    sample_name : str
        Name used for labeling the saved output file.

    Returns
    -------
    M : numpy.ndarray
        The estimated affine transformation matrix.

    transformed_ms_image : numpy.ndarray
        The transformed MSI image after registration.

    Notes
    -----
    - Uses OpenCV's `cv2.estimateAffinePartial2D` to calculate the affine matrix.
    - Applies the transformation to the resized MSI image.
    - Displays and saves the transformed MSI image alongside the original images.
    - Assumes the input points are selected manually or computed separately.
    """
    transformed_ms_image = cv2.warpAffine(resized_msi_image, M, (cropped_image.shape[1], cropped_image.shape[0])) # Assume ms_image and he_image are your numpy arrays representing the images
    fig, axes = plt.subplots(1, 3, figsize=(18, 6)) # Create a figure with three subplots side by side
    # First panel: Cropped, smoothed H&E image
    axes[0].imshow(cropped_image, cmap='gray')
    axes[0].set_title('Cropped, smoothed H&E image')
    axes[0].axis('off')  # Hide the axes
    # Second panel: Interpolated MSI image
    axes[1].imshow(resized_msi_image, cmap='gray')
    axes[1].set_title('Interpolated MSI image')
    axes[1].axis('off')  # Hide the axes
    # Third panel: Transformed image
    axes[2].imshow(transformed_ms_image, cmap='gray')
    axes[2].set_title('Transformed image')
    axes[2].axis('off')  # Hide the axes
    plt.show()
    #fig_outpath = output_directory + '\\' + sample_name + '_manual_affine_transformed_MSI.png'
    fig_outpath = os.path.join(output_directory,f"{sample_name}_manual_affine_transformed_MSI.png")
    plt.savefig(fig_outpath,bbox_inches='tight')
    transformed_ms_image = transformed_ms_image.astype(cropped_image.dtype)
    return M,transformed_ms_image