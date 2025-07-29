# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 17:43:09 2024

@author: lafields2
"""

import pytest
import numpy as np
from unittest.mock import patch, MagicMock
import cv2
from refactor_histology_preprocess import (
    load_he_image,
    foreground_mask_make,
    foreground_extract,
    red_channel_extract,
    bin_he_image,
    smooth_he_image,
    preprocess_he,
)

@patch("refactor_histology_preprocess.cv2.imread")
def test_load_he_image(mock_imread):
    # Arrange
    image_path = "mock_image.tiff"
    mock_image = np.ones((10, 10, 3), dtype=np.uint8)
    mock_imread.return_value = mock_image

    # Act
    result = load_he_image(image_path)

    # Assert
    mock_imread.assert_called_once_with(image_path)
    np.testing.assert_array_equal(result, mock_image)

@patch("refactor_histology_preprocess.cv2.bitwise_and")
def test_foreground_extract(mock_bitwise_and):
    # Arrange
    mock_image = np.ones((10, 10, 3), dtype=np.uint8)
    foreground_mask = np.ones((10, 10), dtype=np.uint8)
    foreground_image = np.ones((10, 10, 3), dtype=np.uint8) * 2
    mock_bitwise_and.return_value = foreground_image

    # Act
    result = foreground_extract(mock_image, foreground_mask)

    # Assert
    mock_bitwise_and.assert_called_once_with(mock_image, mock_image, mask=foreground_mask)
    np.testing.assert_array_equal(result, foreground_image)


def test_red_channel_extract():
    # Arrange
    mock_image = np.random.randint(0, 255, (10, 10, 3), dtype=np.uint8)
    expected_red_channel = mock_image[:, :, 2]

    # Act
    result = red_channel_extract(mock_image)

    # Assert
    np.testing.assert_array_equal(result, expected_red_channel)


@patch("refactor_histology_preprocess.cv2.threshold")
def test_bin_he_image(mock_threshold):
    # Arrange
    red_channel = np.random.randint(0, 255, (10, 10), dtype=np.uint8)
    threshold_value = 128
    thresholded_image = np.zeros((10, 10), dtype=np.uint8)
    mock_threshold.return_value = (None, thresholded_image)

    # Act
    result = bin_he_image(threshold_value, red_channel)

    # Assert
    mock_threshold.assert_called_once_with(red_channel, threshold_value, 255, cv2.THRESH_BINARY)
    np.testing.assert_array_equal(result, thresholded_image)


@patch("refactor_histology_preprocess.cv2.GaussianBlur")
def test_smooth_he_image(mock_gaussian_blur):
    # Arrange
    thresholded_image = np.random.randint(0, 255, (10, 10), dtype=np.uint8)
    smoothed_image = np.random.randint(0, 255, (10, 10), dtype=np.uint8)
    mock_gaussian_blur.return_value = smoothed_image

    # Act
    result = smooth_he_image(thresholded_image)

    # Assert
    mock_gaussian_blur.assert_called_once_with(thresholded_image, (5, 5), 0)
    np.testing.assert_array_equal(result, smoothed_image)