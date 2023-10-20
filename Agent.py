"""
File: Agent.py
Author: Danyal Mohaddes
Description: This file contains the Agent class.
"""

import os
from colorama import Fore
from colorama import Style

import argparse
from Roles import Roles
from Memory import Memory
from Interface import Interface
from System import System
from OpeningPrompt import OpeningPrompt

class Agent():
    """Entity that combines memory (through a Memory class instance), logic engine (through an Interface class instance) and capacity for action (through a System class instance).
    
    Attributes:
        memory: A Memory singleton instance
        model: an Interface singleton instance
        system: a System singleton instance
        objective: the user's initially-stated stated objective
    """


    def __init__(self, args: argparse.Namespace) -> None:
        """Initialization for the Agent class.
        
        Args:
            args: Command-line arguments parsed by argparse
        """

        # Create Memory singleton instance as attribute
        self.memory = Memory(args.model, args.output_dir)
        
        # Create Model singleton instance as attribute
        self.model = Interface(args.temperature, args.model)

        # Create System singleton instance as attribute
        self.system = System(args.autopilot)

        # Create OpeningPrompt singleton instance
        op = OpeningPrompt(args.output_dir, args.objective)

        # Keep track of objective
        self.objective = op.objective

        # Loop over opening prompts and add to memory
        for p in op.prompts:
            self.memory.memorize(p['content'], p['role'])


    def satisfied(self) -> bool:
        """Convenience method to check if execution loop should be stopped.
        
        If human and LLM are both satisfied, or if human asks for gracious halt to program, the final element of the agent's memory will be the stop message.
        
        returns:
            boolean. True means stop execution.
        """

        if "**STOP**" in self.memory.memories[-1].get('content', None):
            return True
        else:
            return False


    def status_check(self) -> None:
        """Print the latest additions to the agent's memory, as well as the current token usage count, to the console."""

        last_memory_ = self.memory.memories[-1]
        role_ = last_memory_['role']
        
        color_dict = {Roles.user.name: Fore.GREEN,
                      Roles.assistant.name: Fore.RED,
                      Roles.system.name: Fore.WHITE}

        print("")
        if role_ == Roles.assistant.name:
            term_size = os.get_terminal_size()
            print('=' * term_size.columns)
        print(f"Tokens used: {self.memory.total_token_count}")
        print(f"{color_dict[role_]}{role_}{Style.RESET_ALL}: {last_memory_['content']}")