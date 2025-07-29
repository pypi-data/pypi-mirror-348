# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 13:30:21 2025

@author: lafields2
"""

import os

def run_fragpipe(working_directory,generic_workflow_file,raw_files,fasta_db,fragpipe_path):
    manifest_path = os.path.join(working_directory, "fragpipe-files.fp-manifest")
    ###Write manifest file###

    with open(manifest_path, 'a') as f:
        for x in raw_files:
            f.write(f'{x}			DDA\n')
        f.close()

    ###Update workflow file###
    with open(generic_workflow_file, 'r') as file:
            lines = file.readlines()

    updated_lines = []
    for line in lines:
            if line.startswith("workdir="):
                updated_lines.append(f"workdir={working_directory}\n")
            elif line.startswith("database.db-path="):
                updated_lines.append(f"database.db-path={fasta_db}\n")
            else:
                updated_lines.append(line)

    workflow_path = f'{working_directory}\\fragpipe.workflow'
    with open(workflow_path, 'w') as file:
            file.writelines(updated_lines)

    os.system(fragpipe_path + ' --headless --workflow ' + workflow_path + ' --manifest ' + manifest_path + ' --workdir ' + working_directory)

# fragpipe_path = r"C:\Users\lawashburn\Downloads\FragPipe-22.0\fragpipe\bin\fragpipe.bat"
# working_directory = r"D:\Manuscripts\2024_MSIight\MSFragger_test\v08"
# generic_workflow_file = r"D:\Manuscripts\2024_MSIight\MSFragger_test\v07_wMouseProteome\fragpipe - Copy.workflow"
# raw_files = [r'D:\Manuscripts\2024_MSIight\480_Rapiflex_HE_files\MSIght\480_Data\20240702_R0008-R1.raw',r'D:\Manuscripts\2024_MSIight\480_Rapiflex_HE_files\MSIght\480_Data\20240702_R0008-R2.raw']
# fasta_db = r'D:\\Manuscripts\\2024_MSIight\\Raw_Files_No_Space\\2024-07-20-decoys-reviewed-contam-UP000000589.fas'

#run_fragpipe(working_directory,generic_workflow_file,raw_files,fasta_db,fragpipe_path)
