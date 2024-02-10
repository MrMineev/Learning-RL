import random
from numpy import random as nrandom

class Rental:
    COST_PER_MOVEMENT = 2
    BALANCE = 50

    FIRST_REQUEST = 3
    SECOND_REQUEST = 4
    FIRST_RETURN = 3
    SECOND_RETURN = 2

    def __init__(self, first, second):
        self.first_rental = first
        self.second_rental = second

    def transfer(self, update):
        self.first_rental += update
        self.second_rental -= update
        self.BALANCE -= abs(update) * self.COST_PER_MOVEMENT

    def request_cars(self):
        first = nrandom.poisson(self.FIRST_REQUEST)
        second = nrandom.poisson(self.SECOND_REQUEST)
        self.BALANCE += (first + second) * 10

        self.first_rental -= first
        self.second_rental -= second

    def give_in_cars(self):
        first = nrandom.poisson(self.FIRST_RETURN)
        second = nrandom.poisson(self.SECOND_RETURN)

        self.first_rental += first
        self.second_rental += second


