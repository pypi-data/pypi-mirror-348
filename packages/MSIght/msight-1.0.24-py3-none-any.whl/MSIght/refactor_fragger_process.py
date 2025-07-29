# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 17:19:57 2024

@author: lafields2
"""

import pandas as pd

def process_fragger(protein_oi_list,ppm_error,psm_path,sized_he_image,output_path):
    psm_report = pd.read_table(psm_path)
    filtered_psm_report = psm_report[psm_report['Is Unique'] == True]
    mass_h = 1.00784
    prot_storage = []
    num_unique_pep_storage = []
    pep_storage = []
    pep_mass_storage = []
    pep_mz_z1_storage = []
    da_err_threshold_storage = []
    ppm_err_threshold_storage = []
    scan_storage = []
    for a in protein_oi_list:
        filtered_protein_psm_report = filtered_psm_report[filtered_psm_report['Protein ID'] == a]
        number_unique_peptides = len(filtered_protein_psm_report.drop_duplicates(subset=['Peptide']))
        calc_mass_filter = filtered_protein_psm_report.drop_duplicates(subset=['Calculated Peptide Mass'])
        for line in range(0,len(calc_mass_filter)):
            peptide = calc_mass_filter['Peptide'].iloc[line]
            pep_mass = calc_mass_filter['Calculated Peptide Mass'].iloc[line]
            scan = calc_mass_filter['Spectrum'].iloc[line]
            da_err_equiv = abs(((ppm_error / 1000000) * pep_mass) - pep_mass)
            da_err_equiv = round(da_err_equiv,2)
            da_error = pep_mass - da_err_equiv
            da_error = round(da_error,2)
            prot_storage.append(a)
            num_unique_pep_storage.append(number_unique_peptides)
            pep_storage.append(peptide)
            pep_mass_storage.append(pep_mass)
            pep_mz_z1_storage.append(mass_h + pep_mass)
            da_err_threshold_storage.append(da_error)
            ppm_err_threshold_storage.append(ppm_error)
            scan_storage.append(scan)
        fragger_results_summary = pd.DataFrame()
        fragger_results_summary['Protein Name'] = prot_storage
        fragger_results_summary['# Unique Peptides'] = num_unique_pep_storage
        fragger_results_summary['Peptide'] = pep_storage
        fragger_results_summary['Peptide Theoretical Mass'] = pep_mass_storage
        fragger_results_summary['Peptide Theoretical m/z (+1)'] = pep_mz_z1_storage
        fragger_results_summary['ppm Error Threshold'] = ppm_err_threshold_storage
        fragger_results_summary['Calc. Da Error Threshold'] = da_err_threshold_storage
        fragger_results_summary['LC-MS/MS Scan'] = scan_storage
        output_path_report = output_path + '\\results_for_MSIght_other2Col.csv'
        fragger_results_summary.to_csv(output_path_report, index=False)
        return output_path_report

def process_fragger_gene(gene_oi_list,ppm_error,psm_path,sized_he_image,output_path):
    psm_report = pd.read_table(psm_path)
    filtered_psm_report = psm_report[psm_report['Is Unique'] == True]
    mass_h = 1.00784
    prot_storage = []
    num_unique_pep_storage = []
    pep_storage = []
    pep_mass_storage = []
    pep_mz_z1_storage = []
    da_err_threshold_storage = []
    ppm_err_threshold_storage = []
    scan_storage = []
    for a in gene_oi_list:
        filtered_protein_psm_report = filtered_psm_report[filtered_psm_report['Gene'] == a]
        number_unique_peptides = len(filtered_protein_psm_report.drop_duplicates(subset=['Peptide']))
        calc_mass_filter = filtered_protein_psm_report.drop_duplicates(subset=['Calculated Peptide Mass'])
        for line in range(0,len(calc_mass_filter)):
            peptide = calc_mass_filter['Peptide'].iloc[line]
            pep_mass = calc_mass_filter['Calculated Peptide Mass'].iloc[line]
            scan = calc_mass_filter['Spectrum'].iloc[line]
            da_err_equiv = abs(((ppm_error / 1000000) * pep_mass) - pep_mass)
            da_err_equiv = round(da_err_equiv,2)
            da_error = pep_mass - da_err_equiv
            da_error = round(da_error,2)
            prot_storage.append(a)
            num_unique_pep_storage.append(number_unique_peptides)
            pep_storage.append(peptide)
            pep_mass_storage.append(pep_mass)
            pep_mz_z1_storage.append(mass_h + pep_mass)
            da_err_threshold_storage.append(da_error)
            ppm_err_threshold_storage.append(ppm_error)
            scan_storage.append(scan)
        fragger_results_summary = pd.DataFrame()
        fragger_results_summary['Protein Name'] = prot_storage
        fragger_results_summary['# Unique Peptides'] = num_unique_pep_storage
        fragger_results_summary['Peptide'] = pep_storage
        fragger_results_summary['Peptide Theoretical Mass'] = pep_mass_storage
        fragger_results_summary['Peptide Theoretical m/z (+1)'] = pep_mz_z1_storage
        fragger_results_summary['ppm Error Threshold'] = ppm_err_threshold_storage
        fragger_results_summary['Calc. Da Error Threshold'] = da_err_threshold_storage
        fragger_results_summary['LC-MS/MS Scan'] = scan_storage
        output_path_report = output_path + '\\results_for_MSIght_other2Col.csv'
        fragger_results_summary.to_csv(output_path_report, index=False)
        return output_path_report
    
def process_fragger(protein_oi_list,ppm_error,psm_path,sized_he_image,output_path):
    psm_report = pd.read_table(psm_path)
    filtered_psm_report = psm_report[psm_report['Is Unique'] == True]
    mass_h = 1.00784
    prot_storage = []
    num_unique_pep_storage = []
    pep_storage = []
    pep_mass_storage = []
    pep_mz_z1_storage = []
    da_err_threshold_storage = []
    ppm_err_threshold_storage = []
    scan_storage = []
    for a in protein_oi_list:
        filtered_protein_psm_report = filtered_psm_report[filtered_psm_report['Protein ID'] == a]
        number_unique_peptides = len(filtered_protein_psm_report.drop_duplicates(subset=['Peptide']))
        calc_mass_filter = filtered_protein_psm_report.drop_duplicates(subset=['Calculated Peptide Mass'])
        for line in range(0,len(calc_mass_filter)):
            peptide = calc_mass_filter['Peptide'].iloc[line]
            pep_mass = calc_mass_filter['Calculated Peptide Mass'].iloc[line]
            scan = calc_mass_filter['Spectrum'].iloc[line]
            da_err_equiv = abs(((ppm_error / 1000000) * pep_mass) - pep_mass)
            da_err_equiv = round(da_err_equiv,2)
            da_error = pep_mass - da_err_equiv
            da_error = round(da_error,2)
            prot_storage.append(a)
            num_unique_pep_storage.append(number_unique_peptides)
            pep_storage.append(peptide)
            pep_mass_storage.append(pep_mass)
            pep_mz_z1_storage.append(mass_h + pep_mass)
            da_err_threshold_storage.append(da_error)
            ppm_err_threshold_storage.append(ppm_error)
            scan_storage.append(scan)
        fragger_results_summary = pd.DataFrame()
        fragger_results_summary['Protein Name'] = prot_storage
        fragger_results_summary['# Unique Peptides'] = num_unique_pep_storage
        fragger_results_summary['Peptide'] = pep_storage
        fragger_results_summary['Peptide Theoretical Mass'] = pep_mass_storage
        fragger_results_summary['Peptide Theoretical m/z (+1)'] = pep_mz_z1_storage
        fragger_results_summary['ppm Error Threshold'] = ppm_err_threshold_storage
        fragger_results_summary['Calc. Da Error Threshold'] = da_err_threshold_storage
        fragger_results_summary['LC-MS/MS Scan'] = scan_storage
        output_path_report = output_path + '\\results_for_MSIght_other2Col.csv'
        fragger_results_summary.to_csv(output_path_report, index=False)
        return output_path_report
    
def global_proteomics_search(fragger_results_path,threshold,min_prot_instances,ppm_error,output_path):
    psm_report = pd.read_table(fragger_results_path)
    filtered_psm_report = psm_report[psm_report['Is Unique'] == True]
    mass_h = 1.00784
    prot_storage = []
    num_unique_pep_storage = []
    pep_storage = []
    pep_mass_storage = []
    pep_mz_z1_storage = []
    da_err_threshold_storage = []
    ppm_err_threshold_storage = []
    scan_storage = []
    def filter_mass(filtered_psm_report):
        sorted_df = filtered_psm_report.sort_values(by='Calculated Peptide Mass')
        filtered_df = sorted_df[~sorted_df['Calculated Peptide Mass'].diff().between(-threshold, threshold) & 
                                ~sorted_df['Calculated Peptide Mass'].diff(-1).between(-threshold, threshold)]
        return filtered_df
    mass_dif_filtered_results = filter_mass(filtered_psm_report)
    filtered_df = mass_dif_filtered_results[mass_dif_filtered_results.groupby('Protein ID')['Protein ID'].transform('count') >= min_prot_instances]
    filtered_protein_list_df = filtered_df.drop_duplicates(subset='Protein ID')
    protein_oi_list = filtered_protein_list_df['Protein ID'].values.tolist()
    for a in protein_oi_list:
        filtered_protein_psm_report = filtered_psm_report[filtered_psm_report['Protein ID'] == a]
        number_unique_peptides = len(filtered_protein_psm_report.drop_duplicates(subset=['Peptide']))
        calc_mass_filter = filtered_protein_psm_report.drop_duplicates(subset=['Calculated Peptide Mass'])
        for line in range(0,len(calc_mass_filter)):
            peptide = calc_mass_filter['Peptide'].iloc[line]
            pep_mass = calc_mass_filter['Calculated Peptide Mass'].iloc[line]
            scan = calc_mass_filter['Spectrum'].iloc[line]
            da_err_equiv = abs(((ppm_error / 1000000) * pep_mass) - pep_mass)
            da_err_equiv = round(da_err_equiv,2)
            da_error = pep_mass - da_err_equiv
            da_error = round(da_error,2)
            prot_storage.append(a)
            num_unique_pep_storage.append(number_unique_peptides)
            pep_storage.append(peptide)
            pep_mass_storage.append(pep_mass)
            pep_mz_z1_storage.append(mass_h + pep_mass)
            da_err_threshold_storage.append(da_error)
            ppm_err_threshold_storage.append(ppm_error)
            scan_storage.append(scan)
    fragger_results_summary = pd.DataFrame()
    fragger_results_summary['Protein Name'] = prot_storage
    fragger_results_summary['# Unique Peptides'] = num_unique_pep_storage
    fragger_results_summary['Peptide'] = pep_storage
    fragger_results_summary['Peptide Theoretical Mass'] = pep_mass_storage
    fragger_results_summary['Peptide Theoretical m/z (+1)'] = pep_mz_z1_storage
    fragger_results_summary['ppm Error Threshold'] = ppm_err_threshold_storage
    fragger_results_summary['Calc. Da Error Threshold'] = da_err_threshold_storage
    fragger_results_summary['LC-MS/MS Scan'] = scan_storage
    output_path_report = output_path + '\\results_for_MSIght_untarget.csv'
    fragger_results_summary.to_csv(output_path_report, index=False)
    return output_path_report