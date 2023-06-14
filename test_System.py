import os
import pytest
import System

@pytest.fixture
def system():
    return System.System(autopilot_=False)

def test_init(system):
    assert system.cwd == "/workspaces/khod-kaar"

def test_prepare_command(system):
    temp_file_path = system._prepare_command(llm_code_='echo "requests\nbeautifulsoup4\npandas" > requirements.txt')
    with open(temp_file_path, 'r') as fp:
        lines = fp.readlines()
        n_lines = len(lines)
    os.remove(temp_file_path)
    # 3 from command, 2 from split_kwd + pwd
    assert n_lines == 3 + 2