import os
import numpy as np
import math
import random

class Racetrack:
    def __init__(self, epsilon=0.05):
        self.racetrack = []
        self.epsilon = epsilon
        self.load_track()
        print("race_track = \n")
        print(self.racetrack)
        self.dimention_x = len(self.racetrack)
        self.dimention_y = len(self.racetrack[0])

        self.game_starts = []
        self.game_ends = []
        for x in range(self.dimention_x):
            for y in range(self.dimention_y):
                if self.racetrack[x][y] == 2:
                    self.game_starts.append((x, y))
                elif self.racetrack[x][y] == 3:
                    self.game_ends.append((x, y))

    def load_track(self):
        self.racetrack = []
        with open("racetrack.txt", "r") as file:
            text = file.read().split()
            for line in text:
                sub = []
                for symbol in line:
                    sub.append(int(symbol))
                self.racetrack.append(sub)
        self.racetrack = np.array(self.racetrack).transpose()

    def move(self, pos_x, pos_y, vel_x, vel_y):
        if pos_x + vel_x < 0 or pos_x + vel_x >= self.dimention_x:
            return False
        elif pos_y + vel_y < 0 or pos_y + vel_y >= self.dimention_y:
            return False
        elif self.racetrack[pos_x + vel_x][pos_y + vel_y] == 0:
            return False

        return True

    def play_game(self, policy_x, policy_y):
        vel_x, vel_y = random.choice(self.game_starts)
        pos_x, pos_y = 0, 0
        states, actions, rewards = [], [], []
        time = 0
        while time <= 1000:
            time += 1

            states.append([pos_x, pos_y])

            change_x = np.random.choice([-1, 0, 1], p=policy_x[pos_x][pos_y])
            change_y = np.random.choice([-1, 0, 1], p=policy_y[pos_x][pos_y])

            actions.append([change_x + 1, change_y + 1])
            rewards.append(-1)

            if np.random.choice([0, 1], p=[0.9, 0.1]) == 0:
                vel_x = min(max(vel_x + change_x, -5), 5)
                vel_y = min(max(vel_y + change_y, -5), 5)

            cond = self.move(pos_x, pos_y, vel_x, vel_y)

            if not cond:
                pos_x, pos_y = random.choice(self.game_starts)
                vel_x, vel_y = 0, 0
                continue

            pos_x += vel_x
            pos_y += vel_y

            if pos_x < 0 or pos_x >= self.dimention_x or pos_y < 0 or pos_y >= self.dimention_y:
                vel_x, vel_y, pos_x, pos_y = 0, 0, 0, 0
            
            if (pos_x, pos_y) in self.game_ends:
                break


        return states, actions, rewards
