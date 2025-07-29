# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 18:29:12 2024

@author: lafields2
"""

import pytest
import numpy as np
import SimpleITK as sitk
from refactor_bspline import perform_bspline


@pytest.mark.parametrize("image_shape", [(64, 64), (128, 128)])
def test_perform_bspline(image_shape):
    # Create a simple synthetic "fixed" image: a gradient pattern
    sized_he_image = np.linspace(0, 255, num=image_shape[0]*image_shape[1], dtype=np.uint8).reshape(image_shape)

    # Create a slightly "transformed" moving image by shifting the gradient
    transformed_ms_image = np.roll(sized_he_image, shift=5, axis=1)

    # Set parameters for the B-spline registration
    number_histograms = 50
    gradient_tolerance = 1e-5
    optimizer_iterations = 5   # Reduced for test speed; in practice might be higher
    courseness = 50

    # Execute the function
    final_transform = perform_bspline(
        sized_he_image,
        transformed_ms_image,
        number_histograms,
        gradient_tolerance,
        optimizer_iterations,
        courseness
    )

    # Check that the returned object is indeed a SimpleITK Transform
    assert isinstance(final_transform, sitk.Transform), "The returned object is not a SimpleITK Transform."

    # Check that the transform has a valid dimension
    # For 2D images, the transform should be 2D
    assert final_transform.GetDimension() == 2, "The transform dimension does not match the expected value."

    # (Optional) You could inspect transform parameters here if needed:
    # params = final_transform.GetParameters()
    # For a simple test, we just ensure it runs and returns a transform.
