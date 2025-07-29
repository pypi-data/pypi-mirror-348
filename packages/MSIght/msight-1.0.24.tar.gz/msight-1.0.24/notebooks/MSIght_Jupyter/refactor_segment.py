# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 16:33:13 2024

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
import matplotlib.patches as mpatches
from skimage import filters
from scipy.ndimage import median_filter, binary_erosion
from sklearn.metrics import silhouette_score
import os
from MSIght_Jupyter.refactor_common_functions import load_and_preprocess_imzml,create_intensity_matrix,apply_dimensionality_reduction

def cluster_msi(filename,output_directory,sample_name,sigma,structuring_element_size,pca_components,
           tsne_components,tsne_perplexity,tsne_interations,tsne_learning_rate,k_means_cluster_number):
    """
    Performs t-SNE dimensionality reduction and K-means clustering on MSI data.

    Parameters
    ----------
    filename : str
        Path to the .imzML file containing the MSI data.

    output_directory : str
        Directory where output files (images and clusters) will be saved.

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

    tsne_perplexity : float
        Perplexity parameter for t-SNE, balancing local and global data structure.

    tsne_interations : int
        Number of iterations for the t-SNE optimization process.

    tsne_learning_rate : float
        Learning rate parameter for t-SNE, controlling the step size during optimization.

    k_means_cluster_number : int
        Number of clusters for K-means clustering.

    Returns
    -------
    df : pandas.DataFrame
        DataFrame containing t-SNE coordinates and cluster labels.

    width : int
        Width of the cluster image.

    height : int
        Height of the cluster image.

    cluster_colors : dict
        Dictionary mapping clusters to fixed colors.

    cluster_image_full : numpy.ndarray
        The full cluster image with pixel-level assignments.

    cmap : matplotlib.colors.ListedColormap
        Colormap for the clusters.

    legend_handles_full : list
        List of legend handles for custom legends.

    tsne_result : numpy.ndarray
        The t-SNE results after dimensionality reduction.

    Notes
    -----
    - Loads and preprocesses the MSI data from the .imzML file.
    - Applies PCA and t-SNE for dimensionality reduction.
    - Performs K-means clustering.
    - Visualizes the clustering results using scatterplots and MSI overlays.
    - Saves the t-SNE scatterplot and cluster image as PNG files.
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
    pca_result, tsne_result = apply_dimensionality_reduction(intensity_matrix, pca_components, tsne_components, tsne_perplexity,tsne_interations,tsne_learning_rate)
    df['tsne-one'] = tsne_result[:, 0] # Add t-SNE results back to DataFrame
    df['tsne-two'] = tsne_result[:, 1] # Add t-SNE results back to DataFrame
    kmeans = KMeans(n_clusters=k_means_cluster_number) # Cluster using K-means
    df['cluster'] = kmeans.fit_predict(pca_result)
    plt.figure(figsize=(16, 10)) # Visualize the t-SNE result
    sns.scatterplot(
        x="tsne-one", y="tsne-two",
        hue="cluster",
        #palette=sns.color_palette("tab10"),
        data=df,
        legend="full",
        alpha=0.6
    )
    plt.title('t-SNE of Mass Spectrometry Image with K-means Clustering')
    fig_outpath = os.path.join(output_directory, f"{sample_name}_tSNE_cluster.png")
    #fig_outpath = output_directory + '\\' + sample_name + '_tSNE_cluster.png'
    plt.savefig(fig_outpath)
    plt.show()
    
    # Define a fixed color map
    cluster_colors = {
        0: '#1f77b4',  # Blue
        1: '#ff7f0e',  # Orange
        2: '#2ca02c',  # Green
        3: '#d62728',  # Red
        4: '#9467bd',  # Purple
        5: '#EC2E8C',  # Pink
        6: '#f032e6',  # Yellow
        7: '#9CE060',  # Light green
    }
    cmap = plt.cm.colors.ListedColormap([cluster_colors[i] for i in range(k_means_cluster_number)]) # Create a colormap for the clusters
    width, height = max(df['x']), max(df['y'])
    cluster_image_full = np.zeros((width, height)) # Create the full cluster image
    for idx, row in df.iterrows():
        x, y = int(row['x']), int(row['y'])
        cluster_image_full[x-1, y-1] = row['cluster']
    plt.figure(figsize=(10, 10))
    plt.imshow(cluster_image_full, cmap=cmap, interpolation='nearest')
    plt.title('Cluster Image of Tissue Spectra')
    plt.colorbar()
    plt.show() # Display the full cluster image
    unique_clusters_full = np.unique(df['cluster'])
    legend_handles_full = [mpatches.Patch(color=cluster_colors[i], label=f'Cluster {i}') for i in unique_clusters_full] # Create custom legend handles for both images
    plt.figure(figsize=(10, 10))
    im_full = plt.imshow(cluster_image_full, cmap=cmap, interpolation='nearest')
    plt.title('Full Clustered Mass Spectrometry Image')
    plt.axis('off')
    plt.legend(handles=legend_handles_full, loc='upper right')
    #fig_outpath = output_directory + '\\' + sample_name + '_MSI_tSNE_cluster_overlay.png'
    fig_outpath = os.path.join(output_directory, f"{sample_name}_MSI_tSNE_cluster_overlay.png")
    plt.savefig(fig_outpath,bbox_inches='tight')
    #fig_outpath = output_directory + '\\' + sample_name + '_MSI_tSNE_cluster_overlay.png'
    fig_outpath = os.path.join(output_directory,f"{sample_name}_MSI_tSNE_cluster_overlay.png")
    plt.savefig(fig_outpath,bbox_inches='tight')
    return df,width, height,cluster_colors,cluster_image_full,cmap,legend_handles_full,tsne_result

def cluster_removal(df,width,height,cluster_colors,cluster_image_full,cmap,legend_handles_full,clusters_to_remove,output_directory,sample_name):
    """
    Creates a composite MSI image by aggregating pixel intensities above a threshold.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing MSI pixel data with coordinates and intensities.

    threshold : float
        Intensity threshold for filtering pixel values.

    output_directory : str
        Directory where the composite image will be saved.

    sample_name : str
        Name used for labeling the saved output file.

    Returns
    -------
    composite_image : numpy.ndarray
        Composite MSI image where pixel values represent the sum of intensities above the threshold.

    Notes
    -----
    - Filters intensities based on the specified threshold.
    - Aggregates intensities into a composite image.
    - Displays and saves the composite image as a PNG file.
    """
    filtered_df = df[~df['cluster'].isin(clusters_to_remove)] # Filter out the rows with clusters to remove
    cluster_image_filtered = np.zeros((width, height)) - 1  # Initialize with -1 to handle missing data
    for idx, row in filtered_df.iterrows():
        x, y = int(row['x']), int(row['y'])
        cluster_image_filtered[x-1, y-1] = row['cluster']
    unique_clusters_filtered = np.unique(filtered_df['cluster']) # Create the cluster image without specific clusters
    legend_handles_filtered = [mpatches.Patch(color=cluster_colors[i], label=f'Cluster {i}') for i in unique_clusters_filtered]
    fig, axes = plt.subplots(1, 2, figsize=(20, 10))
    im_full = axes[0].imshow(cluster_image_full, cmap=cmap, interpolation='nearest')
    axes[0].set_title('Full Clustered Mass Spectrometry Image')
    axes[0].axis('off')
    axes[0].legend(handles=legend_handles_full, loc='upper right')
    cmap_filtered = plt.cm.colors.ListedColormap([cluster_colors[i] for i in unique_clusters_filtered]) # Filtered cluster image
    im_filtered = axes[1].imshow(cluster_image_filtered, cmap=cmap_filtered, interpolation='nearest')
    axes[1].set_title('Clustered Mass Spectrometry Image without Specific Clusters')
    axes[1].axis('off')
    axes[1].legend(handles=legend_handles_filtered, loc='upper right')
    #fig_outpath = output_directory + '\\' + sample_name + '_MSI_tSNE_cluster_overlay_w_clusters_remove.png'
    fig_outpath = os.path.join(output_directory, f"{sample_name}_MSI_tSNE_cluster_overlay_w_clusters_remove.png")
    plt.savefig(fig_outpath,bbox_inches='tight')
    return filtered_df

def make_composite_image(df,threshold,output_directory,sample_name):
    """
    Creates a composite MSI image by aggregating pixel intensities above a specified threshold.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing MSI pixel data with coordinates, m/z values, and intensities.

    threshold : float
        Intensity threshold for filtering pixel values.

    output_directory : str
        Directory where the composite image will be saved.

    sample_name : str
        Name used for labeling the saved output file.

    Returns
    -------
    composite_image : numpy.ndarray
        Composite MSI image where pixel values represent the sum of intensities above the threshold.

    Notes
    -----
    - Filters intensities based on the specified threshold.
    - Aggregates intensities into a composite image.
    - Displays and saves the composite image as a PNG file.
    """
    def process_imzml(file_path):
        """
    Processes an .imzML file and extracts pixel coordinates, m/z values, and intensities.

    Parameters
    ----------
    file_path : str
        Path to the .imzML file containing the MSI data.

    Returns
    -------
    df : pandas.DataFrame
        DataFrame containing pixel coordinates ('x', 'y'), m/z values, and intensity spectra.

    Notes
    -----
    - Uses PyImzML to parse the .imzML file.
    - Extracts spectra for each pixel in the file.
    - Stores the data in a structured DataFrame for further processing.
    """
        parser = pyimzml.ImzMLParser(file_path)
        data = []
        for idx, (x, y, z) in enumerate(parser.coordinates):
            mzs, intens = parser.getspectrum(idx)
            data.append((x, y, mzs, intens))
        df = pd.DataFrame(data, columns=['x', 'y', 'mz_values', 'intensities'])
        return df
    def filter_intensities_above_threshold(mz_values, intensities, threshold): # Function to filter intensities above a given threshold
        """
        Filters intensities that are above a given threshold.
    
        Parameters
        ----------
        mz_values : numpy.ndarray
            Array of m/z values.
    
        intensities : list of numpy.ndarray
            List of intensity spectra corresponding to the m/z values.
    
        threshold : float
            Intensity threshold for filtering pixel values.
    
        Returns
        -------
        filtered_intensities : numpy.ndarray
            Sum of intensities above the threshold for each pixel.
        """
        filtered_intensities = []
        for intens in intensities:
            mask = intens > threshold
            filtered_intensities.append(np.sum(intens[mask]))
        return np.array(filtered_intensities)
    def create_composite_image_for_intensity_threshold(df, threshold): # Function to create the composite image for intensities above a threshold
        """
        Creates a composite image by summing intensities above a threshold.
    
        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame containing MSI pixel data.
    
        threshold : float
            Intensity threshold for filtering pixel values.
    
        Returns
        -------
        composite_image : numpy.ndarray
            Composite MSI image with summed intensities above the threshold.
        """
        width, height = max(df['x']), max(df['y'])
        composite_image = np.zeros((width, height))
        mz_values = np.array(df['mz_values'].tolist())
        intensities = np.array(df['intensities'].tolist())
        filtered_intensities = filter_intensities_above_threshold(mz_values, intensities, threshold)
        for (x, y), intens in zip(df[['x', 'y']].values, filtered_intensities):
            composite_image[x-1, y-1] += intens
        return composite_image
    composite_image = create_composite_image_for_intensity_threshold(df, threshold) # Create the composite image for intensities above the threshold
    plt.figure(figsize=(10, 8)) # Plot the composite image with raw, unnormalized values using matplotlib
    plt.imshow(composite_image, cmap='gray')
    plt.colorbar()
    title = 'Composite Image for Intensities Above Threshold='+str(threshold)
    plt.title(title)
    #fig_outpath = output_directory + '\\' + sample_name + '_MSI_composite_image_all_mz.png'
    fig_outpath = os.path.join(output_directory, f"{sample_name}_MSI_composite_image_all_mz.png")
    plt.savefig(fig_outpath,bbox_inches='tight')
    return composite_image

def composite_wo_selected_clusters(df,clusters_to_remove,composite_image,output_directory,sample_name):
    """
    Creates a composite MSI image with specified clusters removed.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing MSI pixel data with coordinates and cluster labels.

    clusters_to_remove : list
        List of clusters to be removed from the composite image.

    composite_image : numpy.ndarray
        Original composite MSI image before removal.

    output_directory : str
        Directory where the filtered image will be saved.

    sample_name : str
        Name used for labeling the saved output file.

    Returns
    -------
    filtered_image : numpy.ndarray
        Composite MSI image with specified clusters removed.

    Notes
    -----
    - Filters out coordinates corresponding to the specified clusters.
    - Sets the pixel intensities of these coordinates to zero.
    - Displays and saves the updated composite image.
    """
    coordinates_to_remove = df[df['cluster'].isin(clusters_to_remove)][['x', 'y']].values
    list_coord = coordinates_to_remove.tolist()
    filtered_image = composite_image.copy()
    for coord in list_coord: # Set the specified coordinates to zero
        y, x = coord
        if x < filtered_image.shape[1] and y < filtered_image.shape[0]:
            filtered_image[y, x] = 0 
    plt.imshow(filtered_image, cmap='viridis')
    #fig_outpath = output_directory + '\\' + sample_name + '_MSI_filtered_image_w_clusters_removed.png'
    fig_outpath = os.path.join(output_directory, f"{sample_name}_MSI_filtered_image_w_clusters_removed.png")
    plt.savefig(fig_outpath,bbox_inches='tight')
    return filtered_image

def remove_residual_noise(filtered_image,median_filter_size,output_directory,sample_name):
    """
    Reduces residual noise from a filtered MSI image using median filtering along tissue edges.

    Parameters
    ----------
    filtered_image : numpy.ndarray
        The composite MSI image with clusters removed.

    median_filter_size : int
        Size of the median filter applied to the tissue edges.

    output_directory : str
        Directory where the filtered image will be saved.

    sample_name : str
        Name used for labeling the saved output file.

    Returns
    -------
    final_image : numpy.ndarray
        The MSI image after edge-based median filtering.

    Notes
    -----
    - Applies Otsu's thresholding to create a tissue mask.
    - Erodes the tissue mask to detect edges.
    - Applies median filtering to the detected edges.
    - Combines the filtered edges with the original tissue image.
    - Displays and saves the final image with filtered edges.
    """
    tissue_image = filtered_image.copy()
    threshold = filters.threshold_otsu(tissue_image)
    tissue_mask = tissue_image > threshold # Create a binary mask of the tissue region
    edge_mask = tissue_mask & ~binary_erosion(tissue_mask, iterations=5) # Erode the mask to create a mask for the edges
    filtered_image = median_filter(tissue_image, size=median_filter_size) # Apply the median filter to the entire image
    final_image = np.where(edge_mask, filtered_image, tissue_image) # Combine the filtered edges with the original image
    plt.figure(figsize=(18, 6)) # Plot the original, mask, and final images
    plt.subplot(1, 3, 1)
    plt.imshow(tissue_image, cmap='viridis')
    plt.title('Original Image')
    plt.colorbar()
    plt.subplot(1, 3, 2)
    plt.imshow(edge_mask, cmap='gray')
    plt.title('Edge Mask')
    plt.colorbar()
    plt.subplot(1, 3, 3)
    plt.imshow(final_image, cmap='viridis')
    plt.title('Final Image (Filtered Edges)')
    plt.colorbar()
    #fig_outpath = output_directory + '\\' + sample_name + '_MSI_median_filtered_image.png'
    fig_outpath = os.path.join(output_directory, f"{sample_name}_MSI_median_filtered_image.png")
    plt.savefig(fig_outpath,bbox_inches='tight')
    return final_image

def cluster_msi_scored_w_csv(filename, output_directory, sample_name, sigma, structuring_element_size, pca_components,
                tsne_components, tsne_verbose, k_means_cluster_number):
    """
    Performs t-SNE dimensionality reduction and K-means clustering on MSI data, scoring results with Silhouette scores.

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

    tsne_verbose : int
        Verbosity level for t-SNE.

    k_means_cluster_number : int
        Number of clusters for K-means clustering.

    Returns
    -------
    df : pandas.DataFrame
        DataFrame containing MSI coordinates, intensities, and clusters.

    width : int
        Width of the MSI image.

    height : int
        Height of the MSI image.

    tsne_result : numpy.ndarray
        The best t-SNE results after dimensionality reduction.

    Notes
    -----
    - Loads and preprocesses MSI data from the .imzML file.
    - Applies PCA and t-SNE for dimensionality reduction.
    - Performs K-means clustering and evaluates Silhouette scores.
    - Saves t-SNE scatterplots, cluster images, and a CSV file with scores.
    - Uses a grid search for the best t-SNE parameters.
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
    perplexities = [5, 10, 20, 30, 40, 50]
    learning_rates = [200, 250, 300, 350, 400, 450, 500]
    n_iters = [500, 750, 1000, 1500]
    best_silhouette = -1
    best_tsne_result = None
    results_list = [] # Initialize a list to store results
    # Grid search over t-SNE parameters
    for perplexity in perplexities:
        for learning_rate in learning_rates:
            for n_iter in n_iters:
                pca_result, tsne_result = apply_dimensionality_reduction(intensity_matrix, pca_components, tsne_components, perplexity,n_iter,learning_rate)
                kmeans = KMeans(n_clusters=k_means_cluster_number) # Cluster using K-means
                cluster_labels = kmeans.fit_predict(tsne_result)
                silhouette_avg = silhouette_score(tsne_result, cluster_labels) # Calculate Silhouette score
                # print(f"Current Silhouette Score: {silhouette_avg}")
                # print(f"Best Silhouette Score: {best_silhouette}")
                plt.figure(figsize=(16, 10)) # Create t-SNE scatterplot
                sns.scatterplot(
                    x=tsne_result[:, 0], y=tsne_result[:, 1],
                    hue=cluster_labels,
                    #palette=sns.color_palette("tab10"),
                    legend="full",
                    alpha=0.6
                )
                plt.title(f't-SNE with Perplexity={perplexity}, LR={learning_rate}, Iter={n_iter}, Silhouette={silhouette_avg:.3f}')
                #tsne_plot_outpath = f"{output_directory}\\{sample_name}_tSNE_p{perplexity}_lr{learning_rate}_iter{n_iter}_sil{silhouette_avg:.3f}.png"
                tsne_plot_outpath = os.path.join(output_directory, f"{sample_name}_tSNE_p{perplexity}_lr{learning_rate}_iter{n_iter}_sil{silhouette_avg}.png")
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
                #cluster_plot_outpath = f"{output_directory}\\{sample_name}_ClusterImage_p{perplexity}_lr{learning_rate}_iter{n_iter}_sil{silhouette_avg:.3f}.png"
                cluster_plot_outpath = os.path.join(output_directory, f"{sample_name}_ClusterImage_p{perplexity}_lr{learning_rate}_iter{n_iter}_sil{silhouette_avg}.png")
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
    #results_csv_outpath = f"{output_directory}\\{sample_name}_tSNE_Results_pt2.csv"     # Save the results DataFrame as a CSV
    results_csv_outpath = os.path.join(output_directory,f"{sample_name}_tSNE_Results_pt2.csv")
    results_df.to_csv(results_csv_outpath, index=False)
    tsne_result = best_tsne_result # Use the best t-SNE result
    df['tsne-one'] = tsne_result[:, 0]
    df['tsne-two'] = tsne_result[:, 1]
    kmeans = KMeans(n_clusters=k_means_cluster_number) # Cluster using K-means with the best t-SNE result
    df['cluster'] = kmeans.fit_predict(tsne_result)
    return df, width, height, tsne_result