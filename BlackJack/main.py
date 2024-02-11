from agent import Agent
from setting import Blackjack

agent = Agent(plot=True)

while agent.M < int(1e6):
    agent.calculate()

