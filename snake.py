"""
Author: Sharome Burton
Date: 02/12/2022

"""

import pygame
from pygame.locals import *
import random
import cv2
import time

import cvGameDevTools

from cvGameDevTools import capture_frame

cv = cvGameDevTools.CvTool(600, 600, mat_size=(32, 32))

pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake')

# define font
font = pygame.font.SysFont(None, 40)

# setup a rectangle for "Play Again" Option
again_rect = Rect(screen_width // 2 - 80, screen_height // 2, 160, 50)

# define snake variables
snake_pos = [[int(screen_width / 2), int(screen_height / 2)]]
snake_pos.append([300, 310])
snake_pos.append([300, 320])
snake_pos.append([300, 330])
direction = 1  # 1 is up, 2 is right, 3 is down, 4 is left

# define game variables
cell_size = 20
update_snake = 0
food = [0, 0]


pieces = [food]
obstacles = []
obs_limit = 10
no_obs_dist = 60


new_food = True
new_piece = [0, 0]
game_over = False
clicked = False
score = 0

# define colors
bg = (255, 200, 150)
body_inner = (50, 175, 25)
body_outer = (100, 100, 200)
food_col = (200, 50, 50)
blue = (0, 0, 255)
red = (255, 0, 0)


def capture_frame():
    screen = pygame.display.get_surface()
    capture = pygame.surfarray.pixels3d(screen)
    capture = capture.transpose([1, 0, 2])
    capture_bgr = cv2.cvtColor(capture, cv2.COLOR_RGB2BGR)
    return capture_bgr

def draw_screen():
    screen.fill(bg)


def draw_score():
    score_txt = 'Score: ' + str(score)
    score_img = font.render(score_txt, True, blue)
    screen.blit(score_img, (0, 0))


def check_game_over(game_over):
    # first check is to see if the snake has eaten itself by checking if the head has clashed with the rest of the body
    head_count = 0
    for x in snake_pos:
        if snake_pos[0] == x and head_count > 0:
            game_over = True
        head_count += 1

    # second check is to see if the snake has gone out of bounds
    if snake_pos[0][0] < 0 or snake_pos[0][0] > screen_width or snake_pos[0][1] < 0 or snake_pos[0][1] > screen_height:
        game_over = True

    # check if obstacle has been hit
    # for obs in obstacles:
    #     if snake_pos[0] == food:
    #         game_over = True
    #         game_over = check_game_over(game_over)

    return game_over


def draw_game_over(pieces=pieces, obstacles=obstacles):
    over_text = "Game Over!"
    over_img = font.render(over_text, True, blue)
    pygame.draw.rect(screen, red, (screen_width // 2 - 80, screen_height // 2 - 60, 160, 50))
    screen.blit(over_img, (screen_width // 2 - 80, screen_height // 2 - 50))

    again_text = 'Play Again?'
    again_img = font.render(again_text, True, blue)
    pygame.draw.rect(screen, red, again_rect)
    screen.blit(again_img, (screen_width // 2 - 80, screen_height // 2 + 10))

    pieces = [[cell_size * random.randint(0, (screen_width / cell_size) - 1),
               cell_size * random.randint(0, (screen_height / cell_size) - 1)]]
    obstacles = []

    return pieces, obstacles


run = True
while run:

    frame, overlayed, matimg, finger_inputs = cv.frame_step()
    xp, yp, grid_row, grid_col, index_finger, two_fingers = finger_inputs

    draw_screen()
    draw_score()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 3:
                direction = 1
            if event.key == pygame.K_RIGHT and direction != 4:
                direction = 2
            if event.key == pygame.K_DOWN and direction != 1:
                direction = 3
            if event.key == pygame.K_LEFT and direction != 2:
                direction = 4

    # create food

    if new_food == True:
        if len(pieces) < 2:
            new_food = False
            food[0] = cell_size * random.randint(0, (screen_width / cell_size) - 1)
            food[1] = cell_size * random.randint(0, (screen_height / cell_size) - 1)

    # player placed food
    if index_finger:
        if grid_row != None:
            p_food = [0, 0]
            p_food[1] = cell_size * (grid_col - 1)
            p_food[0] = cell_size * (grid_row - 1)
            pieces.append(p_food)
    pieces_unique = []
    [pieces_unique.append(xy) for xy in pieces if xy not in pieces_unique]
    pieces = pieces_unique



    # draw food
    for food in pieces_unique:
        # print(food[0], food[1])
        try:
            pygame.draw.rect(screen, food_col, (food[0], food[1], cell_size, cell_size))
        except IndexError:
            # print("IndexError")
            pass

    # player placed obstacles
    if two_fingers:
        if grid_row != None:
            if abs(snake_pos[0][0] - (grid_col-1)*cell_size) > no_obs_dist and abs(snake_pos[0][1] - (grid_row-1)*cell_size) > no_obs_dist:
                p_obs = [0, 0]
                p_obs[1] = cell_size * (grid_col - 1)
                p_obs[0] = cell_size * (grid_row - 1)
                obstacles.append(p_obs)

    obstacles_unique = []
    [obstacles_unique.append(xy) for xy in obstacles if xy not in obstacles_unique]
    obstacles = obstacles_unique

    while len(obstacles) > obs_limit:
        obstacles.pop(0)

    for obs in obstacles_unique:
        # print(obs[0], obs[1])
        try:
            pygame.draw.rect(screen, blue, (obs[0], obs[1], cell_size, cell_size))
        except IndexError:
            # print("IndexError")
            pass

    # check if obstacle has been hit
    for obs in obstacles:
        if snake_pos[0] == obs:
            game_over = True
            game_over = check_game_over(game_over)


    # check if food has been eaten
    for food in pieces:
        if snake_pos[0] == food:
            # new_food = True
            food.pop()
            # create a new piece at the last point of the snake's tail
            new_piece = list(snake_pos[-1])
            # add an extra piece to the snake
            if direction == 1:
                new_piece[1] += cell_size
            # heading down
            if direction == 3:
                new_piece[1] -= cell_size
            # heading right
            if direction == 2:
                new_piece[0] -= cell_size
            # heading left
            if direction == 4:
                new_piece[0] += cell_size

            # attach new piece to the end of the snake
            snake_pos.append(new_piece)

            # increase score
            score += 1

    if not game_over:
        # print(f"game_over: {game_over}")
        # update snake
        if update_snake > 1:
            update_snake = 0
            # first shift the positions of each snake piece back.
            snake_pos = snake_pos[-1:] + snake_pos[:-1]
            # now update the position of the head based on direction
            # heading up
            if direction == 1:
                snake_pos[0][0] = snake_pos[1][0]
                snake_pos[0][1] = snake_pos[1][1] - cell_size
            # heading down
            if direction == 3:
                snake_pos[0][0] = snake_pos[1][0]
                snake_pos[0][1] = snake_pos[1][1] + cell_size
            # heading right
            if direction == 2:
                snake_pos[0][1] = snake_pos[1][1]
                snake_pos[0][0] = snake_pos[1][0] + cell_size
            # heading left
            if direction == 4:
                snake_pos[0][1] = snake_pos[1][1]
                snake_pos[0][0] = snake_pos[1][0] - cell_size
            game_over = check_game_over(game_over)
            # print("MOVEMENT")

    if game_over:
        pieces, obstacles = draw_game_over(pieces, obstacles)
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            clicked = False
            # reset variables
            game_over = False
            update_snake = 0
            food = [0, 0]
            new_food = True
            new_piece = [0, 0]
            # define snake variables
            snake_pos = [[int(screen_width / 2), int(screen_height / 2)]]
            snake_pos.append([300, 310])
            snake_pos.append([300, 320])
            snake_pos.append([300, 330])
            direction = 1  # 1 is up, 2 is right, 3 is down, 4 is left
            score = 0

    head = 1
    for x in snake_pos:
        # print(x)

        if head == 0:
            pygame.draw.rect(screen, body_outer, (x[0], x[1], cell_size, cell_size))
            pygame.draw.rect(screen, body_inner, (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))
        if head == 1:
            pygame.draw.rect(screen, body_outer, (x[0], x[1], cell_size, cell_size))
            pygame.draw.rect(screen, (255, 0, 0), (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))
            head = 0

    pygame.display.update()

    update_snake += 1


    frame_img = capture_frame()
    cv2.imshow('frame cap', frame_img)

    print(f'XP: {xp} YP: {yp}')

    pygameoverlayed = cv2.addWeighted(frame_img, 0.3, overlayed, 0.7, 0)
    cv2.imshow('game overlayed', cv2.resize(pygameoverlayed, (screen_width, screen_width)))
    # print(time.time())


pygame.quit()
