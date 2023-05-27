import argparse

from Roles import Roles
from Agent import Agent

def khodkaar(objective_ = None):
    agent = Agent(objective_)

    while not agent.satisfied():
        agent.memory.memorize(agent.model.send_prompt(agent.memory.memories), Roles.assistant.name)
        agent.memory.memorize(agent.system.execute(agent.memory.memories[-1]['content']), Roles.user.name)

if __name__ == "__main__":
    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Add optional argument for command-line objective, for ease of testing
    parser.add_argument("-o", "--objective", help = "Input objective (to ...)")
    
    # Read arguments from command line
    args = parser.parse_args()

    # Run program
    khodkaar(args.objective)