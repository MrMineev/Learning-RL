from setting import Rental
from agent import Agent

agent = Agent(20, 20)

while True:
    agent.policy_evaluation()
    a = agent.policy_improvement()
    agent.info()
    if a == True:
        break
print("END!!!")
agent.info()
