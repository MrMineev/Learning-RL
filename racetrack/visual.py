import os
import re
import numpy as np
import math
import pygame
import time
import random

def move(racetrack, pos_x, pos_y, vel_x, vel_y):
    if pos_x + vel_x < 0 or pos_x + vel_x >= dimention_x:
        return False
    elif pos_y + vel_y < 0 or pos_y + vel_y >= dimention_y:
        return False
    elif racetrack[pos_x + vel_x][pos_y + vel_y] == 0:
        return False

    return True

square_size = 30
background_color = (255, 255, 255)
empty_square_color = (120, 118, 117)
back_color = (0, 0, 0)
start_color = (167, 250, 173)
end_color = (250, 174, 167)
player_color = (111, 125, 232)

racetrack = []
with open("racetrack.txt", "r") as file:
    text = file.read().split()
    for i in range(len(text)):
        line = text[i]
        sub = []
        for symbol in line:
            sub.append(int(symbol))
        racetrack.append(sub)
racetrack = np.array(racetrack).transpose()

print(racetrack)
dimention_x = len(racetrack)
dimention_y = len(racetrack[0])

target_x = []
target_y = []
with open("policies.txt", "r") as file:
    text = file.read()
    a = False
    for line in text.split('\n'):
        if len(line.split()) == 0:
            a = True
            continue

        if not a:
            mas = re.split(r'\s+', line)
            mas = [word for word in mas if word]
            target_x.append([int(mas[i]) for i in range(len(mas))])
        else:
            mas = re.split(r'\s+', line)
            mas = [word for word in mas if word]
            target_y.append([int(mas[i]) for i in range(len(mas))])

target_x = np.array(target_x)
target_y = np.array(target_y)

print(f"shape = {target_x.shape}")
print(f"dim = {dimention_x}, {dimention_y}")

policy_x = np.full((dimention_x, dimention_y, 3), 0)
policy_y = np.full((dimention_x, dimention_y, 3), 0)
for x in range(dimention_x):
    for y in range(dimention_y):
        policy_x[x, y, int(target_x[x][y])] = 1
        policy_y[x, y, int(target_y[x][y])] = 1

game_starts = []
game_ends = []
for x in range(dimention_x):
    for y in range(dimention_y):
        if racetrack[x][y] == 2:
            game_starts.append((x, y))
        elif racetrack[x][y] == 3:
            game_ends.append((x, y))

pygame.init()
size = (square_size * dimention_x, square_size * dimention_y)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('RaceTrack') 
screen.fill(background_color) 
pygame.display.flip()

vel_x, vel_y = 0, 0
pos_x, pos_y = random.choice(game_starts)
while True:
    screen.fill(background_color)

    change_x = np.random.choice([-1, 0, 1], p=policy_x[pos_x][pos_y])
    change_y = np.random.choice([-1, 0, 1], p=policy_y[pos_x][pos_y])

    if np.random.choice([0, 1], p=[0.9, 0.1]) == 0:
        vel_x = min(max(vel_x + change_x, -5), 5)
        vel_y = min(max(vel_y + change_y, -5), 5)

    cond = move(racetrack, pos_x, pos_y, vel_x, vel_y)
    if not cond:
        pos_x, pos_y = random.choice(game_starts)
        vel_x, vel_y = 0, 0
        continue
    pos_x += vel_x
    pos_y += vel_y

    for x in range(dimention_x):
        for y in range(dimention_y):
            if racetrack[x][y] == 0:
                pygame.draw.rect(screen, empty_square_color, pygame.Rect(x*square_size, y*square_size, square_size, square_size))
            elif racetrack[x][y] == 2:
                pygame.draw.rect(screen, start_color, pygame.Rect(x*square_size, y*square_size, square_size, square_size))
            elif racetrack[x][y] == 3:
                pygame.draw.rect(screen, end_color, pygame.Rect(x*square_size, y*square_size, square_size, square_size))
    pygame.draw.rect(screen, player_color, pygame.Rect(pos_x*square_size, pos_y*square_size, square_size, square_size))

    pygame.display.flip()

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False


    time.sleep(0.1)


