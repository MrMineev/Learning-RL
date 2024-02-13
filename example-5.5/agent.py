from setting import Game
import numpy as np
import matplotlib.pyplot as plt

class Agent:
    GAMMA = 1

    def __init__(self, eps=0.01):
        self.eps = eps
        self.target_policy = [0.5, 0.5]
        self.behavoir_policy = [0.5, 0.5]
        self.qtable = [0, 0]
        self.returns = [[], []]
        self.game = Game()

        self.datax = []
        self.datay = []

    def step(self):
        states, actions, rewards = self.game.play_game(self.behavoir_policy)


        g_value = 0

        isr = 1 # Importance-Sampling Ratio
        for i in range(len(actions)):
            isr *= self.target_policy[actions[i]] / 0.5

        for t in reversed(range(len(states))):
            g_value = self.GAMMA * g_value + rewards[t]

            '''
            if g_value == 1:
                print(f"states = {states}")
                print(f"actions = {actions}")
                print(f"rewards = {rewards}")
            '''

            if not ((states[t], actions[t]) in [(a, b) for a, b in zip(states[:t], actions[:t])]):
                self.returns[actions[t]].append(g_value * isr)
                self.qtable[actions[t]] = np.mean(np.array(self.returns[actions[t]]))

                a_star = -1
                a_star_max = -1
                for action in range(2):
                    if self.qtable[action] > a_star_max:
                        a_star_max = self.qtable[action]
                        a_star = action

                for action in range(2):
                    if action == a_star:
                        self.target_policy[action] = 1 - self.eps + self.eps / 2
                    else:
                        self.target_policy[action] = self.eps / 2

    def generate(self):
        M = 0
        while M <= 1e4:
            if M % 1000 == 0:
                print(f"STEP = {M}")
            self.step()
            self.datax.append(M)
            self.datay.append(max(self.qtable[0], self.qtable[1]))
            M += 1

        plt.plot(self.datax, self.datay)
        plt.ylim(0, 2)
        plt.show()



