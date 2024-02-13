from numpy import random as nrandom
import numpy as np
import random

class Game:
    def __init__(self):
        pass

    def play_game(self, policy):
        states = []
        actions = []
        rewards = []

        is_terminal = False
        while not is_terminal:
            states.append(0)
            action = nrandom.choice([0, 1], p=policy)
            actions.append(action)
            if action == 0:
                rewards.append(0)
                is_terminal = True
            else:
                option = nrandom.choice([0, 1], p=[0.1, 0.9])
                if option == 0:
                    rewards.append(1)
                    is_terminal = True
                else:
                    rewards.append(0)

        return states, actions, rewards







