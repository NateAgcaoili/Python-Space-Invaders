import pygame
import random
import math
from pygame import mixer

### Initializing pygame ###
pygame.init()

screen = pygame.display.set_mode((800, 600)) #creates screen with size of 800 x 600

pygame.display.set_caption("Space Invaders") #setting title
icon = pygame.image.load('ufo.png') #loading icon image
pygame.display.set_icon(icon) #setting icon image

background = pygame.image.load('background.jpg') #Designed by vectorpouch / Freepik
mixer.music.load('background.wav') 
mixer.music.play(-1) #loops background music

player_score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

def show_score(x, y):
    score = font.render(f"Score: {player_score}", True, (255, 255, 255))
    screen.blit(score, (x, y))

### Game Over ###
over_font = pygame.font.Font('freesansbold.ttf', 64)
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))

### Initializing Player ###
player_img = pygame.image.load('player.png') #loading player icon
player_x = 370 
player_y = 480 
player_x_change = 0
def player(x, y):
    screen.blit(player_img, (x, y)) #draws player

### Initializing Enemy ###
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
enemy_num = 6

for i in range(enemy_num):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(0.4)
    enemy_y_change.append(60)

def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y)) #draws enemy

### Initializing Bullet ###
bullet_img = pygame.image.load('bullet.png') #loading bullet icon
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = -2
bullet_state = "ready"
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10)) #draws bullet

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(((enemy_x - bullet_x) ** 2) + ((enemy_y - bullet_y) ** 2))
    if distance < 27:
        return True
    return False

### Main Game Loop ###
running = True
while running:
    
    screen.fill((0, 0, 0)) #fills screen with black
    screen.blit(background,(0,0))
    # Closes window if X is pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.5
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('shoot.wav')
                    bullet_sound.play() #plays when shooting
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
    # Updating player location
    player_x += player_x_change
    # Setting player boundaries
    if player_x <= 0:
        player_x = 0
    if player_x >= 736:
        player_x = 736
    # Updating enemy locations
    for i in range(enemy_num):
        # Game over
        if enemy_y[i] > 440:
            for j in range(enemy_num):
                enemy_y[j] = 2000 #sends rest of enemies off screen
            game_over_text()
            break
        enemy_x[i] += enemy_x_change[i]
        # Setting enemy boundaries
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 0.4
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -0.4
            enemy_y[i] += enemy_y_change[i]
         # Checking collision
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            hit_sound = mixer.Sound('hit.wav')
            hit_sound.play() #plays when hit
            bullet_y = 480
            bullet_state = "ready"
            player_score += 1
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 150)
        enemy(enemy_x[i], enemy_y[i], i)
    # Updating bullet location
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y += bullet_y_change
   
    player(player_x, player_y) #constantly drawing
    show_score(text_x, text_y)
    pygame.display.update()