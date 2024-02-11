from setting import Blackjack
import matplotlib.pyplot as plt
import random
import numpy as np
import seaborn as sns
import time

def get_random_matrix(a, b, c):
    mas = []
    for i in range(a):
        sub = []
        for j in range(b):
            qwe = []
            for k in range(c):
                qwe.append(random.randint(1, 2))
            sub.append(qwe)
        mas.append(sub)
    return mas

def get_const_matrix(a, b, c, d, initial):
    mas = []
    for i in range(a):
        sub = []
        for j in range(b):
            qwe = []
            for k in range(c):
                wer = []
                for h in range(d):
                    wer.append(initial)
                qwe.append(wer)
            sub.append(qwe)
        mas.append(sub)
    return mas

class Agent:
    M = 0
    def __init__(self, plot=False):
        self.policy = np.random.randint(2, size=(2, 22, 12))

        self.returns = np.empty((2, 22, 12, 2), dtype=object)
        for i in range(self.returns.shape[0]):
            for j in range(self.returns.shape[1]):
                for k in range(self.returns.shape[2]):
                    for h in range(self.returns.shape[3]):
                        self.returns[i, j, k, h] = []

        self.qtable = np.random.rand(2, 2, 22, 12)

        self.game = Blackjack()
        self.plot = plot

    def generate_random_state(self):
        if random.randint(0, 1) == 0:
            return [0, random.randint(4, 21), random.randint(2, 11)]
        else:
            return [1, 11 + random.randint(2, 10), random.randint(2, 11)]


    def step(self):
        state_zero = self.generate_random_state()
        action_zero = random.randint(0, 1)
        states, actions, reward = self.game.play_game_from_state(state_zero, action_zero, self.policy)
        # print(states, actions, reward)
        for i in reversed(range(0, len(states))):
            if (not (states[i] in states[:i])) or (not (actions[i] in actions[:i])):
                self.returns[states[i][0], states[i][1], states[i][2], action_zero].append(reward)
                self.qtable[action_zero, states[i][0], states[i][1], states[i][2]] = np.mean(self.returns[states[i][0], states[i][1], states[i][2], action_zero])

                maxi = -100
                policy_new_action = -1
                for sub_action in range(2):
                    value = self.qtable[sub_action, states[i][0], states[i][1], states[i][2]]
                    if value > maxi:
                        maxi = value
                        policy_new_action = sub_action
                self.policy[states[i][0], states[i][1], states[i][2]] = policy_new_action
        # time.sleep(1)

    def calculate(self):
        if self.M % 1000 == 0:
            print(f"M = {self.M}")
        self.M += 1
        self.step()
        self.game.reset()

        if self.M % 1e5 == 0:
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
        sns.heatmap(self.qtable[0, 0, 11:21 + 1, :], annot=True, linewidth=0.5, ax=axes[0, 0], fmt=".1f", cmap="viridis", annot_kws={"size": 4})
        axes[0, 0].invert_yaxis()
        axes[0, 0].set_title(f'No Ace, Keep')
        axes[0, 0].set_xlabel('Player')
        axes[0, 0].set_ylabel('Dealer')
        sns.heatmap(self.qtable[0, 1, 11:21 + 1, :], annot=True, linewidth=0.5, ax=axes[0, 1], fmt=".1f", cmap="viridis", annot_kws={"size": 4})
        axes[0, 1].invert_yaxis()
        axes[0, 1].set_title(f'No Ace, Hit')
        axes[0, 1].set_xlabel('Player')
        axes[0, 1].set_ylabel('Dealer')
        sns.heatmap(self.qtable[1, 0, 11:21 + 1, :], annot=True, linewidth=0.5, ax=axes[1, 0], fmt=".1f", cmap="viridis", annot_kws={"size": 4})
        axes[1, 0].invert_yaxis()
        axes[1, 0].set_title(f'Ace, Keep')
        axes[1, 0].set_xlabel('Player')
        axes[1, 0].set_ylabel('Dealer')
        sns.heatmap(self.qtable[1, 1, 11:21 + 1, :], annot=True, linewidth=0.5, ax=axes[1, 1], fmt=".1f", cmap="viridis", annot_kws={"size": 4})
        axes[1, 1].invert_yaxis()
        axes[1, 1].set_title(f'Ace, Hit')
        axes[1, 1].set_xlabel('Player')
        axes[1, 1].set_ylabel('Dealer')
        plt.tight_layout()
        plt.savefig(f'data/qtable_{self.M}.svg')
        plt.close(fig)

