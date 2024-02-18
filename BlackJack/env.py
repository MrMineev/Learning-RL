import random
from numpy import random as nrandom
import numpy as np

class Blackjack:
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]

    def __init__(self):
        self.player_hand_sum = 0
        self.player_has_ace = False
        self.dealer_hand_sum = 0
        self.dealer_has_ace = False

    def reset(self):
        self.player_hand_sum = 0
        self.player_has_ace = False
        self.dealer_hand_sum = 0
        self.dealer_has_ace = False

    def get_state(self):
        if self.player_has_ace == True:
            return [1, self.player_hand_sum, self.dealer_hand_sum]
        else:
            return [0, self.player_hand_sum, self.dealer_hand_sum]

    def play_game(self, policy):
        self.initialize_game()

        states = []
        actions = []

        while self.player_hand_sum <= 21:
            states.append(self.get_state())
            s = self.get_state()
            action = np.random.choice([0, 1], p=policy[s[0], s[1], s[2]])
            actions.append(action)
            if action == 1: # Hit
                self.player_hit()
            else:
                break

        self.dealer_policy()

        if self.player_hand_sum > self.dealer_hand_sum and self.player_hand_sum <= 21:
            reward = 1
        elif self.dealer_hand_sum > 21 and self.player_hand_sum <= 21:
            reward = 1
        elif self.dealer_hand_sum == self.player_hand_sum and self.player_hand_sum <= 21:
            reward = 0
        else:
            reward = -1

        return states, actions, reward
    
    def initialize_game(self):
        self.reset()
        self.player_hit()
        self.player_hit()
        self.dealer_hit()

    def generate_random_card(self):
        return random.choice(self.cards)

    def dealer_policy(self):
        if self.dealer_hand_sum > 21:
            if self.dealer_has_ace:
                self.dealer_hand_sum -= 10
                self.dealer_has_ace = False
            else:
                return
        if self.dealer_hand_sum >= 17:
            return
        else:
            self.dealer_hit()
        self.dealer_policy()

    def dealer_hit(self):
        card = self.generate_random_card()
        if card == 11:
            if self.dealer_hand_sum <= 10:
                self.dealer_hand_sum += 11
                self.dealer_has_ace = True
            else:
                self.dealer_hand_sum += 1
        else:
            self.dealer_hand_sum += card

        if self.dealer_hand_sum > 21 and self.dealer_has_ace == True:
            self.dealer_hand_sum -= 10
            self.dealer_has_ace = False

    def player_hit(self):
        card = self.generate_random_card()
        if card == 11:
            if self.player_hand_sum <= 10:
                self.player_hand_sum += 11
                self.player_has_ace = True
            else:
                self.player_hand_sum += 1
        else:
            self.player_hand_sum += card

        if self.player_hand_sum > 21 and self.player_has_ace == True:
            self.player_hand_sum -= 10
            self.player_has_ace = False
