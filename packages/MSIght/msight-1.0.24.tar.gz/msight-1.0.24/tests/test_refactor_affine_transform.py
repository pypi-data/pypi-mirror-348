# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 17:33:42 2024

@author: lafields2
"""

import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from skimage.transform import AffineTransform
from skimage.registration import phase_cross_correlation
from scipy.optimize import minimize
from skimage import img_as_float
from refactor_affine_transform import register_he_msi

@patch("refactor_affine_transform.display_and_save_image")
@patch("refactor_affine_transform.plt.show")
@patch("refactor_affine_transform.warp")
@patch("refactor_affine_transform.phase_cross_correlation")
@patch("refactor_affine_transform.minimize")
@patch("refactor_affine_transform.cv2.cvtColor")
@patch("refactor_affine_transform.cv2.convertScaleAbs")
def test_register_he_msi(
    mock_convert_scale_abs,
    mock_cvt_color,
    mock_minimize,
    mock_phase_cross_correlation,
    mock_warp,
    mock_plt_show,
    mock_display_and_save_image,
):
    # Arrange
    cropped_image = np.random.randint(0, 255, (10, 10), dtype=np.uint8)
    resized_msi_image = np.random.randint(0, 255, (10, 10), dtype=np.uint8)
    msi_threshold = 128
    he_threshold = 128
    output_directory = "mock_output"
    sample_name = "mock_sample"

    # Mock grayscale conversion
    mock_convert_scale_abs.side_effect = lambda x: x
    mock_cvt_color.side_effect = lambda x, _: x

    # Mock phase_cross_correlation
    mock_phase_cross_correlation.return_value = (np.array([2, 3]), None, None)

    # Mock minimize
    mock_minimize.return_value = MagicMock(x=[1, 0, 2, 0, 1, 3])

    # Mock warp
    def warp_mock(image, transform):
        return np.zeros_like(image)  # Simulate the transformation output
    mock_warp.side_effect = warp_mock

    # Act
    optimal_M, final_registered_image = register_he_msi(
        cropped_image, resized_msi_image, msi_threshold, he_threshold, output_directory, sample_name
    )

    # Assert
    # Verify returned matrix and image
    assert isinstance(optimal_M, np.ndarray)
    assert optimal_M.shape == (3, 3)
    assert isinstance(final_registered_image, np.ndarray)
    assert final_registered_image.shape == cropped_image.shape

    # Verify `display_and_save_image` calls with NumPy array checks
    calls = mock_display_and_save_image.call_args_list
    for call in calls:
        args, _ = call  # Extract positional arguments from the call
        image_arg = args[0]
        assert isinstance(image_arg, np.ndarray)  # Ensure the first argument is a NumPy array
        assert image_arg.shape == cropped_image.shape  # Check array shape

    # Verify `phase_cross_correlation` was called once
    mock_phase_cross_correlation.assert_called_once()

    # Verify `minimize` was called once
    mock_minimize.assert_called_once()