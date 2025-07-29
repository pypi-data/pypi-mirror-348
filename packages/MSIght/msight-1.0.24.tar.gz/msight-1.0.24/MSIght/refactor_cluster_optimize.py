# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 17:12:18 2024

@author: lafields2
"""

import pyimzml.ImzMLParser
from scipy.ndimage import gaussian_filter1d,white_tophat
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import silhouette_score
from sklearn.cluster import DBSCAN
from sklearn.mixture import GaussianMixture
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering
from refactor_common_functions import load_and_preprocess_imzml,create_intensity_matrix,apply_dimensionality_reduction
import os

def kmeans_cluster_msi_scored_w_csv(filename, output_directory, sample_name, sigma, structuring_element_size, pca_components,
                tsne_components, tsne_verbose, k_means_cluster_number, max_clusters=10):
    """
    Performs t-SNE dimensionality reduction and K-means clustering on mass spectrometry imaging (MSI) data 
    and saves the clustering results as images and a CSV file.

    Parameters
    ----------
    filename : str
        Path to the .imzML file containing the MSI data.

    output_directory : str
        Directory where output files (images and CSV) will be saved.

    sample_name : str
        Name used to label the saved output files.

    sigma : float
        Standard deviation for Gaussian smoothing of the MSI data.

    structuring_element_size : int
        Size of the structuring element used for morphological operations.

    pca_components : int
        Number of principal components to retain during PCA.

    tsne_components : int
        Number of components for t-SNE dimensionality reduction.

    tsne_verbose : bool
        If True, enables verbose output for the t-SNE process.

    k_means_cluster_number : int
        Number of clusters for K-means clustering.

    max_clusters : int, optional, default=10
        Maximum number of clusters to consider during grid search.

    Returns
    -------
    df : pandas.DataFrame
        DataFrame containing t-SNE coordinates and cluster labels.

    width : int
        Width of the cluster image.

    height : int
        Height of the cluster image.

    tsne_result : numpy.ndarray
        Best t-SNE result based on the highest Silhouette score.

    Notes
    -----
    - Loads and preprocesses the MSI data from the .imzML file.
    - Applies PCA and t-SNE for dimensionality reduction.
    - Performs grid search over t-SNE parameters to optimize the Silhouette score.
    - Saves scatterplots of t-SNE embeddings and cluster images.
    - Stores the grid search results in a CSV file.
    - Returns the best t-SNE result along with relevant data and images.
    """
    coordinates, mz_values, intensities = load_and_preprocess_imzml(filename, sigma, structuring_element_size)
    df = pd.DataFrame({
        'x': [coord[0] for coord in coordinates],
        'y': [coord[1] for coord in coordinates],
        'mz_values': mz_values,
        'intensities': intensities})
    intensity_matrix, all_mz_values = create_intensity_matrix(coordinates, mz_values, intensities)
    intensity_df = pd.DataFrame(intensity_matrix, columns=all_mz_values) # Convert the intensity matrix to a DataFrame
    df_final = pd.concat([df[['x', 'y']], intensity_df], axis=1) # Combine coordinates with the intensity data
    perplexities = [5]
    learning_rates = [500]
    n_iters = [250]
    k_means_cluster_numbers = [2,3,4,5,6,7]
    best_silhouette = -1
    best_tsne_result = None
    results_list = [] # Initialize a list to store results
    for perplexity in perplexities: # Grid search over t-SNE parameters
        for learning_rate in learning_rates:
            for n_iter in n_iters:
                for k_means_cluster_number in k_means_cluster_numbers:
                    pca_result, tsne_result = apply_dimensionality_reduction(intensity_matrix, pca_components, tsne_components, perplexity,n_iter,learning_rate)
                    kmeans = KMeans(n_clusters=k_means_cluster_number) # Cluster using K-means
                    cluster_labels = kmeans.fit_predict(tsne_result)
                    silhouette_avg = silhouette_score(tsne_result, cluster_labels) # Calculate Silhouette score
                    print(f"Current Silhouette Score: {silhouette_avg}")
                    print(f"Best Silhouette Score: {best_silhouette}")
                    plt.figure(figsize=(16, 10))
                    sns.scatterplot(
                        x=tsne_result[:, 0], y=tsne_result[:, 1],
                        hue=cluster_labels,
                        #palette=sns.color_palette("tab10"),
                        legend="full",
                        alpha=0.6)
                    plt.title(f't-SNE with Perplexity={perplexity}, LR={learning_rate}, Iter={n_iter}, Silhouette={silhouette_avg:.3f}, K-means={k_means_cluster_number}')
                    #tsne_plot_outpath = f"{output_directory}\\{sample_name}_tSNE_p{perplexity}_lr{learning_rate}_iter{n_iter}_sil{silhouette_avg:.3f}_kmeans_{k_means_cluster_number}.png"
                    tsne_plot_outpath = os.path.join(output_directory,f'{sample_name}_tSNE_p{perplexity}_lr{learning_rate}_iter{n_iter}_sil{silhouette_avg}_kmeans_{k_means_cluster_number}.png')
                    plt.savefig(tsne_plot_outpath, bbox_inches='tight')
                    plt.close()
                    width, height = max(df['x']), max(df['y'])
                    cluster_image_full = np.zeros((width, height)) # Create the full cluster image
                    for idx, row in df.iterrows():
                        x, y = int(row['x']), int(row['y'])
                        cluster_image_full[x-1, y-1] = cluster_labels[idx]
                    plt.figure(figsize=(10, 10))
                    cmap = plt.cm.colors.ListedColormap([plt.cm.tab10(i) for i in range(k_means_cluster_number)])
                    im_full = plt.imshow(cluster_image_full, cmap=cmap, interpolation='nearest')
                    plt.title(f'Cluster Image with Perplexity={perplexity}, LR={learning_rate}, Iter={n_iter}, Silhouette={silhouette_avg:.3f}')
                    #cluster_plot_outpath = f"{output_directory}\\{sample_name}_ClusterImage_p{perplexity}_lr{learning_rate}_iter{n_iter}_sil{silhouette_avg:.3f}_kmeans_{k_means_cluster_number}.png"
                    cluster_plot_outpath = os.path.join(output_directory,f'{sample_name}_ClusterImage_p{perplexity}_lr{learning_rate}_iter{n_iter}_sil{silhouette_avg}_kmeans_{k_means_cluster_number}.png')
                    plt.savefig(cluster_plot_outpath, bbox_inches='tight')
                    plt.close()
                    results_list.append({
                        'Perplexity': perplexity,
                        'Learning Rate': learning_rate,
                        'Iterations': n_iter,
                        'Silhouette Score': silhouette_avg,
                        'Clusters': len(np.unique(cluster_labels))}) # Append the results to the list
                    if silhouette_avg > best_silhouette: # Check if this is the best score so far
                        best_silhouette = silhouette_avg
                        best_tsne_result = tsne_result
    results_df = pd.DataFrame(results_list) # Create a DataFrame from the results list
    #results_csv_outpath = f"{output_directory}\\{sample_name}_tSNE_Results.csv"
    results_csv_outpath = os.path.join(output_directory,f"{sample_name}_tSNE_Results.csv")
    results_df.to_csv(results_csv_outpath, index=False) # Save the results DataFrame as a CSV
    tsne_result = best_tsne_result # Use the best t-SNE result
    df['tsne-one'] = tsne_result[:, 0]
    df['tsne-two'] = tsne_result[:, 1]
    kmeans = KMeans(n_clusters=k_means_cluster_number) # Cluster using K-means with the best t-SNE result
    df['cluster'] = kmeans.fit_predict(tsne_result)
    return df, width, height, tsne_result


def bottom_up_hierarchical_clustering(filename, output_directory, sample_name, sigma, structuring_element_size, pca_components,
                                      tsne_components, tsne_verbose, max_clusters):
    """
    Performs bottom-up hierarchical clustering on mass spectrometry imaging (MSI) data 
    and evaluates cluster quality using Silhouette scores.

    Parameters
    ----------
    filename : str
        Path to the .imzML file containing the MSI data.

    output_directory : str
        Directory where output files (dendrogram and CSV) will be saved.

    sample_name : str
        Name used to label the saved output files.

    sigma : float
        Standard deviation for Gaussian smoothing of the MSI data.

    structuring_element_size : int
        Size of the structuring element used for morphological operations.

    pca_components : int
        Number of principal components to retain during PCA.

    tsne_components : int
        Number of components for t-SNE dimensionality reduction.

    tsne_verbose : bool
        If True, enables verbose output for the t-SNE process.

    max_clusters : int
        Maximum number of clusters to evaluate for Silhouette scores.

    Returns
    -------
    silhouette_df : pandas.DataFrame
        DataFrame containing the number of clusters and corresponding Silhouette scores.

    Notes
    -----
    - Loads and preprocesses the MSI data from the .imzML file.
    - Applies PCA followed by t-SNE for dimensionality reduction.
    - Performs hierarchical clustering using Ward's method.
    - Generates a dendrogram and saves it as a PNG file.
    - Computes Silhouette scores for cluster evaluations and saves them to a CSV file.
    """
    coordinates, mz_values, intensities = load_and_preprocess_imzml(filename, sigma, structuring_element_size)
    df = pd.DataFrame({
        'x': [coord[0] for coord in coordinates],
        'y': [coord[1] for coord in coordinates],
        'mz_values': mz_values,
        'intensities': intensities})
    intensity_matrix, all_mz_values = create_intensity_matrix(coordinates, mz_values, intensities)
    pca = PCA(n_components=pca_components)
    pca_result = pca.fit_transform(intensity_matrix)
    tsne = TSNE(n_components=tsne_components, verbose=tsne_verbose)
    tsne_result = tsne.fit_transform(pca_result)
    linkage_matrix = linkage(tsne_result, method='ward')
    plt.figure(figsize=(10, 7))
    dendrogram(linkage_matrix)
    plt.title('Hierarchical Clustering Dendrogram (Bottom-Up)')
    plt.xlabel('Data Points')
    plt.ylabel('Distance')
    #dendrogram_path = f"{output_directory}/{sample_name}_dendrogram_bottom_up.png"
    dendrogram_path = os.path.join(output_directory, f"{sample_name}_dendrogram_bottom_up.png")
    plt.savefig(dendrogram_path)
    plt.close()
    silhouette_scores = []
    for n_clusters in range(2, max_clusters+1):
        cluster = AgglomerativeClustering(n_clusters=n_clusters, affinity='euclidean', linkage='ward')
        labels = cluster.fit_predict(tsne_result)
        silhouette_avg = silhouette_score(tsne_result, labels)
        silhouette_scores.append((n_clusters, silhouette_avg))
    silhouette_df = pd.DataFrame(silhouette_scores, columns=['Number of Clusters', 'Silhouette Score'])
    #silhouette_csv = f"{output_directory}/{sample_name}_silhouette_scores_bottom_up.csv"
    silhouette_csv = os.path.join(output_directory, f"{sample_name}_silhouette_scores_bottom_up.csv")
    silhouette_df.to_csv(silhouette_csv, index=False) # Save silhouette scores to a DataFrame and CSV
    return silhouette_df