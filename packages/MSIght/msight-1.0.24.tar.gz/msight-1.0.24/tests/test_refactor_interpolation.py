# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 18:04:10 2024

@author: lafields2
"""

import pytest
import numpy as np
from unittest.mock import patch, MagicMock
import cv2
from refactor_interpolation import interpolate_MSI

@patch("refactor_interpolation.tifffile.TiffFile")
@patch("refactor_interpolation.pyimzml.ImzMLParser.ImzMLParser")
@patch("refactor_interpolation.cv2.resize")
@patch("refactor_interpolation.plt.savefig")
def test_interpolate_MSI(mock_savefig, mock_resize, mock_imzml_parser, mock_tiff_file):
    filename = "mock_filename.imzML"
    image_path = "mock_image.tif"
    sample_name = "mock_sample"
    output_directory = "mock_output"
    smoothed_image = np.array([
        [0, 0, 10, 10],
        [0, 20, 30, 0],
        [10, 40, 50, 0],
        [0, 0, 0, 0]
    ], dtype=np.uint8)
    smoothed_image_binary = smoothed_image.copy()
    smoothed_image_binary[smoothed_image_binary > 0] = 1
    msi_image = np.random.randint(0, 255, (4, 4), dtype=np.uint8)
    mock_parser = MagicMock() # Mock the ImzMLParser
    mock_parser.imzmldict = {'max count of pixels x': 10, 'max count of pixels y': 10}
    mock_imzml_parser.return_value = mock_parser
    mock_tiff_page = MagicMock() # Mock the TIFF file reading
    mock_tiff_page.shape = (8, 8)  # Mocked dimensions of the TIFF image
    mock_tiff_file.return_value.__enter__.return_value.pages = [mock_tiff_page]
    resized_image = np.random.randint(0, 255, (8, 8), dtype=np.uint8) # Mock OpenCV resize
    mock_resize.return_value = resized_image
    cropped_image, resized_msi_image = interpolate_MSI(filename, image_path, msi_image, smoothed_image, output_directory, sample_name)
    assert resized_msi_image.shape == resized_image.shape # Check that dimensions of resized_msi_image and resized_image are the same
    mock_imzml_parser.assert_called_once_with(filename)
    mock_tiff_file.assert_called_once_with(image_path)
    mock_resize.assert_called_once()
    mock_savefig.assert_called_once()
    
import pytest
import numpy as np
from unittest.mock import patch, MagicMock
import cv2
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend for testing
from matplotlib import pyplot as plt

# Assume your function is in a file named visualization.py
from refactor_interpolation import interpolate_and_visualize

@pytest.fixture
def mock_parser():
    # Mock the ImzMLParser to return a controlled dictionary
    mock_parser = MagicMock()
    mock_parser.imzmldict = {
        'max count of pixels x': 100,
        'max count of pixels y': 80
    }
    return mock_parser

@pytest.fixture
def mock_tifffile():
    # Mock TiffFile reading to return pages with a known shape
    mock_page = MagicMock()
    # Simulate a TIFF image of shape (200, 250)
    mock_page.shape = (200, 250)
    mock_tif = MagicMock()
    mock_tif.__enter__.return_value = mock_tif
    mock_tif.pages = [mock_page]
    return mock_tif

@pytest.fixture
def mock_imzml_parser_class(mock_parser):
    # This fixture returns a patch object that, when used, returns mock_parser
    with patch('pyimzml.ImzMLParser.ImzMLParser', return_value=mock_parser):
        yield

@pytest.fixture
def mock_tiff_file_class(mock_tifffile):
    with patch('tifffile.TiffFile', return_value=mock_tifffile):
        yield

@pytest.fixture
def mock_cv2_resize():
    # Mock cv2.resize to return a known transformed image
    with patch.object(cv2, 'resize', side_effect=lambda img, dsize, interpolation: np.zeros((dsize[1], dsize[0]))):
        yield

@pytest.fixture
def mock_plt():
    with patch.object(plt, 'show') as mock_show, \
         patch.object(plt, 'savefig') as mock_savefig:
        yield mock_show, mock_savefig

def test_interpolate_and_visualize(mock_imzml_parser_class, mock_tiff_file_class, mock_cv2_resize, mock_plt):
    # Create a small synthetic MSI image and smoothed image
    # msi_image: for testing, let's say 50x40
    msi_image = np.random.rand(40, 50)
    # smoothed_image: same size, but binary-like pattern
    smoothed_image = np.zeros((40, 50))
    smoothed_image[10:30, 10:40] = 255  # a "region" to simulate something detected

    filename = "fake_file.imzML"
    image_path = "fake_image_path.tiff"
    output_directory = "fake_output_dir"
    sample_name = "test_sample"
    original_areas_to_zoom = {
        "Area1": (10, 10, 20, 20),
        "Area2": (5, 5, 15, 15)
    }

    cropped_image, resized_msi_image = interpolate_and_visualize(
        filename,
        image_path,
        msi_image,
        smoothed_image,
        output_directory,
        sample_name,
        original_areas_to_zoom
    )

    # Assertions:
    # Check the shapes of returned images
    # The cropped image is derived by identifying non-zero regions. 
    # In our synthetic data, we know we had a region from (10:30, 10:40).
    # After cropping, dimensions should be roughly (20, 30).
    assert cropped_image.shape == (20, 30), f"Unexpected cropped_image shape: {cropped_image.shape}"

    # resized_msi_image is produced by cv2.resize which we mocked to return zeros of expected dimension
    # The dimension should match the cropped_image dimension (as per code logic).
    # The code rescales MSI image from original MSI dims to cropped dims, and we have mocked resize to reflect that.
    assert resized_msi_image.shape == (20, 30), f"Unexpected resized_msi_image shape: {resized_msi_image.shape}"

    # Ensure that matplotlib functions were called
    mock_show, mock_savefig = mock_plt
    mock_show.assert_called_once()
    mock_savefig.assert_called_once()