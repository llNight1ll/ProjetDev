import os

import pygame

from entities import Player

from engine.controller import controller

from engine.engine import applyGravity

from entities import Player
from entities import Eye

from entities import list_objects




pygame.init()   

#Called before init
os.environ['SDL_VIDEO_CENTERED'] = '1' 

#Called before set_mode
info = pygame.display.Info()

screen_widht, screen_height = info.current_w, info.current_h 

WIDTH, HEIGHT = 1080, 720
WHITE = (255, 255, 255)
RED = (255, 0, 0)



# create game's window

pygame.display.set_caption('Mygame')
screen = pygame.display.set_mode((screen_widht-10, screen_height-50), pygame.RESIZABLE)
clock = pygame.time.Clock() 

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]


background = pygame.transform.scale(pygame.image.load('assets/bck.png'), (screen_widht-10, screen_height-50))

offset_X = 0
offset_Y = 0

player = Player.Player()
eye = Eye.Eye(player)

running = True

while running: 
    
    screen.blit(background, (offset_X,offset_Y))

    screen.blit(player.image, player.rect)

    screen.blit(eye.image, eye.rect)

    for obj in list_objects:

        pygame.draw.rect(screen, obj.rgb, obj.object, obj.width)

    controller(player, eye)

    
    applyGravity(player, list_objects)

    if (player.frame_index !=  0):
        player.play_animation(140,103,4)



    # Mettre à jour l'affichage
    pygame.display.flip()
    clock.tick(60)  # 60 FPS