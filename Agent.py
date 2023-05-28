import os
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

from Roles import Roles
from Memory import Memory
from Interface import Interface
from System import System
from OpeningPrompt import OpeningPrompt

class Agent():
    def __init__(self, args) -> None:
        # Create Memory singleton instance as attribute
        self.memory = Memory()
        
        # Create Model singleton instance as attribute
        self.model = Interface(args.temperature)

        # Create System singleton instance as attribute
        self.system = System()

        # Create OpeningPrompt singleton instance
        op = OpeningPrompt(args.objective)

        # Loop over opening prompts and add to memory
        for p in op.prompts:
            self.memory.memorize(p['content'], p['role'])

    def satisfied(self):
        # TODO this needs to be incorporated in the OpeningPrompt
        if self.memory.memories[-1].get('content', None) == "Satisfied.":
            return True
        else:
            return False

    def status_check(self):
        last_memory_ = self.memory.memories[-1]
        role_ = last_memory_['role']
        
        color_dict = {Roles.user.name: Fore.GREEN,
                      Roles.assistant.name: Fore.RED,
                      Roles.system.name: Fore.WHITE}

        print("")
        if role_ == Roles.assistant.name:
            term_size = os.get_terminal_size()
            print('=' * term_size.columns)
        print(f"Tokens used: {self.model.tokens_used}") # TODO change this back to being from Memory, so that it updates when the user has output too
        print(f"{color_dict[role_]}{role_}{Style.RESET_ALL}: {last_memory_['content']}")