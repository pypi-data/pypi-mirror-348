# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 17:21:54 2024

@author: lafields2
"""

import matplotlib.pyplot as plt
import os
import cv2
from utils.mz_image_extract import extract_mz_image_transform
from utils.mz_image_extract import overlay_msi_he
import pandas as pd
import numpy as np


def merge_all_results(output_directory,sample_name,fragger_out,filename,sized_he_image,b_spline_apply):
    mz_image_dir_path = output_directory + '\\' + sample_name + '_mz_images'
    try:  
        os.mkdir(mz_image_dir_path)  
    except OSError:  
        pass
    ms_fragger_results = pd.read_csv(fragger_out)
    prot_list_df = ms_fragger_results.drop_duplicates(subset=['Protein Name'])
    prot_list = prot_list_df['Protein Name'].values.tolist()
    for b in prot_list:
        mz_image_dir_protein_path = mz_image_dir_path + '\\' + b + '_mz_images'
        try:  
            os.mkdir(mz_image_dir_protein_path)  
        except OSError:  
            pass
        prot_filtered_df = ms_fragger_results[ms_fragger_results['Protein Name'] == b]
        image_composite_array = []
        for c in range(0,len(prot_filtered_df)):
            mz = prot_filtered_df['Peptide Theoretical m/z (+1)'].iloc[c]
            tol = prot_filtered_df['Calc. Da Error Threshold'].iloc[c]
            z_value=1
            mz_image_transformed = extract_mz_image_transform(filename, mz, tol, z_value, b_spline_apply, sized_he_image)
            image_composite_array.append(mz_image_transformed)
            overlay_msi_he(mz_image_transformed,sized_he_image,mz)
        composite_image = np.sum(image_composite_array, axis=0)
        plt.imshow(composite_image)
        plt.title('Composite image for protein ' + str(b))
        plt.colorbar()
        fig_outpath = mz_image_dir_protein_path + '\\' + sample_name + '_protein_' + str(b) + '_composite_image.png'
        plt.savefig(fig_outpath,bbox_inches='tight')
        plt.clf()
        sized_he_image = sized_he_image.astype('uint8')
        composite_image = composite_image.astype('uint8')
        overlay_composite_image_5 = cv2.addWeighted(sized_he_image, 0.95, composite_image, 0.05, 0)
        plt.imshow(overlay_composite_image_5)
        plt.title('MSI/H&E overlay protein ' + str(b))
        plt.colorbar()
        fig_outpath = mz_image_dir_protein_path + '\\' + sample_name + '_protein_' + str(b) + '_overlay_composite_image_5percentweight.png'
        plt.savefig(fig_outpath,bbox_inches='tight')
        plt.clf()
        overlay_composite_image_10 = cv2.addWeighted(sized_he_image, 0.9, composite_image, 0.1, 0)
        plt.imshow(overlay_composite_image_10)
        plt.title('MSI/H&E overlay protein ' + str(b))
        plt.colorbar()
        fig_outpath = mz_image_dir_protein_path + '\\' + sample_name + '_protein_' + str(b) + '_overlay_composite_image_10percentweight.png'
        plt.savefig(fig_outpath,bbox_inches='tight')
        plt.clf()
        overlay_composite_image_15 = cv2.addWeighted(sized_he_image, 0.85, composite_image, 0.15, 0)
        plt.imshow(overlay_composite_image_15)
        plt.title('MSI/H&E overlay protein ' + str(b))
        plt.colorbar()
        fig_outpath = mz_image_dir_protein_path + '\\' + sample_name + '_protein_' + str(b) + '_overlay_composite_image_15percentweight.png'
        plt.savefig(fig_outpath,bbox_inches='tight')
        plt.clf()
        overlay_composite_image_50 = cv2.addWeighted(sized_he_image, 0.5, composite_image, 0.5, 0)
        plt.imshow(overlay_composite_image_50)
        plt.title('MSI/H&E overlay protein ' + str(b))
        plt.colorbar()
        fig_outpath = mz_image_dir_protein_path + '\\' + sample_name + '_protein_' + str(b) + '_overlay_composite_image_50percentweight.png'
        plt.savefig(fig_outpath,bbox_inches='tight')
        plt.clf()
        overlay_composite_image_20 = cv2.addWeighted(sized_he_image, 0.8, composite_image, 0.2, 0)
        plt.imshow(overlay_composite_image_20)
        plt.title('MSI/H&E overlay protein ' + str(b))
        plt.colorbar()
        fig_outpath = mz_image_dir_protein_path + '\\' + sample_name + '_protein_' + str(b) + '_overlay_composite_image_20percentweight.png'
        plt.savefig(fig_outpath,bbox_inches='tight')
        plt.clf()
        
def merge_all_results_gene_wise(output_directory,sample_name,fragger_out,filename,sized_he_image,b_spline_apply):
    mz_image_dir_path = output_directory + '\\' + sample_name + '_mz_images'
    try:  
        os.mkdir(mz_image_dir_path)  
    except OSError:  
        pass
    ms_fragger_results = pd.read_csv(fragger_out)
    prot_list_df = ms_fragger_results.drop_duplicates(subset=['Gene'])
    prot_list = prot_list_df['Gene'].values.tolist()
    for b in prot_list:
        mz_image_dir_protein_path = mz_image_dir_path + '\\' + b + '_mz_images'
        try:  
            os.mkdir(mz_image_dir_protein_path)  
        except OSError:  
            pass
        prot_filtered_df = ms_fragger_results[ms_fragger_results['Gene'] == b]
        image_composite_array = []
        for c in range(0,len(prot_filtered_df)):
            mz = prot_filtered_df['Peptide Theoretical m/z (+1)'].iloc[c]
            tol = prot_filtered_df['Calc. Da Error Threshold'].iloc[c]
            z_value=1
            mz_image_transformed = extract_mz_image_transform(filename, mz, tol, z_value, b_spline_apply, sized_he_image)
            image_composite_array.append(mz_image_transformed)
            overlay_msi_he(mz_image_transformed,sized_he_image,mz)
        composite_image = np.sum(image_composite_array, axis=0)
        plt.imshow(composite_image)
        plt.title('Composite image for gene ' + str(b))
        plt.colorbar()
        fig_outpath = mz_image_dir_protein_path + '\\' + sample_name + '_gene_' + str(b) + '_composite_image.png'
        plt.savefig(fig_outpath,bbox_inches='tight')
        plt.clf()
        sized_he_image = sized_he_image.astype('uint8')
        composite_image = composite_image.astype('uint8')
        overlay_composite_image_5 = cv2.addWeighted(sized_he_image, 0.95, composite_image, 0.05, 0)
        plt.imshow(overlay_composite_image_5)
        plt.title('MSI/H&E overlay gene ' + str(b))
        plt.colorbar()
        fig_outpath = mz_image_dir_protein_path + '\\' + sample_name + '_gene_' + str(b) + '_overlay_composite_image_5percentweight.png'
        plt.savefig(fig_outpath,bbox_inches='tight')
        plt.clf()
        overlay_composite_image_10 = cv2.addWeighted(sized_he_image, 0.9, composite_image, 0.1, 0)
        plt.imshow(overlay_composite_image_10)
        plt.title('MSI/H&E overlay gene ' + str(b))
        plt.colorbar()
        fig_outpath = mz_image_dir_protein_path + '\\' + sample_name + '_gene_' + str(b) + '_overlay_composite_image_10percentweight.png'
        plt.savefig(fig_outpath,bbox_inches='tight')
        plt.clf()
        overlay_composite_image_15 = cv2.addWeighted(sized_he_image, 0.85, composite_image, 0.15, 0)
        plt.imshow(overlay_composite_image_15)
        plt.title('MSI/H&E overlay gene ' + str(b))
        plt.colorbar()
        fig_outpath = mz_image_dir_protein_path + '\\' + sample_name + '_gene_' + str(b) + '_overlay_composite_image_15percentweight.png'
        plt.savefig(fig_outpath,bbox_inches='tight')
        plt.clf()
        overlay_composite_image_50 = cv2.addWeighted(sized_he_image, 0.5, composite_image, 0.5, 0)
        plt.imshow(overlay_composite_image_50)
        plt.title('MSI/H&E overlay gene ' + str(b))
        plt.colorbar()
        fig_outpath = mz_image_dir_protein_path + '\\' + sample_name + '_gene_' + str(b) + '_overlay_composite_image_50percentweight.png'
        plt.savefig(fig_outpath,bbox_inches='tight')
        plt.clf()
        overlay_composite_image_20 = cv2.addWeighted(sized_he_image, 0.8, composite_image, 0.2, 0)
        plt.imshow(overlay_composite_image_20)
        plt.title('MSI/H&E overlay gene ' + str(b))
        plt.colorbar()
        fig_outpath = mz_image_dir_protein_path + '\\' + sample_name + '_gene_' + str(b) + '_overlay_composite_image_20percentweight.png'
        plt.savefig(fig_outpath,bbox_inches='tight')
        plt.clf()