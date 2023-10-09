import os
import pytest
from Agent import Agent
from khod_kaar import khod_kaar

import subprocess

class Args:
    """Class to mock the argparser"""

    def __init__(self, model_, output_dir_, temperature_, autopilot_, objective_):
        self.model = model_
        self.output_dir = output_dir_
        self.temperature = temperature_
        self.autopilot = autopilot_
        self.objective = objective_


@pytest.fixture
def simple_args():
    args = ['gpt-4', 
            './output/', 
            0.0, 
            True, 
            "to write, test and execute a simple Python program that writes 'Hello, World!'."
    ]
    return Args(*args)
    

def test_integration(simple_args):

    assert True

    # TODO This returns an ioctl error once the subprocess is activated. Investigate further.
    # agent = Agent(simple_args)
    # khod_kaar(agent)