import pygame
from sys import exit
from random import randint

pygame.init()
pygame.font.init()
pygame.display.set_caption('Runner')
screen = pygame.display.set_mode((800,400))
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = 0
start_time = 0
game_message = 'Press Space to Run'

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surface = test_font.render(f'{current_time // 100}', False, (64,64,64))
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rect)

    return current_time//100

def obstacle_movement(obstacle_rect_list):
    if obstacle_rect_list:
        for obstacle_rect in obstacle_rect_list:
            obstacle_rect.x -= 5

            screen.blit(snail_surface, obstacle_rect)
        
        return obstacle_rect_list
    
    else: return []

# Background Surfaces
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/Ground.png').convert()

# Obstacles ---------------------------
obstacle_rect_list = []

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom =(800,300))

fly_surface = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_rect = fly_surface.get_rect(midbottom = (800,150))

# Player -------------------------------
player_surface = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80,300))

player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

# Timer -------------------------------
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 900)

player_grav = 0

# Full game logic
while True:
    #Listening to Input Events
    for event in pygame.event.get():

        # Quit event on pressing quit button
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        # Keyboard input to restart game
        if game_active == 0 and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_active = 1
            start_time = pygame.time.get_ticks()

        if game_active == 1:
            # Mouse Jumping
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.y >= 200:
                    print('Mouse/Player Collision')
                    player_grav = -20
            
            # Space Jumping
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.y >= 200:
                    print('jump')
                    player_grav = -20
        
        # Timer
        if event.type == obstacle_timer and game_active == 1:
            print('test')
            obstacle_rect_list.append(
                snail_surface.get_rect(midbottom =(randint(900,1100),300))
                )


    # Game Active
    if game_active == 1:
        
        # Background and Score --------------------------------
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        display_score()

# Player Code -----------------------------------------
        screen.blit(player_surface, player_rect)

        # Player Gravity
        player_rect.y += player_grav
        
        if player_rect.y >= 200: # Defines the floor and resets gravity
            player_grav = 0

        if player_rect.y < 200: # If player is above the floor, add gravity
            player_grav += 1

# Obstacle Movement ------------------------------------
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Snail logic ----------------------------------------
        # snail_rect.left -= 4
        # if snail_rect.right <= 0:
        #     snail_rect.left = 800
        # screen.blit(snail_surface, snail_rect)

        # if player_rect.colliderect(snail_rect) == 1:
        #     print('Snail/Player Collision')
        #     game_message = f'{display_score()}'
        #     game_active = 0


        # Fly logic ------------------------------------------
        # fly_rect.left -= 6
        # if fly_rect.left <= -200:
        #     fly_rect.left = 1000
        # screen.blit(fly_surface, fly_rect)

        # if player_rect.colliderect(fly_rect) == 1:
        #     print('Fly/Player Collision')
        #     game_message = f'{display_score()}'
        #     game_active = 0
    
    # Start/GameOver Screen
    else:
        screen.fill((94,129,162))

        title_surf = test_font.render('Pixel Jumper',False, (111,196,169))
        title_rect = title_surf.get_rect(center = (400,50))
        screen.blit(title_surf,title_rect)

        screen.blit(player_stand,player_stand_rect)

        instruct_surf = test_font.render(game_message, False, (111,196,169))
        instruct_rect = instruct_surf.get_rect(center = (400,350))
        screen.blit(instruct_surf, instruct_rect)

    pygame.display.update()
    clock.tick(60)
