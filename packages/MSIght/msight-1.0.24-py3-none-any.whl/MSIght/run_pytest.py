# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 16:50:40 2024

@author: lafields2
"""

import pytest
import os

if __name__ == "__main__":
    # Assuming run_pytest.py is in MSight:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    tests_dir = os.path.join(base_dir, "tests")
    pytest.main(["-v", tests_dir])