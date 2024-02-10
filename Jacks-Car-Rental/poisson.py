from numpy import random as nrandom
import numpy as np

def poisson_distribution(lam, k):
    return np.exp(-lam) * (lam ** k) / np.math.factorial(k)

class Poisson:
    def __init__(self, lam, maximum, epsilon=0.01):
        self.eps = epsilon
        self.lam = lam
        self.game_size = maximum
        self.probabilities = []

        self.left = 0
        self.right = self.game_size

        self.generate()

    def generate(self):
        for i in range(self.game_size + 1):
            self.probabilities.append(poisson_distribution(self.lam, i))

        for i in range(self.game_size + 1):
            if self.probabilities[i] > self.eps:
                self.left = i
                break
        for i in reversed(range(self.game_size + 1)):
            if self.probabilities[i] > self.eps:
                self.right = i
                break

    def get_value(self, x):
        return self.probabilities[x]


