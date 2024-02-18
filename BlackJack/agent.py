from env import Blackjack
import matplotlib.pyplot as plt
import random
import numpy as np
import seaborn as sns
import time
from progress.bar import ChargingBar

class Agent:
    M = 0

    def __init__(self, mu=0.5):
        self.mu = mu
        self.policy = np.full((2, 22, 12), 1)
        self.qtable = np.full((2, 2, 22, 12), 0.0)
        self.c_table = np.full((2, 2, 22, 12), 0.0)

        self.game = Blackjack()

    def step(self):
        behavior = np.full((2, 22, 12, 2), self.mu)
        for i in range(2):
            for j in range(22):
                for k in range(12):
                    behavior[i, j, k, self.policy[i, j, k]] = 1 - self.mu

        states, actions, reward = self.game.play_game(behavior)
        # print(f"states = {states}")
        # print(f"actions = {actions}")
        # print(f"reward = {reward}")
        weight = 1.0
        for i in reversed(range(0, len(states))):
            self.c_table[actions[i], states[i][0], states[i][1], states[i][2]] += weight
            
            qval = self.qtable[actions[i], states[i][0], states[i][1], states[i][2]]
            cval = self.c_table[actions[i], states[i][0], states[i][1], states[i][2]]
            self.qtable[actions[i], states[i][0], states[i][1], states[i][2]] = qval + weight / cval * (reward - qval)

            maxi = -1e6
            best_action = -1
            for action in range(2):
                if self.qtable[action, states[i][0], states[i][1], states[i][2]] > maxi:
                    maxi = self.qtable[action, states[i][0], states[i][1], states[i][2]]
                    best_action = action
            self.policy[states[i][0], states[i][1], states[i][2]] = best_action

            if actions[i] != best_action:
                break

            weight *= 1 / behavior[states[i][0], states[i][1], states[i][2], actions[i]]

    def train(self, goal=1000):
        print(f"--------------------------- TRAINING -------------------------")
        print()
        bar = ChargingBar('Progress', max=goal)
        t = 0
        while t < goal:
            self.step()
            t += 1
            bar.next()
        bar.finish()

        print()
        print(f"--------------------------- TRAINING -------------------------")
        print()
        print()

        self.save_policy()
        self.save_qtable()


    def save_policy(self):
        fig, axes = plt.subplots(1, 2)
        sns.heatmap(self.policy[0], linewidth=0.5, ax=axes[0])
        axes[0].invert_yaxis()
        sns.heatmap(self.policy[1], linewidth=0.5, ax=axes[1])
        axes[1].invert_yaxis()
        plt.savefig(f'data/policy_{self.M}.svg')
        plt.close(fig)


    def save_qtable(self):
        fig, axes = plt.subplots(2, 2)

        # Plot the first heatmap on the first subplot
        sns.heatmap(self.qtable[0, 0, :, :], annot=True, linewidth=0.5, ax=axes[0, 0], fmt=".1f", cmap="viridis", annot_kws={"size": 4})
        axes[0, 0].invert_yaxis()
        axes[0, 0].set_title(f'No Ace, Keep')
        axes[0, 0].set_xlabel('Dealer')
        axes[0, 0].set_ylabel('Player')
        sns.heatmap(self.qtable[1, 0, :, :], annot=True, linewidth=0.5, ax=axes[1, 0], fmt=".1f", cmap="viridis", annot_kws={"size": 4})
        axes[1, 0].invert_yaxis()
        axes[1, 0].set_title(f'No Ace, Hit')
        axes[1, 0].set_xlabel('Dealer')
        axes[1, 0].set_ylabel('Player')
        sns.heatmap(self.qtable[0, 1, :, :], annot=True, linewidth=0.5, ax=axes[0, 1], fmt=".1f", cmap="viridis", annot_kws={"size": 4})
        axes[0, 1].invert_yaxis()
        axes[0, 1].set_title(f'Ace, Keep')
        axes[0, 1].set_xlabel('Dealer')
        axes[0, 1].set_ylabel('Player')
        sns.heatmap(self.qtable[1, 1, :, :], annot=True, linewidth=0.5, ax=axes[1, 1], fmt=".1f", cmap="viridis", annot_kws={"size": 4})
        axes[1, 1].invert_yaxis()
        axes[1, 1].set_title(f'Ace, Hit')
        axes[1, 1].set_xlabel('Dealer')
        axes[1, 1].set_ylabel('Player')
        plt.tight_layout()
        plt.savefig(f'data/qtable_{self.M}.svg')
        plt.close(fig)

