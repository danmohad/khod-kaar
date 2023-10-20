import os
import pytest
from Agent import Agent
from khod_kaar import khod_kaar


class MockArgs:
    """Class to mock the argparser"""

    def __init__(self, model_, output_dir_, temperature_, autopilot_, objective_):
        self.model = model_
        self.output_dir = output_dir_
        self.temperature = temperature_
        self.autopilot = autopilot_
        self.objective = objective_


@pytest.fixture
def simple_args():
    """Fixture to mock simple arguments to create a program that writes 'Hello, World!'."""
    
    args = ['gpt-4', 
            './output/', 
            0.0, 
            True, 
            "to write, test and execute a simple Python program that writes 'Hello, World!'."
    ]
    return MockArgs(*args)
    

def test_integration(simple_args):
    """Integration test for khod-kaar using simple_args.
    
    khod-kaar must execute without errors, and the generated program must print 'Hello, World!'."""

    khod_kaar(Agent(simple_args))
    sp = subprocess.run(['python', '../hello_world_project/hello'],
                       check=True, capture_output=True, text=True)
    assert sp.stdout == 'Hello, World!'
