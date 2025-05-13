import pygame

from entities import Player

from engine.controller import controller

from engine.engine import applyGravity
from engine.engine import checkPlayerCollision

from entities import Player
from entities import Eye

from entities import list_objects
from scene import getPlayer

def game(screen, screen_width, screen_height, clock, joysticks, control_mode):
    pygame.joystick.init()

    background = pygame.transform.scale(pygame.image.load('assets/bck.png').convert(), (screen_width-10, screen_height-50))

    offset_X = 0
    offset_Y = 0

    players = []
    eyes = []

    #Create the 2 keyboard players
    if control_mode == getPlayer.ControlMode.KEYBOARD:
        players.append(Player.Player(-1))
        players.append(Player.Player(-2))
    else:
        for js in joysticks:
            players.append(Player.Player(joysticks[js].get_instance_id()))
    
    for player in players:
        print(f"Joueur créé avec l'ID: {player.PlayerID}")

    for player in players:
        eyes.append(Eye.Eye(player))

    running = True

    while running: 
        screen.blit(background, (offset_X, offset_Y))

        for player in players:
            screen.blit(player.image, player.rect)

        for eye in eyes:
            screen.blit(eye.image, eye.rect)

        for obj in list_objects:
            pygame.draw.rect(screen, obj.rgb, obj.object, obj.width)

        for i, player in enumerate(players):
            controller(players, eyes[i], control_mode)

        for player in players:
            applyGravity(player, list_objects)

            if (player.frame_index != 0):
                player.play_animation(140, 103, 4)

        checkPlayerCollision(players)

        #print(clock.get_fps())
        pygame.display.flip()
        clock.tick(60)  # 60 FPS

        #print(players[0].rect.x, players[0].rect.y)