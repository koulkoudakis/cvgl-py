"""
Author: Sharome Burton
Date: 02/13/2022

"""

import pygame
import os

import cv2
import cvGameDevTools
from cvGameDevTools import capture_frame


pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Face")

# Computer vision
cv = cvGameDevTools.CvTool(WIDTH, HEIGHT)

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# Game parameters
FPS = 60
BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('helvetica', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 60)

SHIP_W, SHIP_H = 30, 25
MON_W, MON_H = 200, 200
MHAND_W, MHAND_H = 200, 160
SHIP_VEL = 10

BULLET_VEL = 10
MAX_BULLETS = 3
BULLET_TRACKING = 5
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

# Yellow Spaceship
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SHIP_W, SHIP_H)),
    90
    )
YELLOW_HIT = pygame.USEREVENT + 1


# Red Spaceship
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP_IMAGE = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SHIP_W, SHIP_H)),
    270
    )
RED_HIT = pygame.USEREVENT + 2

# Monster head
MONSTER_IMAGE = pygame.image.load(os.path.join('Assets', 'monster_head.png'))
MONSTER_IMAGE = pygame.transform.scale(MONSTER_IMAGE, (MON_W, MON_H))
MONSTER_HIT = pygame.USEREVENT + 3

# Monster hand
MONSTER_HAND_IMAGE = pygame.image.load(os.path.join('Assets', 'monster_hand.png'))
MONSTER_HAND_IMAGE_LEFT = pygame.transform.scale(MONSTER_HAND_IMAGE, (MHAND_W, MHAND_H))
MONSTER_HAND_IMAGE_RIGHT = pygame.transform.flip(MONSTER_HAND_IMAGE_LEFT, True, False)
MONSTER_HAND_HIT = pygame.USEREVENT + 3


# Background
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')),
                               (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, yellow_health, red_health, face, hand_bullets, face_health, hand):

    # WIN.fill(WHITE)
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(f"Red HP: {red_health}/10", 1, RED)
    yellow_health_text = HEALTH_FONT.render(f"Yellow HP: {yellow_health}/10", 1, YELLOW)
    face_health_text = HEALTH_FONT.render(f"DIMENSIONAL HORROR HP: {face_health}/100", 1, WHITE)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(face_health_text, (WIDTH // 2 - face_health_text.get_width() // 2, HEIGHT - face_health_text.get_height()))



    WIN.blit(YELLOW_SPACESHIP_IMAGE, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP_IMAGE, (red.x, red.y))
    WIN.blit(MONSTER_IMAGE, (face.x,
                            # WIDTH // 2 - MONSTER_IMAGE.get_width() // 2,
                             face.y))

    if hand.centerx < WIDTH // 2:
        WIN.blit(MONSTER_HAND_IMAGE_LEFT, (hand.x, hand.y))
    else:
        WIN.blit(MONSTER_HAND_IMAGE_RIGHT, (hand.x, hand.y))


    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
        
    for bullet in hand_bullets:
        pygame.draw.rect(WIN, WHITE, bullet)

    pygame.display.update()

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2,
                         HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def handle_bullets(yellow_bullets, red_bullets, yellow, red, face, hand_bullets, hand):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif face.colliderect(bullet):
            pygame.event.post(pygame.event.Event(MONSTER_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)


    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif face.colliderect(bullet):
            pygame.event.post(pygame.event.Event(MONSTER_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

    for bullet in hand_bullets:

        if hand.centerx < WIDTH //2:
            if bullet.y < yellow.centery:
                bullet.y += BULLET_TRACKING
            elif bullet.y > yellow.centery:
                bullet.y -= BULLET_TRACKING
            bullet.x -= BULLET_VEL*2
            if yellow.colliderect(bullet):
                pygame.event.post(pygame.event.Event(YELLOW_HIT))
                hand_bullets.remove(bullet)
            if red.colliderect(bullet):
                pygame.event.post(pygame.event.Event(RED_HIT))
                hand_bullets.remove(bullet)
            elif bullet.x < 0:
                hand_bullets.remove(bullet)

        else:
            if bullet.y < red.centery:
                bullet.y += BULLET_TRACKING
            elif bullet.y > red.centery:
                bullet.y -= BULLET_TRACKING
            bullet.x += BULLET_VEL *2
            if yellow.colliderect(bullet):
                pygame.event.post(pygame.event.Event(YELLOW_HIT))
                hand_bullets.remove(bullet)
            if red.colliderect(bullet):
                pygame.event.post(pygame.event.Event(RED_HIT))
                hand_bullets.remove(bullet)
            elif bullet.x > WIDTH:
                hand_bullets.remove(bullet)


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - SHIP_VEL >= 0:  # LEFT
        yellow.x -= SHIP_VEL
    if keys_pressed[pygame.K_d] and yellow.x + SHIP_VEL + yellow.width <= BORDER.x:  # RIGHT
        yellow.x += SHIP_VEL
    if keys_pressed[pygame.K_w] and yellow.y - SHIP_VEL >= 0:  # UP
        yellow.y -= SHIP_VEL
    if keys_pressed[pygame.K_s] and yellow.y + SHIP_VEL + yellow.height <= HEIGHT:  # DOWN
        yellow.y += SHIP_VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - SHIP_VEL >= BORDER.x + BORDER.width:  # LEFT
        red.x -= SHIP_VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + SHIP_VEL + red.width <= WIDTH:  # RIGHT
        red.x += SHIP_VEL
    if keys_pressed[pygame.K_UP] and red.y - SHIP_VEL >= 0:  # UP
        red.y -= SHIP_VEL
    if keys_pressed[pygame.K_DOWN] and red.y + SHIP_VEL + red.height <= HEIGHT:  # DOWN
        red.y += SHIP_VEL


def main():
    yellow = pygame.Rect(100, 100, SHIP_W, SHIP_H)
    yellow_bullets = []
    yellow_health = 10

    red = pygame.Rect(800, 300, SHIP_W, SHIP_H)
    red_bullets = []
    red_health = 10

    face = pygame.Rect(WIDTH // 2 - MONSTER_IMAGE.get_width() // 2,
                        HEIGHT // 2 - MONSTER_IMAGE.get_height() // 2,
                        MON_W,
                        MON_H
                        )
    hand_bullets = []
    face_health = 100

    hand = pygame.Rect(WIDTH // 2 - MONSTER_IMAGE.get_width() // 2,
                        HEIGHT // 2 - MONSTER_IMAGE.get_height() // 2,
                        MON_W,
                        MON_H
                        )



    clock = pygame.time.Clock()
    run = True
    while run:

        clock.tick(FPS)

        frame, overlayed, matimg, finger_inputs, face_inputs = cv.frame_step(face=True, display_face=True)
        xp, yp, grid_row, grid_col, index_finger, two_fingers = finger_inputs
        xf, yf, wf, hf, xcf, ycf = face_inputs

        ### CV EVENTS

        if xf != None:
            face.centerx = xcf
            face.centery = ycf

        if xp != None:
            if index_finger:
                hand.centerx = xp
                hand.centery = yp

        if two_fingers and len(hand_bullets) < MAX_BULLETS*2:
            bullet = pygame.Rect(
                hand.centerx, hand.centery, 20, 10)
            hand_bullets.append(bullet)
            BULLET_FIRE_SOUND.play()


        ### EVENTS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height // 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == MONSTER_HIT:
                face_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if face_health <= 0:
            winner_text = "Yellow Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        # print(red_bullets, yellow_bullets)

        keys_pressed = pygame.key.get_pressed()

        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red, face, hand_bullets, hand)

        draw_window(red, yellow, red_bullets, yellow_bullets, yellow_health, red_health, face, hand_bullets, face_health, hand)

        frame_img = capture_frame()
        # cv2.imshow('frame cap', frame_img)

        print(f'XP: {xp} YP: {yp}')

        pygameoverlayed = cv2.addWeighted(frame_img, 0.3, overlayed, 0.7, 0)
        cv2.imshow('game overlayed', cv2.resize(pygameoverlayed, (int(WIDTH*0.6), int(HEIGHT*0.6))))

    main()

if __name__ == "__main__":
    main()