from agent import Agent
import os

player = Agent(mu=0.3)
player.train(M=3000)
player.save(f"{os.getcwd()}/policies.txt")


