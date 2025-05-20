import pygame

from entities import Player

from engine.controller import controller

from engine.engine import checkPlayerCollision

from entities import Player
from entities import Eye

from entities import list_objects
from scene import getPlayer

def draw_player_ui(screen, players):    
    ui_y = 1080 - 150 - 40
    
    total_width = len(players) * 400
    start_x = (1920 - total_width) // 2
    
    font = pygame.font.Font(None, 48)

    for i, player in enumerate(players):
        # column position
        column_x = start_x + (i * 400)
        
        # add skin icon
        skin_icon = pygame.transform.scale_by(pygame.image.load(f'assets/player{player.skin_number}.png').convert_alpha(), 0.05)
        skin_rect = skin_icon.get_rect(center=(column_x + 400//2, ui_y))
        screen.blit(skin_icon, skin_rect)
        
        # player name
        player_text = f"Player {player.PlayerID}"
        text_surface = font.render(player_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(column_x + 400//2, ui_y + 40))
        screen.blit(text_surface, text_rect)
        
        # player lifes
        for life in range(3): 
            life_x = column_x + (400 - (3 * (30 + 10)))//2 + (life * (30 + 10))
            life_y = ui_y + 80 
            
            # player life color depending on the life
            color = (255, 0, 0) if life < player.health else (50, 50, 50)
            
            # player life box
            pygame.draw.rect(screen, color, (life_x, life_y, 30, 30), border_radius=5)

def game(screen, screen_width, screen_height, clock, joysticks, control_mode):
    pygame.joystick.init()
    pygame.font.init()

    # font size for player text
    player_font = pygame.font.Font(None, 36)  

    background = pygame.transform.scale(pygame.image.load('assets/bck.png').convert(), (screen_width-10, screen_height-50))

    offset_X = 0
    offset_Y = 0

    players = []
    eyes = []

    #Create the 2 keyboard players
    if control_mode == getPlayer.ControlMode.KEYBOARD:
        players.append(Player.Player(1))
        players.append(Player.Player(2))
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

        # Gestion des contrôles pour tous les joueurs
        controller(players, control_mode)

        for player in players:
            if not player.isDead:
                player.update()

        for player in players:
            if not player.isDead:
                screen.blit(player.image, player.rect)
                # player text above player
                player_text = f"Player {player.PlayerID}"
                text_surface = player_font.render(player_text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(player.rect.centerx, player.rect.top - 20))
                screen.blit(text_surface, text_rect)

        for obj in list_objects:
            pygame.draw.rect(screen, obj.rgb, obj.object, obj.width)

        for player in players:
            if not player.isDead:
                if (player.frame_index != 0):
                    player.play_animation(140, 103, 4)

        checkPlayerCollision(players)

        # Dessiner l'UI des joueurs
        draw_player_ui(screen, players)

        #print(clock.get_fps())
        pygame.display.flip()
        clock.tick(60)  # 60 FPS

        #print(players[0].rect.x, players[0].rect.y)