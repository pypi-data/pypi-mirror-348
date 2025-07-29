# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 17:28:29 2024

@author: lafields2
"""

import pyimzml.ImzMLParser
from pyimzml.ImzMLParser import getionimage
import plotly.express as px
import cv2
import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt

def apply_bspline_transform_to_msi(b_spline_transform, msi_data_image):
    msi_image_sitk = sitk.GetImageFromArray(msi_data_image.astype(np.float32))
    resampler = sitk.ResampleImageFilter() # Apply the B-spline transformation using SimpleITK's ResampleImageFilter
    resampler.SetReferenceImage(msi_image_sitk)  # Use the MSI image's properties
    resampler.SetInterpolator(sitk.sitkLinear)
    resampler.SetTransform(b_spline_transform)
    resampler.SetDefaultPixelValue(0)
    transformed_msi_image_sitk = resampler.Execute(msi_image_sitk) # Perform the resampling
    transformed_msi_image = sitk.GetArrayFromImage(transformed_msi_image_sitk) # Convert the transformed MSI image back to a numpy array
    return transformed_msi_image

def extract_mz_image_transform(filename, mz, mz_tolerance, z_value, b_spline_apply, sized_he_image):
    parser = pyimzml.ImzMLParser.ImzMLParser(filename)
    mz_img = getionimage(parser, mz, tol=mz_tolerance, z=z_value,reduce_func=sum) # img stored as 2D numpy array
    fig = px.imshow(mz_img,title='MSI image @ m/z ' + str(mz))
    dimensions = sized_he_image.shape
    x_dimension = dimensions[1]
    y_dimension = dimensions[0]
    resized_msi_mz_image = cv2.resize(mz_img, (x_dimension,y_dimension), interpolation=cv2.INTER_LINEAR) # Resize MSI image to match dimensions of microscopy image
    msi_result = apply_bspline_transform_to_msi(b_spline_apply, resized_msi_mz_image)
    return msi_result

def overlay_msi_he(msi_result,sized_he_image,mz):
    msi_result = msi_result.astype(sized_he_image.dtype)
    overlay_mz = cv2.addWeighted(sized_he_image, 0.5, msi_result, 0.5, 0)
    plt.imshow(overlay_mz)
    plt.title('MSI/H&E overlay @ m/z ' + str(mz))