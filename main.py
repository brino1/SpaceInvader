import pygame
import random
import math
from pygame import mixer



pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('./asset/background.png')

mixer.music.load('./asset/background.wav')
mixer.music.play(-1)

pygame.display.set_caption("Space Invader")
icon = pygame.image.load('./asset/ufo.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('./asset/player.png')
playerX = 370
playerY = 480
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('./asset/enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

shotImg = pygame.image.load('./asset/bullet.png')
shotX = 0
shotY = 480
shotX_change = 0
shotY_change = 7
shot_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score : "+ str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER : " + str(score_value), True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


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
                shot_Sound = mixer.Sound('./asset/laser.wav')
                shot_Sound.play()
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

    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], shotX, shotY)
        if collision:
            explosion_Sound = mixer.Sound('./asset/explosion.wav')
            explosion_Sound.play()
            shotY = 480
            shot_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    if shotY <= 0:
        shotY = 480
        shot_state = "ready"
    if shot_state == "fire":
        fire_shot(shotX, shotY)
        shotY -= shotY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
