# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 17:26:18 2024

@author: lafields2
"""

import cv2
import matplotlib.pyplot as plt

def manual_register_he_msi(pts_ms, pts_he,resized_msi_image,cropped_image,output_directory,sample_name):
    M, inliers = cv2.estimateAffinePartial2D(pts_ms, pts_he) # Compute the affine transformation matrix
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
    fig_outpath = output_directory + '\\' + sample_name + '_manual_affine_transformed_MSI.png'
    plt.savefig(fig_outpath,bbox_inches='tight')
    transformed_ms_image = transformed_ms_image.astype(cropped_image.dtype)
    return M,transformed_ms_image