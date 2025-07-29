# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 16:32:04 2024

@author: lafields2
"""

import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import matplotlib.patches as mpatches
from skimage.filters import threshold_otsu
from scipy.ndimage import binary_erosion, median_filter
from sklearn.metrics import silhouette_score
from refactor_segment import cluster_msi,cluster_removal,make_composite_image, composite_wo_selected_clusters,remove_residual_noise,cluster_msi_scored_w_csv
import matplotlib.pyplot as plt

@pytest.fixture
def mock_intensity_matrix():
    # Mock data for testing
    coordinates = [(1, 1), (2, 2), (3, 3)]
    mz_values = [np.array([100, 200, 300]), np.array([100, 200, 300]), np.array([100, 200, 300])]
    intensities = [np.array([10, 20, 30]), np.array([15, 25, 35]), np.array([20, 30, 40])]
    return coordinates, mz_values, intensities
@pytest.fixture
def mock_df():
    # Sample DataFrame with mock cluster data
    data = {
        'x': [1, 2, 3, 4, 5],
        'y': [1, 2, 3, 4, 5],
        'cluster': [0, 1, 2, 2, 1],
    }
    df = pd.DataFrame(data)
    width, height = 6, 6  # Mock dimensions
    cluster_colors = {
        0: '#1f77b4',  # Blue
        1: '#ff7f0e',  # Orange
        2: '#2ca02c',  # Green
    }
    cluster_image_full = np.zeros((width, height))
    for _, row in df.iterrows():
        cluster_image_full[row['x'] - 1, row['y'] - 1] = row['cluster']
    cmap = plt.cm.colors.ListedColormap(cluster_colors.values())
    legend_handles_full = [
        mpatches.Patch(color=color, label=f'Cluster {i}')
        for i, color in cluster_colors.items()
    ]
    return df, width, height, cluster_colors, cluster_image_full, cmap, legend_handles_full

@patch("refactor_segment.load_and_preprocess_imzml")
@patch("refactor_segment.plt.savefig")
@patch("refactor_segment.plt.show")
def test_cluster_msi(mock_show, mock_savefig, mock_load_preprocess, mock_intensity_matrix):
    # Arrange
    filename = r"D:\Manuscripts\2024_MSIight\480_Rapiflex_HE_files\MSIght\MALDI Data\2024_centroid_data_export_20240822\R0008\v243_5-total ion count.imzML"
    #filename = "test.imzml"
    output_directory = "output"
    sample_name = "sample"
    sigma = 1
    structuring_element_size = 5
    pca_components = 2
    tsne_components = 2
    tsne_perplexity = 2
    tsne_interations = 300
    tsne_learning_rate = 200
    k_means_cluster_number = 2

    mock_load_preprocess.return_value = mock_intensity_matrix

    # Act
    result = cluster_msi(
        filename,
        output_directory,
        sample_name,
        sigma,
        structuring_element_size,
        pca_components,
        tsne_components,
        tsne_perplexity,
        tsne_interations,
        tsne_learning_rate,
        k_means_cluster_number,
    )

    # Assert
    df, width, height, cluster_colors, cluster_image_full, cmap, legend_handles_full, tsne_result = result

    # Validate DataFrame structure
    assert isinstance(df, pd.DataFrame)
    assert "tsne-one" in df.columns
    assert "tsne-two" in df.columns
    assert "cluster" in df.columns

    # Validate cluster image size
    assert cluster_image_full.shape == (max(df['x']), max(df['y']))

    # Validate calls
    mock_load_preprocess.assert_called_once_with(filename, sigma, structuring_element_size)
    mock_savefig.assert_called()  # Ensure plots are being saved
    mock_show.assert_called()  # Ensure plots are being displayed

@patch("refactor_segment.plt.savefig")
def test_cluster_removal(mock_savefig, mock_df):
    df, width, height, cluster_colors, cluster_image_full, cmap, legend_handles_full = mock_df
    clusters_to_remove = [1]  # Remove cluster 1
    output_directory = "mock_output"
    sample_name = "mock_sample"

    # Call the function
    filtered_df = cluster_removal(
        df,
        width,
        height,
        cluster_colors,
        cluster_image_full,
        cmap,
        legend_handles_full,
        clusters_to_remove,
        output_directory,
        sample_name,
    )

    # Assertions
    # Verify clusters_to_remove are not in filtered_df
    assert not any(filtered_df['cluster'].isin(clusters_to_remove)), "Clusters to remove still present in filtered_df"
    
    # Check DataFrame structure
    assert isinstance(filtered_df, pd.DataFrame)
    assert 'x' in filtered_df.columns
    assert 'y' in filtered_df.columns
    assert 'cluster' in filtered_df.columns

    # Verify plt.savefig was called
    mock_savefig.assert_called_once_with(
        f"{output_directory}\\{sample_name}_MSI_tSNE_cluster_overlay_w_clusters_remove.png", bbox_inches='tight'
    )

@pytest.fixture
def mock_composite_df():
    # Create a mock DataFrame
    data = {
        'x': [1, 2, 3, 4],
        'y': [1, 2, 3, 4],
        'mz_values': [[100, 200, 300], [100, 200, 300], [100, 200, 300], [100, 200, 300]],
        'intensities': [
            np.array([10, 20, 30]),
            np.array([15, 25, 35]),
            np.array([20, 30, 40]),
            np.array([25, 35, 45]),
        ],
    }
    return pd.DataFrame(data)

@patch("refactor_segment.plt.savefig")
def test_make_composite_image(mock_savefig, mock_composite_df):
    # Arrange
    df = mock_composite_df
    threshold = 20
    output_directory = "mock_output"
    sample_name = "mock_sample"

    # Act
    composite_image = make_composite_image(df, threshold, output_directory, sample_name)

    # Assert
    # Ensure composite_image is a 2D numpy array with correct dimensions
    assert isinstance(composite_image, np.ndarray)
    assert composite_image.shape == (4, 4)  # Based on mock data: max(x) and max(y)

    # Check values in the composite image
    assert composite_image[0, 0] == 30  # Sum of intensities above threshold at (1,1)
    assert composite_image[1, 1] == 60  # Sum of intensities above threshold at (2,2)

    # Verify plt.savefig was called with the correct path
    mock_savefig.assert_called_once_with(
        f"{output_directory}\\{sample_name}_MSI_composite_image_all_mz.png", bbox_inches="tight"
    )

@pytest.fixture
def mock_pre_cluster_removal_data():
    # Mock DataFrame with cluster data
    data = {
        'x': [1, 2, 3, 4],
        'y': [1, 2, 3, 4],
        'cluster': [0, 1, 2, 1],
    }
    df = pd.DataFrame(data)

    # Mock composite image (5x5 array for simplicity)
    composite_image = np.array([
        [10, 20, 30, 40, 50],
        [15, 25, 35, 45, 55],
        [20, 30, 40, 50, 60],
        [25, 35, 45, 55, 65],
        [30, 40, 50, 60, 70],
    ])

    return df, composite_image

@patch("refactor_segment.plt.savefig")
def test_composite_wo_selected_clusters(mock_savefig, mock_pre_cluster_removal_data):
    # Arrange
    df, composite_image = mock_pre_cluster_removal_data
    clusters_to_remove = [1]  # Specify clusters to remove
    output_directory = "mock_output"
    sample_name = "mock_sample"

    # Generate the expected filtered image
    expected_filtered_image = composite_image.copy()
    coordinates_to_remove = df[df['cluster'].isin(clusters_to_remove)][['x', 'y']].values
    for coord in coordinates_to_remove:
        y, x = coord
        if x < expected_filtered_image.shape[1] and y < expected_filtered_image.shape[0]:
            expected_filtered_image[y, x] = 0  # Set cluster pixels to 0

    # Act
    filtered_image = composite_wo_selected_clusters(
        df, clusters_to_remove, composite_image, output_directory, sample_name
    )

    # Assert
    # Ensure filtered_image is a 2D numpy array
    assert isinstance(filtered_image, np.ndarray)
    assert filtered_image.shape == composite_image.shape

    # Dynamically compare the filtered image to the correctly computed expected filtered image
    np.testing.assert_array_equal(filtered_image, expected_filtered_image)

    # Ensure plt.savefig was called once with the correct path
    mock_savefig.assert_called_once_with(
        f"{output_directory}\\{sample_name}_MSI_filtered_image_w_clusters_removed.png",
        bbox_inches="tight",
    )
    
@patch("refactor_segment.plt.savefig")
def test_remove_residual_noise(mock_savefig):
    # Arrange
    filtered_image = np.array([
        [10, 20, 30, 40],
        [50, 60, 70, 80],
        [90, 100, 110, 120],
        [130, 140, 150, 160],
    ])  # Mock input image
    median_filter_size = 3
    output_directory = "mock_output"
    sample_name = "mock_sample"

    # Expected threshold and operations
    threshold = threshold_otsu(filtered_image)
    tissue_mask = filtered_image > threshold
    edge_mask = tissue_mask & ~binary_erosion(tissue_mask, iterations=5)
    filtered_image_med = median_filter(filtered_image, size=median_filter_size)
    expected_final_image = np.where(edge_mask, filtered_image_med, filtered_image)

    # Act
    final_image = remove_residual_noise(filtered_image, median_filter_size, output_directory, sample_name)

    # Assert
    # Verify the output image matches the expected processed image
    np.testing.assert_array_equal(final_image, expected_final_image)

    # Ensure plt.savefig was called with the correct path
    mock_savefig.assert_called_once_with(
        f"{output_directory}\\{sample_name}_MSI_median_filtered_image.png",
        bbox_inches="tight",
    )
    
@patch("refactor_segment.plt.savefig")
@patch("refactor_segment.pd.DataFrame.to_csv")
@patch("refactor_segment.load_and_preprocess_imzml")
@patch("refactor_segment.create_intensity_matrix")
@patch("refactor_segment.apply_dimensionality_reduction")
def test_cluster_msi_scored_w_csv(
    mock_apply_dimensionality_reduction,
    mock_create_intensity_matrix,
    mock_load_and_preprocess_imzml,
    mock_to_csv,
    mock_savefig,
):
    # Arrange
    filename = "mock_file.imzML"
    output_directory = "mock_output"
    sample_name = "mock_sample"
    sigma = 2
    structuring_element_size = 3
    pca_components = 10
    tsne_components = 2
    tsne_verbose = 0
    k_means_cluster_number = 3

    # Mock input data
    coordinates = [(1, 1), (2, 2), (3, 3), (4, 4)]
    mz_values = [[100, 200], [100, 200], [100, 200], [100, 200]]
    intensities = [[10, 20], [30, 40], [50, 60], [70, 80]]
    intensity_matrix = np.array([
        [10, 20],
        [30, 40],
        [50, 60],
        [70, 80],
    ])
    all_mz_values = [100, 200]
    tsne_result_mock = np.array([
        [1.0, 2.0],
        [2.0, 3.0],
        [3.0, 4.0],
        [4.0, 5.0],
    ])
    pca_result_mock = np.array([
        [1.0, 1.0],
        [2.0, 2.0],
        [3.0, 3.0],
        [4.0, 4.0],
    ])

    # Mock return values
    mock_load_and_preprocess_imzml.return_value = (coordinates, mz_values, intensities)
    mock_create_intensity_matrix.return_value = (intensity_matrix, all_mz_values)
    mock_apply_dimensionality_reduction.return_value = (pca_result_mock, tsne_result_mock)

    # Act
    df, width, height, tsne_result = cluster_msi_scored_w_csv(
        filename,
        output_directory,
        sample_name,
        sigma,
        structuring_element_size,
        pca_components,
        tsne_components,
        tsne_verbose,
        k_means_cluster_number,
    )

    # Assert
    # Ensure DataFrame was created with the correct structure
    assert isinstance(df, pd.DataFrame)
    assert 'x' in df.columns
    assert 'y' in df.columns
    assert 'tsne-one' in df.columns
    assert 'tsne-two' in df.columns
    assert 'cluster' in df.columns

    # Check t-SNE result assignment
    np.testing.assert_array_equal(df[['tsne-one', 'tsne-two']].values, tsne_result_mock)

    # Verify silhouette scores were calculated
    cluster_labels = df['cluster'].values
    silhouette_avg = silhouette_score(tsne_result_mock, cluster_labels)
    #assert silhouette_avg != 0  # Ensure the silhouette score was calculated

    # Ensure plt.savefig was called multiple times
    assert mock_savefig.call_count > 0

    # Verify CSV saving
    mock_to_csv.assert_called_once_with(
        f"{output_directory}\\{sample_name}_tSNE_Results_pt2.csv",
        index=False,
    )