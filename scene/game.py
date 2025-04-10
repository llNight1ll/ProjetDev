import pygame

from entities import Player

from engine.controller import controller

from engine.engine import applyGravity

from entities import Player
from entities import Eye

from entities import list_objects

def game(screen, screen_width, screen_height, clock, numberOfReadyPlayers):
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]


    background = pygame.transform.scale(pygame.image.load('assets/bck.png'), (screen_width-10, screen_height-50))

    offset_X = 0
    offset_Y = 0

    players = []
    eyes = []
    for i in range(numberOfReadyPlayers):
        players.append(Player.Player())

    for player in players:
        eyes.append(Eye.Eye(player))

    running = True

    while running: 
        
        screen.blit(background, (offset_X,offset_Y))

        for player in players:
            screen.blit(player.image, player.rect)

        for eye in eyes:
            screen.blit(eye.image, eye.rect)

        for obj in list_objects:

            pygame.draw.rect(screen, obj.rgb, obj.object, obj.width)

        for i in range(numberOfReadyPlayers):
            controller(players[i], eyes[i])

        
        for i in range(numberOfReadyPlayers):
            applyGravity(players[i], list_objects)

            if (players[i].frame_index !=  0):
                players[i].play_animation(140,103,4)

        # Mettre à jour l'affichage
        pygame.display.flip()
        clock.tick(60)  # 60 FPS

        #print(players[0].rect.x, players[0].rect.y)