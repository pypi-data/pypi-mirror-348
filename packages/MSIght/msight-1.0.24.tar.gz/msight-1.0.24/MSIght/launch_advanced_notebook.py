# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 17:37:28 2024

@author: lafields2
"""

import os
import subprocess

def main():
    # Define the absolute path relative to the current working directory
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    notebook_path = os.path.join(root_path, "notebooks", "advanced_workflow.ipynb")

    if not os.path.exists(notebook_path):
        print(f"Advanced notebook file not found: {notebook_path}")
        return
    
    print(f"Launching advanced notebook at {notebook_path}...")
    # Use subprocess to launch the notebook
    subprocess.run(["jupyter", "notebook", notebook_path], check=True)
    