# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 17:27:23 2024

@author: lafields2
"""

import plotly.express as px
import cv2
import matplotlib.pyplot as plt

def show_msi_he_coords(final_MSI_image,final_he_image):
    fig = px.imshow(final_MSI_image,title='MSI Image')
    fig.show()
    rotated_array = final_he_image
    fig = px.imshow(rotated_array,title='H&E Image')
    fig.show()

def manual_register_he_msi(pts_ms, pts_he,resized_msi_image,cropped_image,output_directory,sample_name):
    M, inliers = cv2.estimateAffinePartial2D(pts_ms, pts_he) # Compute the affine transformation matrix
    transformed_ms_image = cv2.warpAffine(resized_msi_image, M, (cropped_image.shape[1], cropped_image.shape[0])) # Assume ms_image and he_image are your numpy arrays representing the images
    plt.imshow(cropped_image)
    plt.title('Cropped, smoothed H&E image')
    plt.show()
    plt.imshow(resized_msi_image)
    plt.title('Interpolated MSI image')
    plt.show()
    plt.imshow(transformed_ms_image)
    plt.title('Transformed image')
    fig_outpath = output_directory + '\\' + sample_name + '_manual_affine_transformed_MSI.png'
    plt.savefig(fig_outpath,bbox_inches='tight')
    transformed_ms_image = transformed_ms_image.astype(cropped_image.dtype)
    return M