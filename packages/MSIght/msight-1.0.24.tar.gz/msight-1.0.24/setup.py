# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 09:15:08 2024

@author: lafields2
"""

from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="MSIght", 
    version="1.0.24",
    author="Li Labs (University of Wisconsin-Madison)",
    author_email="lafields2@wisc.edu",
    description="MSIght is an open-source Python-based algorithm designed for proteome characterization from the automated integration of histology, LC-MS/MS, and MSI datasets.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/laurenfields/MSIght_1.0.0",  # Replace with your repo
    packages=find_packages(include=["MSIght", "notebooks"]),
    include_package_data=True,
    package_data={
        "MSIght": ["*.*"],                     # Include everything in MSIght
        "notebooks": ["*.ipynb", "**/*"],  # Include notebooks and subfolders
    },
    entry_points={
        "console_scripts": [
            "msight-notebook=MSIght.launch_basic_notebook:main",
            "msight-advanced=MSIght.launch_advanced_notebook:main"
        ]
    },
    project_urls={
        "Documentation": "https://msight-100.readthedocs.io/en/latest/?badge=latest",
        "PyPI": "https://pypi.org/project/msight/",
        "Source": "https://github.com/laurenfields/MSIght_1.0.0",
        "User manual": "https://docs.google.com/document/d/1LNEW0XPbH9mTnc5Fh0l7QC1vW48mU75P3hPOI2Tp66E/pub",
        "Tracker": "https://github.com/laurenfields/MSIght_1.0.0/issues",
    },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)