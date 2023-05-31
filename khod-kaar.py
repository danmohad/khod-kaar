import argparse

from Roles import Roles
from Agent import Agent

def khodkaar(args_):
    agent = Agent(args_)

    while not agent.satisfied():
        agent.memory.memorize(agent.model.send_prompt(agent.memory.memories), Roles.assistant.name)
        agent.status_check()
        agent.memory.memorize(agent.system.execute(agent.memory.memories[-1]['content']), Roles.user.name)
        agent.status_check()
        agent.memory.short_to_long_term()

if __name__ == "__main__":
    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Add optional arguments for ease of testing
    parser.add_argument("-o", "--objective", help = "Input objective (to ...)", type=str)
    parser.add_argument("-t", "--temperature", help = "Input LLM prompting temperature [0,1] (default: 1.0)", type=float)
    parser.add_argument("-m", "--model", help = "Input LLM model (default: gpt-4)", type=str)
    parser.add_argument("-d", "--long_term_memory", help = "Location on disk to save long-term memory (default: .)", type=str)
    parser.add_argument("-a", "--autopilot", help = "DANGEROUS: accept all commands until program self-terminates", action=argparse.BooleanOptionalAction)
    
    # Read arguments from command line
    args = parser.parse_args()

    # Run program
    khodkaar(args)