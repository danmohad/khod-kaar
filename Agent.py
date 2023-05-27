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
        if self.memory.memories[-1].get('content', None) == "Satisfied.":
            return True
        else:
            return False