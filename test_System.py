"""
File: test_System.py
Author: Danyal Mohaddes
Description: This file contains coverage tests for the System class.
"""

import os
import pytest
import System

@pytest.fixture
def system():
    return System.System(autopilot_=False)

def test_init(system):
    assert "khod-kaar" in system.cwd

def test_prepare_command(system):
    temp_file_path = system._prepare_command(llm_code_='echo "requests\nbeautifulsoup4\npandas" > requirements.txt')
    with open(temp_file_path, 'r') as fp:
        lines = fp.readlines()
        n_lines = len(lines)
    os.remove(temp_file_path)
    # 3 from command, 3 from split_kwd + pwd
    assert n_lines == 3 + 3