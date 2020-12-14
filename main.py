import pygame

### Initializing pygame ###
pygame.init()

screen = pygame.display.set_mode((800, 600)) #creates screen with size of 800 x 600

pygame.display.set_caption("Space Invaders") #setting title
icon = pygame.image.load('ufo.png') #loading icon image
pygame.display.set_icon(icon) #setting icon image

### Initializing Player ###
player_img = pygame.image.load('player.png') #loading player icon
player_x = 370 #initial player x screen position
player_y = 480 #initial player y screen position
player_x_change = 0
def player(x, y):
    screen.blit(player_img, (x, y)) #draws player

### Main Game Loop ###
running = True
while running:
    
    screen.fill((0, 0, 0)) #fills screen with black
    # Closes window if X is pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.1
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    player_x += player_x_change
    player(player_x, player_y) #constantly drawing
    pygame.display.update()