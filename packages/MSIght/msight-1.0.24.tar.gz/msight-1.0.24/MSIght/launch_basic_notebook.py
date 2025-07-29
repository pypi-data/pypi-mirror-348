# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 09:37:05 2024

@author: lafields2
"""

import os
import subprocess

def main():
    # Define the absolute path relative to the current working directory
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    notebook_path = os.path.join(root_path, "notebooks", "basic_workflow.ipynb")

    if not os.path.exists(notebook_path):
        print(f"Notebook file not found: {notebook_path}")
        return
    
    print(f"Launching notebook at {notebook_path}...")
    # Use subprocess to launch the notebook
    subprocess.run(["jupyter", "notebook", notebook_path], check=True)
    
