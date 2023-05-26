from Roles import Roles
from Agent import Agent

agent = Agent()

while not agent.satisfied():
    agent.memory.memorize(agent.model.send_prompt(agent.memory.memories), Roles.assistant.name)
    agent.memory.memorize(agent.system.execute(agent.memory.memories[-1]['content']), Roles.user.name)