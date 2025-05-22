import pygame
import sys
import json
from scene import menu
from scene.screen import *

def leaderboard(screen, joystick):
    # colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (100, 100, 100)
    
    # Initialisation responsive
    WIDTH, HEIGHT = screen.get_size()
    ui = resize_elements((WIDTH, HEIGHT))
    title_font = ui["title_font"]
    text_font = ui["text_font"]
    back_button = ui["back_button"]
    scale = ui["scale"]
    scale_x = ui["scale_x"]
    scale_y = ui["scale_y"]


    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    running = False

            elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                ui = resize_elements(event.size)
                title_font = ui["title_font"]
                text_font = ui["text_font"]
                back_button = ui["back_button"]
                scale = ui["scale"]
                scale_x = ui["scale_x"]
                scale_y = ui["scale_y"]

                WIDTH, HEIGHT = event.size
                                    
            elif event.type == pygame.JOYDEVICEADDED:
                joystick = pygame.joystick.Joystick(event.device_index)
                joystick.init()
                joysticks[joystick.get_instance_id()] = joystick
                print(f"Manette connectée : {joystick.get_name()}")

            elif event.type == pygame.JOYDEVICEREMOVED:
                if event.instance_id in joysticks:
                    del joysticks[event.instance_id]
                    print("Manette déconnectée")
                
            elif event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                running = False

        # background
        screen.fill((50, 50, 50))
        
        # title
        title = title_font.render("Leaderboard", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title, title_rect)
        
        try:
            # load json
            with open('data/data.json', 'r') as f:
                data = json.load(f)
            
            # sort scores
            sorted_scores = sorted(data["scores"].items(), key=lambda x: x[1], reverse=True)
            
            # display scores
            y_offset = 200
            for player_id, score in sorted_scores:
                # player image
                try:
                    player_image = pygame.image.load(f'assets/player{player_id}.png').convert_alpha()
                    scale_factor = 0.04 * WIDTH / player_image.get_width()
                    player_image = pygame.transform.scale_by(player_image, scale_factor)
                    player_rect = player_image.get_rect(center=(WIDTH // 2 - 100 * scale_x, y_offset * scale_y))
                    screen.blit(player_image, player_rect)
                except:
                    pass
                
                # score text
                score_text = f"Player {player_id}: {score} win{'s' if score > 1 else ''}"
                text = text_font.render(score_text, True, WHITE)
                text_rect = text.get_rect(center=(WIDTH // 2 + 100 * scale_x, y_offset * scale_y))
                screen.blit(text, text_rect)
                
                y_offset += 80 *scale_y
                
        except Exception as e:
            error_text = text_font.render("Error while loading scores", True, WHITE)
            error_rect = error_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(error_text, error_rect)
        
        # back button
        pygame.draw.rect(screen, GRAY, back_button, border_radius=10)
        back_text = text_font.render("Back", True, WHITE)
        back_text_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_text_rect)
        
        pygame.display.flip()
        clock.tick(60)

BASE_WIDTH = 1280
BASE_HEIGHT = 720

def resize_elements(screen_size):
    width, height = screen_size
    scale_x = width / BASE_WIDTH
    scale_y = height / BASE_HEIGHT
    scale = min(scale_x, scale_y)

    title_font = pygame.font.Font(None, int(72 * scale))
    text_font = pygame.font.Font(None, int(36 * scale))

    # Bouton "Back" responsive
    back_button = pygame.Rect(width // 2 - int(100 * scale), height - int(100 * scale), int(200 * scale), int(50 * scale))

    return {
        "scale": scale,
        "scale_x": scale_x,
        "scale_y": scale_y,
        "title_font": title_font,
        "text_font": text_font,
        "back_button": back_button,
        "width": width,
        "height": height
    }
