import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('./asset/background.png')

pygame.display.set_caption("Space Invader")
icon = pygame.image.load('./asset/ufo.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('./asset/player.png')
playerX = 370
playerY = 480
playerX_change = 0

enemyImg = pygame.image.load('./asset/enemy.png')
enemyX = random.randint(0, 735)
enemyY = random.randint(50, 150)
enemyX_change = 4
enemyY_change = 10

shotImg = pygame.image.load('./asset/bullet.png')
shotX = 0
shotY = 480
shotX_change = 0
shotY_change = 7
shot_state = "ready"

score = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire_shot(x, y):
    global shot_state
    shot_state = "fire"
    screen.blit(shotImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if shot_state == "ready":
                    shotX = playerX
                    fire_shot(playerX, shotY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    enemyX += enemyX_change
    if enemyX <= 0:
        enemyX_change = 4
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -4
        enemyY += enemyY_change

    if shotY <= 0:
        shotY = 480
        shot_state = "ready"
    if shot_state == "fire":
        fire_shot(shotX, shotY)
        shotY -= shotY_change

    collision = isCollision(enemyX, enemyY, shotX, shotY)
    if collision:
        shotY = 480
        shot_state = "ready"
        score += 1
        print(score)
        enemyX = random.randint(0, 735)
        enemyY = random.randint(50, 150)

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()
