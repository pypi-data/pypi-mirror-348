# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 15:28:00 2024

@author: lafields2
"""

import pyimzml.ImzMLParser
from scipy.ndimage import gaussian_filter1d,white_tophat
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

def load_and_preprocess_imzml(filename, sigma, structuring_element_size):
    """
    Loads and preprocesses MSI data from an .imzML file by applying Gaussian smoothing 
    and top-hat baseline correction.

    Parameters
    ----------
    filename : str
        Path to the .imzML file containing the MSI data.

    sigma : float
        Standard deviation for Gaussian smoothing applied to the intensity values.

    structuring_element_size : int
        Size of the structuring element used for top-hat baseline correction.

    Returns
    -------
    coordinates : list of tuples
        List of pixel coordinates (x, y) from the .imzML file.

    mz_values : list of numpy.ndarray
        List of m/z values corresponding to each pixel.

    intensities : list of numpy.ndarray
        List of preprocessed intensity values for each pixel.

    Notes
    -----
    - Uses PyImzML to parse the .imzML file.
    - Applies Gaussian smoothing to reduce noise in the intensity spectra.
    - Applies top-hat baseline correction to remove background noise.
    - Returns preprocessed data suitable for further analysis.
    """
    parser = pyimzml.ImzMLParser.ImzMLParser(filename)
    coordinates, mz_values, intensities = [], [], []
    for idx, (x, y, z) in enumerate(parser.coordinates):
        mzs, intens = parser.getspectrum(idx)
        smoothed_intens = gaussian_filter1d(intens, sigma=sigma)
        baseline_corrected_intens = white_tophat(smoothed_intens, size=structuring_element_size)
        coordinates.append((x, y))
        mz_values.append(mzs)
        intensities.append(baseline_corrected_intens)
    return coordinates, mz_values, intensities

def create_intensity_matrix(coordinates, mz_values, intensities):
    """
    Creates an intensity matrix from preprocessed MSI data.

    Parameters
    ----------
    coordinates : list of tuples
        List of pixel coordinates (x, y) from the .imzML file.

    mz_values : list of numpy.ndarray
        List of m/z values corresponding to each pixel.

    intensities : list of numpy.ndarray
        List of preprocessed intensity values for each pixel.

    Returns
    -------
    intensity_matrix : numpy.ndarray
        A 2D array where each row represents a pixel, and each column corresponds to a unique m/z value.

    all_mz_values : numpy.ndarray
        A sorted array of unique m/z values across all pixels.

    Notes
    -----
    - Extracts unique m/z values across all pixels.
    - Initializes an intensity matrix with zeros.
    - Fills the matrix with intensity values using `np.searchsorted` for fast indexing.
    - Returns the intensity matrix and the corresponding m/z values.
    """
    all_mz_values = np.unique(np.concatenate(mz_values))
    intensity_matrix = np.zeros((len(coordinates), len(all_mz_values)))
    for i, (mzs, intens) in enumerate(zip(mz_values, intensities)):
        intensity_matrix[i, np.searchsorted(all_mz_values, mzs)] = intens
    return intensity_matrix, all_mz_values

def apply_dimensionality_reduction(intensity_matrix, pca_components, tsne_components, tsne_perplexity,tsne_interations,tsne_learning_rate):
    """
    Applies PCA and t-SNE for dimensionality reduction on an intensity matrix.

    Parameters
    ----------
    intensity_matrix : numpy.ndarray
        The 2D array where rows correspond to pixels and columns correspond to m/z values.

    pca_components : int
        Number of principal components to retain during PCA.

    tsne_components : int
        Number of components for t-SNE dimensionality reduction.

    tsne_perplexity : float
        Perplexity parameter for t-SNE, balancing local and global data structure.

    tsne_iterations : int
        Number of iterations for the t-SNE optimization process.

    tsne_learning_rate : float
        Learning rate parameter for t-SNE, controlling the step size during optimization.

    Returns
    -------
    pca_result : numpy.ndarray
        PCA-transformed matrix of reduced dimensions.

    tsne_result : numpy.ndarray
        t-SNE-transformed matrix of reduced dimensions.

    Notes
    -----
    - Applies PCA for initial dimensionality reduction to speed up t-SNE.
    - Applies t-SNE on the PCA-transformed matrix for further reduction.
    - Returns both PCA and t-SNE results for further analysis or visualization.
    """
    pca = PCA(n_components=pca_components)
    pca_result = pca.fit_transform(intensity_matrix)
    tsne = TSNE(n_components=tsne_components, perplexity=tsne_perplexity, n_iter=tsne_interations, learning_rate=tsne_learning_rate)
    tsne_result = tsne.fit_transform(pca_result)
    return pca_result, tsne_result

