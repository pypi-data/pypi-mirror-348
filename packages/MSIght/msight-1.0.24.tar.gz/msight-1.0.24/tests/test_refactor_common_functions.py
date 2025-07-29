# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 18:55:43 2024

@author: lafields2
"""

import pytest
from unittest.mock import patch, MagicMock
import numpy as np
from scipy.ndimage import gaussian_filter1d
from skimage.morphology import white_tophat

from refactor_common_functions import load_and_preprocess_imzml,create_intensity_matrix,apply_dimensionality_reduction

@pytest.fixture
def mock_parser():
    # Create a mock parser object
    mock_parser = MagicMock()

    # Define coordinates
    mock_parser.coordinates = [(1, 1, 1), (2, 2, 1)]  # Two coordinates for testing

    # Define the getspectrum behavior
    # Let’s say each spectrum has 5 mz values and corresponding intensities
    mzs_1 = np.linspace(100, 200, 5)
    intensities_1 = np.array([10, 20, 30, 20, 10], dtype=float)

    mzs_2 = np.linspace(100, 200, 5)
    intensities_2 = np.array([5, 15, 25, 15, 5], dtype=float)

    def mock_getspectrum(idx):
        if idx == 0:
            return mzs_1, intensities_1
        elif idx == 1:
            return mzs_2, intensities_2
        else:
            raise IndexError("Index out of range")

    mock_parser.getspectrum.side_effect = mock_getspectrum

    return mock_parser

@patch('pyimzml.ImzMLParser.ImzMLParser')
def test_load_and_preprocess_imzml(mock_imzml_parser_class, mock_parser):
    # Setup the mock parser instance
    mock_imzml_parser_class.return_value = mock_parser

    filename = "fake_file.imzML"
    sigma = 1
    structuring_element_size = 3

    coordinates, mz_values, intensities = load_and_preprocess_imzml(
        filename, sigma, structuring_element_size
    )

    # Assertions
    # We passed two coordinates, so we expect 2 entries
    assert len(coordinates) == 2, f"Expected 2 coordinates, got {len(coordinates)}"
    assert len(mz_values) == 2, f"Expected 2 mz arrays, got {len(mz_values)}"
    assert len(intensities) == 2, f"Expected 2 intensity arrays, got {len(intensities)}"

    # Check the shape of the first spectrum
    assert len(mz_values[0]) == 5, "Expected 5 mz points in the first spectrum"
    assert len(intensities[0]) == 5, "Expected 5 intensity points in the first spectrum"
    
    # Check that the coordinates match what we mocked
    expected_coords = [(1, 1), (2, 2)]
    assert coordinates == expected_coords, f"Coordinates do not match expected: {coordinates} vs. {expected_coords}"

    # Check that preprocessing was applied.
    # The function applies gaussian_filter1d and white_tophat.
    # We know the input intensities had a certain shape. 
    # We won't deeply verify the correctness of the filtering 
    # (that’s part of SciPy/skimage), but we can at least 
    # ensure the output is not equal to the raw input.

    raw_intensity = np.array([10, 20, 30, 20, 10], dtype=float)
    processed_intensity = intensities[0]
    # They should differ after filtering. Let's just ensure they aren't identical.
    assert not np.array_equal(raw_intensity, processed_intensity), "Preprocessing did not alter intensities."

    print("Test passed!")

def test_create_intensity_matrix():
    # Suppose we have 3 pixels/coordinates
    coordinates = [(1, 1), (2, 2), (3, 3)]

    # mz_values for each coordinate (spectrum)
    mz_values = [
        np.array([100, 150, 200]),      # Spectrum 1
        np.array([100, 200, 250]),      # Spectrum 2
        np.array([150, 250, 300])       # Spectrum 3
    ]

    # Corresponding intensities for each spectrum
    intensities = [
        np.array([10, 20, 30]),         # Intensities for Spectrum 1
        np.array([5, 15, 25]),          # Intensities for Spectrum 2
        np.array([2, 22, 42])           # Intensities for Spectrum 3
    ]

    # Call the function
    intensity_matrix, all_mz_values = create_intensity_matrix(coordinates, mz_values, intensities)

    # We expect all_mz_values to be sorted and unique
    expected_all_mz_values = np.array([100, 150, 200, 250, 300])
    assert np.array_equal(all_mz_values, expected_all_mz_values), f"Expected {expected_all_mz_values}, got {all_mz_values}"

    # The intensity_matrix should have shape (3 (spectra) x 5 (unique mzs))
    assert intensity_matrix.shape == (3, 5), f"Expected shape (3,5), got {intensity_matrix.shape}"

    # Check the correct placement of intensities:
    # Spectrum 1 had mz=[100,150,200] => intensities=[10,20,30], so those should appear in the corresponding positions
    # Positions in all_mz_values: 100->0, 150->1, 200->2, 250->3, 300->4
    # Thus row 0 should be [10,20,30,0,0]
    np.testing.assert_array_equal(intensity_matrix[0], np.array([10,20,30,0,0]))

    # Spectrum 2: mz=[100,200,250], intensities=[5,15,25] => row 1 should be [5,0,15,25,0]
    np.testing.assert_array_equal(intensity_matrix[1], np.array([5,0,15,25,0]))

    # Spectrum 3: mz=[150,250,300], intensities=[2,22,42] => row 2 should be [0,2,0,22,42]
    np.testing.assert_array_equal(intensity_matrix[2], np.array([0,2,0,22,42]))

    print("Test passed!")
    
def test_apply_dimensionality_reduction():
    # Create a synthetic intensity matrix with 20 samples and 10 features
    np.random.seed(42)  # for reproducibility
    intensity_matrix = np.random.rand(20, 10)

    pca_components = 5
    tsne_components = 2
    tsne_perplexity = 5
    tsne_iterations = 300
    tsne_learning_rate = 200

    pca_result, tsne_result = apply_dimensionality_reduction(
        intensity_matrix,
        pca_components,
        tsne_components,
        tsne_perplexity,
        tsne_iterations,
        tsne_learning_rate
    )

    # Check shapes
    # PCA result should have shape (n_samples, pca_components)
    assert pca_result.shape == (20, pca_components), f"Expected PCA shape (20,{pca_components}), got {pca_result.shape}"

    # t-SNE result should have shape (n_samples, tsne_components)
    assert tsne_result.shape == (20, tsne_components), f"Expected t-SNE shape (20,{tsne_components}), got {tsne_result.shape}"

    # Check that the results are numeric arrays
    assert isinstance(pca_result, np.ndarray), "PCA result should be a numpy array."
    assert isinstance(tsne_result, np.ndarray), "t-SNE result should be a numpy array."

    print("Test passed!")