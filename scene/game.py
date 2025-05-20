import pygame

from entities import Player

from engine.controller import controller

from engine.engine import checkPlayerCollision

from entities import Player
from entities import Eye

from entities import list_objects
from scene import getPlayer

projectiles = pygame.sprite.Group()

def draw_player_ui(screen, players):    
    ui_y = 900 - 150 - 40
    
    total_width = len(players) * 400
    start_x = (1500 - total_width) // 2
    
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

def game(screen, clock, joysticks, control_mode):
    pygame.joystick.init()
    pygame.font.init()
    base_width, base_height = screen.get_size()
    global projectiles

    # font size for player text
    player_font = pygame.font.Font(None, 36)  

    background = pygame.image.load('assets/bck2.png').convert()

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
                

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:

                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                background = pygame.transform.scale(background, event.size)

                scale_x = event.size[0] / base_width
                scale_y = event.size[1] / base_height

                base_width, base_height = event.size[0], event.size[1]

                print("scale :", scale_x, scale_y)
                for player in players :
                    player.resize(scale_x,scale_y)




        screen.blit(background, (offset_X, offset_Y))

        # Gestion des contrôles pour tous les joueurs
        controller(players, control_mode, projectiles,events)

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

        # Mise à jour des projectiles
        projectiles.update()

        # Dessin
        projectiles.draw(screen)

        # Dessiner l'UI des joueurs
        draw_player_ui(screen, players)

        #print(clock.get_fps())
        pygame.display.flip()
        clock.tick(60)  # 60 FPS

        #print(players[0].rect.x, players[0].rect.y)