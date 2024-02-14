from environment import Racetrack
import numpy as np
import copy
import random
import matplotlib.pyplot as plt
from progress.bar import ChargingBar


class Agent:
    GAMMA = 1

    def __init__(self, mu=0.1):
        self.racetrack = Racetrack()
        self.mu = mu

        self.learning_data_y = []

        # actions for x - {0, 1, ..., 5}
        self.qtable_x = np.zeros((self.racetrack.dimention_x, self.racetrack.dimention_y, 3))
        self.weight_sum_x = np.zeros((self.racetrack.dimention_x, self.racetrack.dimention_y, 3))
        self.target_x = np.zeros((self.racetrack.dimention_x, self.racetrack.dimention_y))

        self.qtable_y = np.zeros((self.racetrack.dimention_x, self.racetrack.dimention_y, 3))
        self.weight_sum_y = np.zeros((self.racetrack.dimention_x, self.racetrack.dimention_y, 3))
        self.target_y = np.zeros((self.racetrack.dimention_x, self.racetrack.dimention_y))

    def step(self):
        # change the behavior to a slightly changed target policy
        behavior_x = np.full((self.racetrack.dimention_x, self.racetrack.dimention_y, 3), 1/5)
        behavior_y = np.full((self.racetrack.dimention_x, self.racetrack.dimention_y, 3), 1/5)
        for x in range(self.racetrack.dimention_x):
            for y in range(self.racetrack.dimention_y):
                behavior_x[x, y, int(self.target_x[x, y])] = 3/5
                behavior_y[x, y, int(self.target_y[x, y])] = 3/5

        states, actions, rewards = self.racetrack.play_game(behavior_x, behavior_y)

        self.learning_data_y.append(len(rewards))

        # print(f"states = {states}")
        # print(f"actions = {actions}")
        # print(f"rewards = {rewards}")

        g_value = 0
        weight_x, weight_y = 1, 1
        for t in reversed(range(len(states))):
            s_x = states[t][0]
            s_y = states[t][1]
            action_x = actions[t][0]
            action_y = actions[t][1]

            g_value = self.GAMMA * g_value + rewards[t]

            # X Policy

            self.weight_sum_x[s_x][s_y][action_x] += weight_x
            weight_sum = self.weight_sum_x[s_x][s_y][action_x]
            qtable_x_val = self.qtable_x[s_x][s_y][action_x]

            self.qtable_x[s_x][s_y][action_x] = qtable_x_val + weight_x / weight_sum * (g_value - qtable_x_val)

            alpha_action_x = -1
            alpha_reward = -10000
            for sub_action in range(3):
                if self.qtable_x[s_x][s_y][sub_action] > alpha_reward:
                    alpha_reward = self.qtable_x[s_x][s_y][sub_action]
                    alpha_action_x = sub_action
            self.target_x[s_x][s_y] = alpha_action_x

            # Y Policy

            self.weight_sum_y[s_x][s_y][action_y] += weight_y
            weight_sum = self.weight_sum_y[s_x][s_y][action_y]
            qtable_y_val = self.qtable_y[s_x][s_y][action_y]

            self.qtable_y[s_x][s_y][action_y] = qtable_y_val + weight_y / weight_sum * (g_value - qtable_y_val)

            alpha_action_y = -1
            alpha_reward = -10000
            for sub_action in range(3):
                if self.qtable_y[s_x][s_y][sub_action] > alpha_reward:
                    alpha_reward = self.qtable_y[s_x][s_y][sub_action]
                    alpha_action_y = sub_action
            self.target_y[s_x][s_y] = alpha_action_y

            if action_x != alpha_action_x and action_y != alpha_action_y:
                break

            weight_x = weight_x * 1 / behavior_x[s_x, s_y, action_x]
            weight_y = weight_y * 1 / behavior_y[s_x, s_y, action_y]

    def train(self, M=int(1e3), LOG=int(1e2)):
        print(f"GAME = [{self.racetrack.dimention_x}, {self.racetrack.dimention_y}]")

        print(f"--------------------------- TRAINING -------------------------")
        print()
        bar = ChargingBar('Progress', max=M)
        t = 0
        while t < M:
            self.step()
            t += 1
            bar.next()
        bar.finish()

        print()
        print(f"--------------------------- TRAINING -------------------------")
        print()
        print()


        self.save_policies()


    def save_policies(self):
        behavior_x = np.full((self.racetrack.dimention_x, self.racetrack.dimention_y, 3), 0)
        behavior_y = np.full((self.racetrack.dimention_x, self.racetrack.dimention_y, 3), 0)
        for x in range(self.racetrack.dimention_x):
            for y in range(self.racetrack.dimention_y):
                behavior_x[x, y, int(self.target_x[x, y])] = 1
                behavior_y[x, y, int(self.target_y[x, y])] = 1
        rewards = []
        for i in range(30):
            _, _, r = self.racetrack.play_game(behavior_x, behavior_y)
            rewards.append(len(r))
        print(f"length = {rewards}")

        fig, axes = plt.subplots(2, 2)
        axes[0, 0].imshow(self.target_x, cmap='gray')
        axes[0, 0].set_title('Target X')
        axes[1, 0].imshow(self.target_y, cmap='gray')
        axes[1, 0].set_title('Target Y')

        qtable_x_show = np.zeros((self.racetrack.dimention_x, self.racetrack.dimention_y))
        qtable_y_show = np.zeros((self.racetrack.dimention_x, self.racetrack.dimention_y))
        for x in range(self.racetrack.dimention_x):
            for y in range(self.racetrack.dimention_y):
                qtable_x_show[x, y] = self.qtable_x[x, y, int(self.target_x[x, y])]
                qtable_y_show[x, y] = self.qtable_y[x, y, int(self.target_y[x, y])]


        axes[0, 1].imshow(qtable_x_show, cmap='gray')
        axes[0, 1].set_title('Q-Table X')
        axes[1, 1].imshow(qtable_y_show, cmap='gray')
        axes[1, 1].set_title('Q-Table Y')

        plt.tight_layout()
        plt.show()

        plt.plot([i for i in range(len(self.learning_data_y))], self.learning_data_y)
        plt.show()

    def save(self, path):
        with open(path, 'w') as file:
            s = ""
            for x in range(self.racetrack.dimention_x):
                for y in range(self.racetrack.dimention_y):
                    s += str(int(self.target_x[x][y])) + " "
                s += '\n'
            s += '\n'
            for x in range(self.racetrack.dimention_x):
                for y in range(self.racetrack.dimention_y):
                    s += str(int(self.target_y[x][y])) + " "
                s += '\n'
            file.write(s)











