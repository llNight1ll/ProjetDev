import pygame
import sys
import json
from scene import menu
from scene.screen import *

def leaderboard(screen):
    # colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (100, 100, 100)
    
    # font
    title_font = pygame.font.Font(None, 72)
    text_font = pygame.font.Font(None, 36)
    
    # back button
    back_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
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
                    player_rect = player_image.get_rect(center=(WIDTH // 2 - 100, y_offset))
                    screen.blit(player_image, player_rect)
                except:
                    pass
                
                # score text
                score_text = f"Player {player_id}: {score} win{'s' if score > 1 else ''}"
                text = text_font.render(score_text, True, WHITE)
                text_rect = text.get_rect(center=(WIDTH // 2 + 100, y_offset))
                screen.blit(text, text_rect)
                
                y_offset += 80
                
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