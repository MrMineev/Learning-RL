from env import Blackjack
import numpy as np

policy = np.full((2, 22, 12, 2), 0.3)
for i in range(2):
    for j in range(22):
        for k in range(12):
            policy[i, j, k, 1] = 0.7

game = Blackjack()
states, actions, reward = game.play_game(policy)

print(f"states = {states}")
print(f"actions = {actions}")
print(f"reward = {reward}")



