from setting import Rental
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from poisson import Poisson


def get_matrix(n, m, initial):
    mas = []
    for i in range(n):
        mas.append([initial] * m)
    return mas


class Agent:
    GAMMA = 0.9
    GAME_SIZE = 20
    EPS = 5
    MAX_MOVEMENT = 5

    EPS_CHANCE = 0.01

    iteration = 0

    def __init__(self, first, second):
        self.rental = Rental(first, second)

        self.policy = get_matrix(self.GAME_SIZE + 1, self.GAME_SIZE + 1, 0)
        self.qtable = get_matrix(self.GAME_SIZE + 1, self.GAME_SIZE + 1, 0)

        self.first_buy = Poisson(self.rental.FIRST_REQUEST, self.GAME_SIZE, epsilon=self.EPS_CHANCE)
        self.second_buy = Poisson(self.rental.SECOND_REQUEST, self.GAME_SIZE, epsilon=self.EPS_CHANCE)
        self.first_return = Poisson(self.rental.FIRST_RETURN, self.GAME_SIZE, epsilon=self.EPS_CHANCE)
        self.second_return = Poisson(self.rental.SECOND_RETURN, self.GAME_SIZE, epsilon=self.EPS_CHANCE)

    def expected_reward(self, first, second, action):
        sum = -abs(action) * self.rental.COST_PER_MOVEMENT
        new_position_a = max(min(first + action, self.GAME_SIZE), 0)
        new_position_b = max(min(second - action, self.GAME_SIZE), 0)
        for bA in range(self.first_buy.left, self.first_buy.right + 1):  # buy
            for bB in range(self.second_buy.left, self.second_buy.right + 1):  # buy
                for rA in range(self.first_return.left, self.first_return.right + 1):  # return
                    for rB in range(self.second_return.left, self.second_return.right + 1):  # return
                        valid_buy_a = min(bA, new_position_a)
                        valid_buy_b = min(bB, new_position_b)

                        new_first = max(min(new_position_a - valid_buy_a + rA, self.GAME_SIZE), 0)
                        new_second = max(min(new_position_b - valid_buy_b + rB, self.GAME_SIZE), 0)

                        reward = (valid_buy_a + valid_buy_b) * 10

                        prob = self.first_buy.get_value(bA)
                        prob *= self.second_buy.get_value(bB)
                        prob *= self.first_return.get_value(rA)
                        prob *= self.second_return.get_value(rB)

                        sum += prob * (reward + self.GAMMA * self.qtable[new_first][new_second])
        return sum

    def policy_evaluation(self):
        delta = 0
        for i in range(self.GAME_SIZE + 1):
            for j in range(self.GAME_SIZE + 1):
                v = self.qtable[i][j]
                self.qtable[i][j] = self.expected_reward(i, j, self.policy[i][j])
                delta = max(delta, abs(v - self.qtable[i][j]))
        print(f"DELTA = {delta}")
        if delta < self.EPS:
            return
        self.policy_evaluation()

    def policy_improvement(self):
        old_action = 0
        is_stable = True

        for i in range(self.GAME_SIZE + 1):
            if i % 2 == 0:
                print(i)
            for j in range(self.GAME_SIZE + 1):
                old_action = self.policy[i][j]

                maxi = -1000
                index = 0
                for action in range(-min(self.MAX_MOVEMENT, i), min(self.MAX_MOVEMENT, j) + 1):
                    sum = self.expected_reward(i, j, action)

                    if maxi < sum:
                        maxi = sum
                        index = action
                self.policy[i][j] = index

                if old_action != self.policy[i][j]:
                    is_stable = False

        return is_stable

    def save_policy(self):
        ax = sns.heatmap(self.policy, linewidth=0.5)
        ax.invert_yaxis()
        plt.savefig('data/policy' + str(self.iteration) + '.svg')
        plt.close()

    def save_value(self):
        ax = sns.heatmap(self.qtable, linewidth=0.5)
        ax.invert_yaxis()
        plt.savefig('data/value' + str(self.iteration) + '.svg')
        plt.close()

    def info(self):
        self.save_value()
        self.save_policy()
        self.iteration += 1
