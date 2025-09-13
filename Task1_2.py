# Q:  why the speed of the enemy and player are too slow when we are inserting an backgrond image
# ans : for every iteration our background image is reloading but that background image is heavy that is our 
# while become slow and that will make our player and enemy too slow

import pygame
import random
import math
from pygame import mixer

pygame.init()

# score 
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

# background sound
mixer.music.load('sound.wav')
mixer.music.play(-1)

txtX = 10
txtY = 10


def show_score():
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (txtX, txtY))


game_over = pygame.font.Font('freesansbold.ttf', 32)


def game_O_txt():
    over_text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (300, 270))


# W,H
# ON PYGAME DISPLAY
# TOP LEFT (X = 0 ) , TOP RIGHT 800
# TOP (Y = 0)
# BOTTOM = 600

# used to insert image on game window
screen = pygame.display.set_mode((800, 600))
icon = pygame.image.load('My_game.png')
pygame.display.set_icon(icon)

background = pygame.image.load('background_img.png')

# player creation.
playerImg = pygame.image.load('rocket.png')
playerX = 450
playerY = 480
p_speedchange = 0

enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
size = 9

for i in range(size):
    # enemy creation.
    enemyimg.append(pygame.image.load('meteor-shower.png'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(30, 480))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# bullet creation.
# ready state :- we can't see the bullet on the screen
# fire :- the bullet is currently is moving.
bulletimg = pygame.image.load('bullet_img.png')
bulletX = playerX + 9
bulletY = playerY - 3
bulletX_change = 0
bulletY_change = 0.99
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 9, y + 10))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if (distance < 20):
        return True
    else:
        return False


# function to create palyer at every instance

def player(x, y):
    # 'blit' just means draw
    screen.blit(playerImg, (playerX, playerY))


def enemy(x, y, i):
    # 'blit' just means draw
    screen.blit(enemyimg[i], (enemyX[i], enemyY[i]))


# caption for game window
pygame.display.set_caption('My Game')

running = True

# all the events are there in the pygame.event
# giving the input through our keyboard is also an event
# closeing of our game window or any window are also an event
#  whenever we press some key on our keyboard it is an keystrok event.
while running:
    # r , g , b
    screen.fill((0, 0, 20))

    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if any key strok is pressed wether it is right or left
        # conditionn for that , if event is any quit type for that  we used a for loop.
        # here keydown is identifing that these is any key is pressed or not.

        if event.type == pygame.KEYDOWN:
            # it check is key pressed was left ot not
            if event.key == pygame.K_LEFT:
                p_speedchange = -0.4
            if event.key == pygame.K_RIGHT:
                p_speedchange = 0.4
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('Laser (3).wav')
                bullet_sound.play()
                if bullet_state is "ready":
                    # x cordinate of spaceship.
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.type == pygame.K_LEFT or event.type == pygame.K_RIGHT:
                p_speedchange = 0

    for i in range(size):
        if enemyY[i] > 470:
            for j in range(size):
                enemyY[j] = 2000
            game_O_txt()
            break

        if enemyX[i] <= 0:
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = 0.3
        if enemyX[i] >= 780:
            enemyY[i] += enemyY_change[i]
            enemyX_change[i] = -0.3
        enemyX[i] += enemyX_change[i]
        col = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if col:
            explo_sound = mixer.Sound('explosion.wav')
            explo_sound.play()
            bullet_state = "ready"
            bulletY = 480
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(30, 480)
        enemy(enemyX[i], enemyY[i], i)

    # player boundary condition.

    playerX += p_speedchange
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736

    # enemy boundary condition

    # bullet movement:
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score()
    pygame.display.update()


