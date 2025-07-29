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
    all_mz_values = np.unique(np.concatenate(mz_values))
    intensity_matrix = np.zeros((len(coordinates), len(all_mz_values)))
    for i, (mzs, intens) in enumerate(zip(mz_values, intensities)):
        intensity_matrix[i, np.searchsorted(all_mz_values, mzs)] = intens
    return intensity_matrix, all_mz_values

def apply_dimensionality_reduction(intensity_matrix, pca_components, tsne_components, tsne_perplexity,tsne_interations,tsne_learning_rate):
    pca = PCA(n_components=pca_components)
    pca_result = pca.fit_transform(intensity_matrix)
    tsne = TSNE(n_components=tsne_components, perplexity=tsne_perplexity, n_iter=tsne_interations, learning_rate=tsne_learning_rate)
    tsne_result = tsne.fit_transform(pca_result)
    return pca_result, tsne_result

