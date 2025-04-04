import pygame

from entities import Player

from engine.controller import controller

from engine.engine import applyGravity

from entities import Player
from entities import Eye

from entities import list_objects

def game(screen, screen_width, screen_height, clock):
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]


    background = pygame.transform.scale(pygame.image.load('assets/bck.png'), (screen_width-10, screen_height-50))

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