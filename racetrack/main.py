from agent import Agent
import os

player = Agent(mu=0.25)
player.train(M=1000)
player.save(f"{os.getcwd()}/policies.txt")


