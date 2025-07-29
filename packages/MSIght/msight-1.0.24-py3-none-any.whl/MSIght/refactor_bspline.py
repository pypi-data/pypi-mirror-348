# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 17:11:11 2024

@author: lafields2
"""

import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt

def perform_bspline(sized_he_image,transformed_ms_image,number_histograms,gradient_tolerance,optimizer_iterations,courseness):
    fixed_image_sitk = sitk.GetImageFromArray(sized_he_image.astype(np.float32))
    transformed_ms_image_sitk = sitk.GetImageFromArray(transformed_ms_image.astype(np.float32))
    fixed_image_sitk = sitk.GetImageFromArray(sized_he_image.astype(np.float32))
    transformed_ms_image_sitk = sitk.GetImageFromArray(transformed_ms_image.astype(np.float32))
    grid_physical_spacing = [courseness, courseness]  # Can be adjusted to change the courseness of the B-spline, set to like 50
    b_spline_transform = sitk.BSplineTransformInitializer(image1=fixed_image_sitk, 
                                                          transformDomainMeshSize=[int(sz/grid) for sz, grid in zip(fixed_image_sitk.GetSize(), grid_physical_spacing)])
    parameters = np.zeros(b_spline_transform.GetNumberOfParameters())
    b_spline_transform.SetParameters(parameters)
    registration_method = sitk.ImageRegistrationMethod()
    registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=number_histograms) #set to like 50
    registration_method.SetShrinkFactorsPerLevel(shrinkFactors=[4, 2, 1])
    registration_method.SetSmoothingSigmasPerLevel(smoothingSigmas=[2, 1, 0])
    registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()
    registration_method.SetInitialTransform(b_spline_transform, inPlace=False)
    registration_method.SetOptimizerAsLBFGSB(gradientConvergenceTolerance=gradient_tolerance, numberOfIterations=optimizer_iterations) #tolerance should be 1e-5, iterations 100
    registration_method.SetOptimizerScalesFromPhysicalShift()
    registration_method.SetInterpolator(sitk.sitkLinear)
    final_transform = registration_method.Execute(fixed_image_sitk, transformed_ms_image_sitk)
    # Apply the final transformation to the transformed moving image (result of affine transformation)
    final_resampler = sitk.ResampleImageFilter()
    final_resampler.SetReferenceImage(fixed_image_sitk)
    final_resampler.SetInterpolator(sitk.sitkLinear)
    final_resampler.SetTransform(final_transform)
    final_resampler.SetDefaultPixelValue(0)
    final_refined_image_sitk = final_resampler.Execute(transformed_ms_image_sitk)
    final_refined_image = sitk.GetArrayFromImage(final_refined_image_sitk)
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 3, 1)
    plt.title('Fixed Image')
    plt.imshow(sized_he_image, cmap='gray')
    plt.subplot(1, 3, 2)
    plt.title('Affine Transformed Image')
    plt.imshow(transformed_ms_image, cmap='gray')
    plt.subplot(1, 3, 3)
    plt.title('B-Spline Refined Image')
    plt.imshow(final_refined_image, cmap='gray')
    plt.show()
    return final_transform
