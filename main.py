import pygame 
import math
import random

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((900, 600))

# BackGround
background = pygame.image.load('space.jpg')

# Caption and icon
#OBS: Procurar um icon no FlatIcon
pygame.display.set_caption("Game in Space")
icon = pygame.image.load('galaxy.png')
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('arcade-game.png')
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6 

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ghost.png'))
    enemyX.append(random.randint(0, 835))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5)
    enemyY_change.append(25)

#bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bulletSmall.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score: "+ str(score_value), True, (255,255, 255))
    screen.blit(score, (x, y))

def player(x,y):
    screen.blit(playerImg, (x, y))

def enemy(x,y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 5, y + 3))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY , 2)))
    if distance < 27: 
        return True
    else:
        return False

#game loop
running = True
while running:

    #RGB - Red, Green, Blue
    screen.fill((0, 0, 0))
    
    #Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keastroke is pressed check wheter its right or left
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:  
                # Get the current x Cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # Checking for boundaries of spaceship so it doesn't go out dounds
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 836:
        playerX = 836

    #enemy movement
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 836:
            enemyX_change[i] = -1.5
            enemyY[i] += enemyY_change[i]

        #Collision 
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision: 
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 900)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement 
    if bulletY <= 0: 
        bulletY = 480
        bullet_state = "reday"

    if bullet_state is "fire":
        fire_bullet(playerX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()