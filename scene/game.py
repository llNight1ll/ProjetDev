import pygame

from entities import Player

from engine.controller import controller

from engine.engine import applyGravity

from entities import Player
from entities import Eye

from entities import list_objects

def game(screen, screen_width, screen_height, clock, numberOfReadyPlayers, joysticks):
    pygame.joystick.init()


    background = pygame.transform.scale(pygame.image.load('assets/bck.png'), (screen_width-10, screen_height-50))

    offset_X = 0
    offset_Y = 0

    players = []
    eyes = []

    #Create keyboard players
    #players.append(Player.Player(-1))
    #players.append(Player.Player(-2))


    #Create controller players
    for js in joysticks:
        players.append(Player.Player(joysticks[js].get_instance_id()))
    
    for player in players :
        print(player.PlayerID)

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


        for player,eye in zip(players, eyes):
            controller(players, eye)

        for player in players:
            applyGravity(player, list_objects)

            if (player.frame_index !=  0):
                player.play_animation(140,103,4)

        # Mettre à jour l'affichage
        pygame.display.flip()
        clock.tick(60)  # 60 FPS

        #print(players[0].rect.x, players[0].rect.y)