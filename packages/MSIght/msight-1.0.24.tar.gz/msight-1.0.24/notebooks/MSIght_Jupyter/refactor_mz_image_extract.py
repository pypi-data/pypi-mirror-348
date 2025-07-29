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
    """
    Applies a B-spline transformation to an MSI image using SimpleITK.

    Parameters
    ----------
    b_spline_transform : sitk.Transform
        The B-spline transformation object obtained from registration.

    msi_data_image : numpy.ndarray
        The MSI image to be transformed, expected as a 2D array.

    Returns
    -------
    transformed_msi_image : numpy.ndarray
        The transformed MSI image as a numpy array.

    Notes
    -----
    - Converts the input MSI image to a SimpleITK image.
    - Uses `sitk.ResampleImageFilter` to apply the B-spline transformation.
    - Sets the interpolator to linear and the default pixel value to 0.
    - Converts the transformed image back to a numpy array for further processing.
    """
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
    """
    Extracts an m/z image from an .imzML file, resizes it, and applies a B-spline transformation.

    Parameters
    ----------
    filename : str
        Path to the .imzML file containing the MSI data.

    mz : float
        The target m/z value to extract from the MSI data.

    mz_tolerance : float
        Tolerance for the target m/z value during image extraction.

    z_value : int
        Charge state value for m/z extraction.

    b_spline_apply : sitk.Transform
        The B-spline transform to apply to the extracted m/z image.

    sized_he_image : numpy.ndarray
        The reference H&E image used for resizing the MSI image.

    Returns
    -------
    msi_result : numpy.ndarray
        The transformed m/z image after resizing and applying the B-spline transform.

    Notes
    -----
    - Extracts an m/z image using `getionimage` from PyImzML.
    - Resizes the m/z image to match the H&E image's dimensions.
    - Applies a B-spline transformation using SimpleITK if provided.
    - Returns the transformed m/z image as a numpy array.
    """
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
    """
    Overlays an MSI image onto an H&E image and displays the result.

    Parameters
    ----------
    msi_result : numpy.ndarray
        The transformed MSI image.

    sized_he_image : numpy.ndarray
        The reference H&E image.

    mz : float
        The m/z value corresponding to the MSI image.

    Returns
    -------
    None

    Notes
    -----
    - Ensures the MSI image has the same data type as the H&E image.
    - Uses OpenCV's `cv2.addWeighted` for overlaying the images with equal weights.
    - Displays the overlay using Matplotlib.
    """
    msi_result = msi_result.astype(sized_he_image.dtype)
    overlay_mz = cv2.addWeighted(sized_he_image, 0.5, msi_result, 0.5, 0)
    plt.imshow(overlay_mz)
    plt.title('MSI/H&E overlay @ m/z ' + str(mz))