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

    def play_game_from_state(self, state, action, policy):
        self.reset()
        self.player_has_ace = state[0]
        self.player_hand_sum = state[1]
        self.dealer_hand_sum = state[2]

        return self.play_game(action, policy)

    def play_game(self, action, policy):
        states = []
        actions = []
        reward = 0

        state = self.get_state()
        states.append(state)
        actions.append(action)

        if action != 0: # player hit
            self.player_hit()

            while self.player_hand_sum <= 21:
                state = self.get_state()
                states.append(state)
                actions.append(policy[state[0]][state[1]][state[2]])

                if actions[-1] == 1:
                    self.player_hit()
                else:
                    break

        self.dealer_policy()

        # print(f"result = {self.player_hand_sum} {self.dealer_hand_sum}")

        if self.player_hand_sum > self.dealer_hand_sum and self.player_hand_sum <= 21:
            reward = 1
        elif self.dealer_hand_sum > 21 and self.player_hand_sum <= 21:
            reward = 1
        elif self.dealer_hand_sum == self.player_hand_sum and self.player_hand_sum <= 21:
            reward = 0
        else:
            reward = -1

        return states, actions, reward

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
            card = self.generate_random_card()
            if card == 11:
                if self.dealer_hand_sum <= 10:
                    self.dealer_hand_sum += 11
                    self.dealer_has_ace = True
                else:
                    self.dealer_hand_sum += 1
            else:
                self.dealer_hand_sum += card
        self.dealer_policy()

    def player_hit(self):
        card = self.generate_random_card()
        if card == 11:
            if self.player_hand_sum <= 10:
                self.player_hand_sum += 11
                self.player_has_ace = True
            else:
                self.player_hand_sum += 1
        self.player_hand_sum += card

        if self.player_hand_sum > 21 and self.player_has_ace == True:
            self.player_hand_sum -= 10
            self.player_has_ace = False
