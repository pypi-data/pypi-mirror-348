# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 18:35:55 2024

@author: lafields2
"""

import pytest
from unittest.mock import patch, MagicMock
import numpy as np
import pandas as pd

# Mocked functions - adjust the import path to match your actual code structure
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import seaborn as sns
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score
from sklearn.cluster import AgglomerativeClustering
# Import the function under test
from refactor_cluster_optimize import kmeans_cluster_msi_scored_w_csv

@pytest.fixture
def mock_load_and_preprocess_imzml():
    # Return coordinates, mz_values, intensities
    # Let's say we have a 10-pixel data set
    coordinates = [(x+1, x+1) for x in range(10)]  # (1,1), (2,2), ..., (10,10)
    mz_values = np.linspace(100, 200, 10)
    intensities = np.random.rand(10)
    return coordinates, mz_values, intensities

@pytest.fixture
def mock_create_intensity_matrix():
    # Create a small intensity matrix (10x10) and corresponding mz_values
    intensity_matrix = np.random.rand(10, 10)
    all_mz_values = np.linspace(100, 200, 10)
    return intensity_matrix, all_mz_values

@pytest.fixture
def mock_apply_dimensionality_reduction():
    # PCA and t-SNE results - say 2D t-SNE and PCA 
    pca_result = np.random.rand(10, 2)
    tsne_result = np.random.rand(10, 2)
    return pca_result, tsne_result

@patch('refactor_cluster_optimize.load_and_preprocess_imzml')
@patch('refactor_cluster_optimize.create_intensity_matrix')
@patch('refactor_cluster_optimize.apply_dimensionality_reduction')
@patch('matplotlib.pyplot.savefig')
@patch('pandas.DataFrame.to_csv')
def test_kmeans_cluster_msi_scored_w_csv(mock_to_csv, mock_savefig, mock_apply_dimred, mock_create_im, mock_load_pre):
    # Setup the mocks
    mock_load_pre.return_value = ([(x+1, x+1) for x in range(10)], 
                                  np.linspace(100, 200, 10),
                                  np.random.rand(10))
    mock_create_im.return_value = (np.random.rand(10, 10), np.linspace(100, 200, 10))
    # apply_dimensionality_reduction is called multiple times in grid search, 
    # we can always return the same mock result
    pca_res = np.random.rand(10, 2)
    tsne_res = np.random.rand(10, 2)
    mock_apply_dimred.return_value = (pca_res, tsne_res)
    
    # Now call the function with arbitrary parameters
    filename = "fake_file.imzML"
    output_directory = "fake_output"
    sample_name = "test_sample"
    sigma = 1
    structuring_element_size = 3
    pca_components = 2
    tsne_components = 2
    tsne_verbose = False
    k_means_cluster_number = 3
    max_clusters = 8

    df, width, height, tsne_result = kmeans_cluster_msi_scored_w_csv(
        filename, output_directory, sample_name, sigma, structuring_element_size,
        pca_components, tsne_components, tsne_verbose, k_means_cluster_number, max_clusters
    )

    # Assertions:
    # Check that we got a DataFrame back
    assert isinstance(df, pd.DataFrame), "The returned df is not a DataFrame."
    # We know from the mocks that we had 10 data points
    assert len(df) == 10, f"DataFrame should have 10 rows, got {len(df)}."
    assert 'tsne-one' in df.columns and 'tsne-two' in df.columns, "t-SNE columns not present in the DataFrame."
    assert 'cluster' in df.columns, "Cluster column not present in the DataFrame."

    # Check tsne_result is a numpy array
    assert isinstance(tsne_result, np.ndarray), "tsne_result is not a numpy array."
    assert tsne_result.shape == (10, 2), f"t-SNE result shape should be (10, 2), got {tsne_result.shape}."

    # Width and height are derived from the max coordinate; since we had coordinates (x+1,x+1),
    # max would be 10 for both width and height.
    assert width == 10, f"Expected width=10, got {width}."
    assert height == 10, f"Expected height=10, got {height}."

    # Check that file output functions were called
    # The function tries to save multiple plots and CSVs due to the grid search.
    mock_savefig.assert_called()  # At least one call should have happened
    mock_to_csv.assert_called_once()  # Results CSV should be written once

    print("Test passed!")
    
   