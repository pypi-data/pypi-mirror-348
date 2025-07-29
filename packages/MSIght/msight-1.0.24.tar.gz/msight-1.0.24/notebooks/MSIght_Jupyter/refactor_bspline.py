# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 17:11:11 2024

@author: lafields2
"""

import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt

def perform_bspline(sized_he_image,transformed_ms_image,number_histograms,gradient_tolerance,optimizer_iterations,courseness):
    """
    Perform B-spline registration on two images using SimpleITK.

    This function refines an affine-transformed mass spectrometry image using a B-spline transformation.
    It computes an optimized transformation and applies it to align the image to the reference histological 
    image. The function also visualizes the original, affine-transformed, and refined images.

    Parameters
    ----------
    sized_he_image : np.ndarray
        The reference histological image (H&E-stained), expected as a 2D NumPy array of dtype `float32`.
    transformed_ms_image : np.ndarray
        The mass spectrometry image after affine transformation, expected as a 2D NumPy array of dtype `float32`.
    number_histograms : int
        The number of histogram bins for Mattes mutual information.
    gradient_tolerance : float
        The convergence tolerance for the optimizer.
    optimizer_iterations : int
        The maximum number of iterations allowed during optimization.
    courseness : int
        The grid spacing for the B-spline transform domain.

    Returns
    -------
    sitk.Transform
        The final optimized B-spline transformation.

    Notes
    -----
    - The function uses SimpleITK's BSplineTransformInitializer for the initial transform setup.
    - The Mattes mutual information metric is used to guide the registration process.
    - Visualization of the fixed, affine-transformed, and refined images is performed using Matplotlib.

    Examples
    --------
    >>> import numpy as np
    >>> sized_he_image = np.random.rand(1920, 2560).astype(np.float32)
    >>> transformed_ms_image = np.random.rand(1920, 2560).astype(np.float32)
    >>> final_transform = perform_bspline(
    ...     sized_he_image, transformed_ms_image, 
    ...     number_histograms=50, gradient_tolerance=1e-5, 
    ...     optimizer_iterations=100, courseness=50
    ... )
    """
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
