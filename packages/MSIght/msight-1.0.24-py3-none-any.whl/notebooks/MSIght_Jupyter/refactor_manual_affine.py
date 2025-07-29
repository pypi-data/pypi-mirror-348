# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 17:27:23 2024

@author: lafields2
"""

import plotly.express as px
import cv2
import matplotlib.pyplot as plt
import os

def show_msi_he_coords(final_MSI_image,final_he_image):
    """
    Displays the MSI and H&E images side by side with coordinates using Plotly.

    Parameters
    ----------
    final_MSI_image : numpy.ndarray
        The final MSI image after interpolation and transformation.

    final_he_image : numpy.ndarray
        The final H&E image after processing and transformation.

    Returns
    -------
    None

    Notes
    -----
    - Uses Plotly's `imshow` for interactive visualization.
    - Displays coordinate axes for better comparison.
    - Titles the plots as 'MSI Image' and 'H&E Image'.
    """
    fig = px.imshow(final_MSI_image,title='MSI Image')
    fig.show()
    rotated_array = final_he_image
    fig = px.imshow(rotated_array,title='H&E Image')
    fig.show()

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

    Notes
    -----
    - Uses OpenCV's `cv2.estimateAffinePartial2D` to calculate the affine matrix.
    - Applies the transformation to the resized MSI image.
    - Displays and saves the transformed MSI image.
    - Assumes the input points are selected manually or computed separately.
    """
    transformed_ms_image = cv2.warpAffine(resized_msi_image, M, (cropped_image.shape[1], cropped_image.shape[0])) # Assume ms_image and he_image are your numpy arrays representing the images
    plt.imshow(cropped_image)
    plt.title('Cropped, smoothed H&E image')
    plt.show()
    plt.imshow(resized_msi_image)
    plt.title('Interpolated MSI image')
    plt.show()
    plt.imshow(transformed_ms_image)
    plt.title('Transformed image')
    #fig_outpath = output_directory + '\\' + sample_name + '_manual_affine_transformed_MSI.png'
    fig_outpath = os.path.join(output_directory, f"{sample_name}_manual_affine_transformed_MSI.png")
    plt.savefig(fig_outpath,bbox_inches='tight')
    transformed_ms_image = transformed_ms_image.astype(cropped_image.dtype)
    return M