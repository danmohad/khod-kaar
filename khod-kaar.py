import argparse

from Roles import Roles
from Agent import Agent

def khodkaar() -> None:
    """Top-level function to allow integration tests in CI.
    
        Arguments:
            none
            
        Returns:
            none"""

    agent = Agent(parse_args())

    while not agent.satisfied():
        agent.memory.memorize(agent.model.send_prompt(agent.memory.memories), Roles.assistant.name)
        agent.status_check()
        agent.memory.memorize(agent.system.execute(agent.memory.memories[-1]['content']), Roles.user.name)
        agent.status_check()
        agent.memory.short_to_long_term()

def parse_args() -> argparse.Namespace:
    """Wrapper function for argparse to perform command-line argument parsing.
        
        Arguments:
            none
            
        Returns:
            object containing parsed command-line arguments"""
    
    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Add optional arguments for ease of testing
    parser.add_argument("-o", "--objective", help = "Input objective (starting with the word 'to ...')", type=str)
    parser.add_argument("-t", "--temperature", help = "Input LLM prompting temperature [0,1] (default: 1.0)", type=float, default=1.0)
    parser.add_argument("-m", "--model", help = "Input LLM model (default: gpt-4)", type=str, default="gpt-4")
    parser.add_argument("-d", "--output_dir", help = "Directory on disk to save outputs (default: ./output/)", type=str, default="./output/")
    parser.add_argument("-a", "--autopilot", help = "DANGEROUS: accept all commands until program self-terminates", action=argparse.BooleanOptionalAction)
    
    # Read and return arguments from command line
    return parser.parse_args()


if __name__ == "__main__":
    """Clause to allow running the program as an executable."""

    khodkaar()