import pygame
import sys
from scene import getPlayer
import os


pygame.init()   

#Called before init
os.environ['SDL_VIDEO_CENTERED'] = '1' 

#Called before set_mode
info = pygame.display.Info()

screen_width, screen_height = info.current_w, info.current_h 

WIDTH, HEIGHT = 1080, 720
WHITE = (255, 255, 255)
RED = (255, 0, 0)

joysticks = {}


# create game's window

pygame.display.set_caption('Mygame')
screen = pygame.display.set_mode((screen_width-10, screen_height-50), pygame.RESIZABLE)
clock = pygame.time.Clock() 

# Couleurs
WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
DARK_GRAY = (100, 100, 100)
pygame.font.init()

# Police et taille
font = pygame.font.Font(None, 50)

# Création des boutons
class Button:
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GRAY
        self.callback = callback

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.color = DARK_GRAY if self.rect.collidepoint(pos) else GRAY

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback(joysticks)

# Fonctions des boutons
def play_game(joysticks):
    getPlayer.getPlayer(joysticks)


def open_settings():
    print("Settings button clicked")

def quit_game():
    pygame.quit()
    sys.exit()

# Création des instances de boutons
buttons = [
    Button("Play", 300, 200, 200, 50, play_game),
    Button("Settings", 300, 300, 200, 50, open_settings),
    Button("Quit", 300, 400, 200, 50, quit_game)
]

# Boucle principale
def menu():
    running = True

    pygame.joystick.init()
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        joysticks[joystick.get_instance_id()] = joystick
        print(f"Manette détectée au démarrage : {joystick.get_name()}")


    while running:
        screen.fill((50, 50, 50))
        
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    button.check_click(event.pos)
    
    pygame.quit()
    sys.exit()

 


if __name__ == "__main__":
    menu()


