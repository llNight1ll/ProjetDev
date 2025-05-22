import pygame
import sys

from entities import Player

from engine.controller import controller

from engine.engine import checkPlayerCollision
from engine.engine import bulletCollision
from engine.engine import checkEndGame

from entities import Player

from scene import getPlayer

from entities.Object import map1

from scene import menu


bullets = pygame.sprite.Group()

def draw_player_ui(screen, players):
    screen_width, screen_height = screen.get_size()

    #Ratios
    ui_height_ratio = 0.95
    ui_margin_bottom_ratio = 0.0
    player_column_ratio = 0.25
    icon_size_ratio = 0.03
    text_size_ratio = 0.03
    life_box_size_ratio = 0.01
    life_box_margin_ratio = 0.01

    #UI position
    ui_y = screen_height - int(screen_height * ui_height_ratio) - int(screen_height * ui_margin_bottom_ratio)

    player_column_width = int(screen_width * player_column_ratio)
    total_width = len(players) * player_column_width
    start_x = (screen_width - total_width) // 2

    #Font
    font_size = int(screen_height * text_size_ratio)
    font = pygame.font.Font(None, font_size)

    for i, player in enumerate(players):
        column_x = start_x + (i * player_column_width)

        #Skin icon
        skin_icon = pygame.image.load(f'assets/player{player.skin_number}.png').convert_alpha()
        scale_factor = icon_size_ratio * screen_width / skin_icon.get_width()
        skin_icon = pygame.transform.scale_by(skin_icon, scale_factor)
        skin_rect = skin_icon.get_rect(center=(column_x + player_column_width // 2, ui_y))
        screen.blit(skin_icon, skin_rect)

        #Player name
        player_text = f"Player {player.PlayerID}"
        text_surface = font.render(player_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(column_x + player_column_width // 2, ui_y + int(screen_height * 0.04)))
        screen.blit(text_surface, text_rect)

        #Player lives
        life_box_size = int(screen_width * life_box_size_ratio)
        life_box_margin = int(screen_width * life_box_margin_ratio)
        total_life_width = 3 * life_box_size + 2 * life_box_margin
        life_start_x = column_x + (player_column_width - total_life_width) // 2
        life_y = ui_y + int(screen_height * 0.08)

        for life in range(3):
            life_x = life_start_x + life * (life_box_size + life_box_margin)
            color = (255, 0, 0) if life < player.health else (50, 50, 50)
            pygame.draw.rect(screen, color, (life_x, life_y, life_box_size, life_box_size), border_radius=5)


def game(screen, clock, joysticks, control_mode):
    pygame.joystick.init()
    pygame.font.init()
    base_width, base_height = screen.get_size()
    global bullets

    # font size for player text
    player_font = pygame.font.Font(None, 36)  


    players = []

    #Create the 2 keyboard players
    if control_mode == getPlayer.ControlMode.KEYBOARD:
        players.append(Player.Player(1))
        players.append(Player.Player(2))
    else:
        for js in joysticks:
            players.append(Player.Player(joysticks[js].get_instance_id()))
    
    for player in players:
        print(f"Joueur créé avec l'ID: {player.PlayerID}")


    running = True

    while running: 
                

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:

                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

                scale_x = event.size[0] / base_width
                scale_y = event.size[1] / base_height

                base_width, base_height = event.size[0], event.size[1]



                for player in players :
                    player.resize(scale_x,scale_y)

                map1.resize(scale_x, scale_y, event.size[0], event.size[1])





        map1.draw(screen)
        
        bullets.update()

        for bullet in bullets:  
            bulletCollision(bullet, players)
            
        bullets.draw(screen)

        # Gestion des contrôles pour tous les joueurs
        controller(players, control_mode, bullets,events)

        for player in players:
            if not player.isDead:
                player.update()

        for player in players:
            if not player.isDead:
                screen.blit(player.image, player.rect)
                player.pistol.draw(screen)
                # player text above player
                player_text = f"Player {player.PlayerID}"
                text_surface = player_font.render(player_text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(player.rect.centerx, player.rect.top - 20))
                screen.blit(text_surface, text_rect)



        for player in players:
            if not player.isDead:
                if (player.frame_index != 0):
                    player.play_animation(140, 103, 4)

        checkPlayerCollision(players)

        # check if there is only one player alive
        if checkEndGame(players):
            running = False

        # Dessiner l'UI des joueurs
        draw_player_ui(screen, players)

        #print(clock.get_fps())
        pygame.display.flip()
        clock.tick(60)  # 60 FPS

        #print(players[0].rect.x, players[0].rect.y)
    
    # find winner
    winner = None
    for player in players:
        if not player.isDead:
            winner = player
            break
    
    # draw end screen
    draw_end_screen(screen, winner, clock)

def draw_end_screen(screen, winner, clock):
    screen_width, screen_height = screen.get_size()
    
    # font
    title_font = pygame.font.Font(None, 72)
    text_font = pygame.font.Font(None, 36)
    
    button_width = 200
    button_height = 50
    button_x = (screen_width - button_width) // 2
    button_y = screen_height - 100
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    running = False
                    menu.menu()
        
        # background
        screen.fill((0, 0, 0))
        
        # title
        title_text = "Fin de partie"
        title_surface = title_font.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(screen_width // 2, 100))
        screen.blit(title_surface, title_rect)
        
        if winner:
            # winner image
            winner_image = pygame.image.load(f'assets/player{winner.skin_number}.png').convert_alpha()
            scale_factor = 0.2 * screen_width / winner_image.get_width()
            winner_image = pygame.transform.scale_by(winner_image, scale_factor)
            winner_rect = winner_image.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
            screen.blit(winner_image, winner_rect)
            
            # winner text
            winner_text = f"Le joueur {winner.PlayerID} a gagné !"
            text_surface = text_font.render(winner_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
            screen.blit(text_surface, text_rect)
        
        # back to menu button
        pygame.draw.rect(screen, (100, 100, 100), button_rect, border_radius=10)
        button_text = "Retour au menu"
        button_surface = text_font.render(button_text, True, (255, 255, 255))
        button_text_rect = button_surface.get_rect(center=button_rect.center)
        screen.blit(button_surface, button_text_rect)
        
        pygame.display.flip()
        clock.tick(60)