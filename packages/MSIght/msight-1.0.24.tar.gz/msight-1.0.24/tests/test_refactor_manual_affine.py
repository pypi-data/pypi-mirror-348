# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 18:59:37 2024

@author: lafields2
"""

import pytest
from unittest.mock import patch, MagicMock
import numpy as np
import cv2
from matplotlib import pyplot as plt

from refactor_manual_affine import manual_register_he_msi

@patch('cv2.estimateAffinePartial2D')
@patch('cv2.warpAffine')
@patch('matplotlib.pyplot.savefig')
@patch('matplotlib.pyplot.show')
def test_manual_register_he_msi(mock_show, mock_savefig, mock_warpAffine, mock_estimateAffinePartial2D):
    # Create synthetic data
    pts_ms = np.array([[10, 10], [20, 20]], dtype=np.float32)
    pts_he = np.array([[12, 12], [22, 22]], dtype=np.float32)

    # Create synthetic images
    resized_msi_image = np.zeros((50, 50), dtype=np.uint8)
    cropped_image = np.zeros((50, 50), dtype=np.uint8)

    output_directory = "fake_output"
    sample_name = "test_sample"

    # Mock the return value of estimateAffinePartial2D
    # Suppose the transformation is a simple translation.
    mock_transform_matrix = np.array([[1, 0, 2],
                                      [0, 1, 2]], dtype=np.float32)
    mock_estimateAffinePartial2D.return_value = (mock_transform_matrix, np.array([True, True]))

    # Mock warpAffine to just return a shifted image
    # For simplicity, return the same image
    mock_transformed_image = np.zeros((50, 50), dtype=np.uint8)
    mock_warpAffine.return_value = mock_transformed_image

    # Call the function
    M = manual_register_he_msi(pts_ms, pts_he, resized_msi_image, cropped_image, output_directory, sample_name)

    # Assertions:
    # Check that estimateAffinePartial2D was called with the correct arguments
    mock_estimateAffinePartial2D.assert_called_once_with(pts_ms, pts_he)

    # Check that warpAffine was called with the correct parameters
    # warpAffine needs the input image, the transformation matrix, and the output size
    mock_warpAffine.assert_called_once()
    args, kwargs = mock_warpAffine.call_args
    assert np.array_equal(args[0], resized_msi_image), "warpAffine input image is incorrect."
    assert np.array_equal(args[1], mock_transform_matrix), "warpAffine transform matrix is incorrect."
    assert args[2] == (cropped_image.shape[1], cropped_image.shape[0]), "warpAffine output size is incorrect."

    # Check the returned matrix M
    assert np.array_equal(M, mock_transform_matrix), "Returned transformation matrix does not match expected."

    # Check that savefig was called once
    mock_savefig.assert_called_once()

    # Check that show was called twice for the first two images and once for the final image display (3 times total)
    # Actually, the code shows 3 images: cropped_image, resized_msi_image, and transformed_ms_image.
    # The code provided calls plt.show() after each of the first two images, and does not show after the third (it just saves).
    # If the code is as given, that would be 2 calls to show().
    # Adjust this assertion if the code changes.
    assert mock_show.call_count == 2, f"Expected 2 calls to show(), got {mock_show.call_count}"

    print("Test passed!")
