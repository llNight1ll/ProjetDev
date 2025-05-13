import pygame
import os
import sys
from enum import Enum

class ControlMode(Enum):
    CONTROLLER = "controller"
    KEYBOARD = "keyboard"

class GameConfig:
    def __init__(self):
        self.control_mode = None
        self.joysticks = {}
        self.players = []
        self.is_ready = {}

    def set_control_mode(self, mode):
        self.control_mode = mode
        self.joysticks.clear()
        self.players.clear()
        self.is_ready.clear()

game_config = GameConfig()

pygame.init()

# Initialisation de la fenêtre
os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

pygame.display.set_caption('Mygame')
screen = pygame.display.set_mode((screen_width-10, screen_height-50), pygame.RESIZABLE)
clock = pygame.time.Clock()

# Couleurs
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (69, 253, 112)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
DARK_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

colors = [RED, GREEN, BLUE, WHITE, BLACK]

# Police
pygame.font.init()
font = pygame.font.Font(None, 50)

# Liste des joueurs
players = []
IsReady = {}

buttons = []

def update_players(joysticks):
    global players, buttons, IsReady
    players = [pygame.Rect(300 * i, 600, 200, 50) for i in range(len(joysticks))]

    buttons.clear()
    IsReady.clear()
    
    for i, instance_id in enumerate(joysticks):
        if game_config.control_mode == ControlMode.KEYBOARD:
            buttons.append(Button("Clavier", 300 * i, 600, 200, 50, instance_id, colors[i % len(colors)]))
        else:
            buttons.append(Button(f"Manette {i}", 300 * i, 600, 200, 50, instance_id, colors[i % len(colors)]))
        IsReady[instance_id] = False

def ready(instance_id):
    if instance_id in IsReady:
        IsReady[instance_id] = not IsReady[instance_id]
        return IsReady[instance_id]
        
def getPlayer(joysticks, control_mode=None):
    global IsReady
    running = True

    if control_mode:
        game_config.set_control_mode(control_mode)
    
    if game_config.control_mode == ControlMode.CONTROLLER:
        if len(joysticks) > 0:
            update_players(joysticks)
    elif game_config.control_mode == ControlMode.KEYBOARD:
        # Initialiser un joueur clavier par défaut
        joysticks[0] = 'keyboard'
        update_players(joysticks)
        
    while running:
        #Check if all players are ready
        start = True
        if all(IsReady.values()) and len(IsReady) > 0:
            start = True
        else:
            start = False

        # if keyboard then launch game without connecting menu
        if start or (game_config.control_mode == ControlMode.KEYBOARD):
            # Import ici pour éviter l'import circulaire
            from scene import game
            game.game(screen, screen_width, screen_height, clock, joysticks, game_config.control_mode)
            pygame.quit()
            sys.exit()
            break

        screen.fill((50, 50, 50))
        
        for button in buttons:
            if button.instance_id in IsReady:
                is_ready = IsReady[button.instance_id]
                if is_ready is True:
                    button.draw(screen, LIGHT_GREEN)
                elif is_ready is False:
                    button.draw(screen, WHITE)
            
        pygame.display.flip()
        
        joystick_names_seen = set()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #Check if a player is added
            elif event.type == pygame.JOYDEVICEADDED:
                joystick = pygame.joystick.Joystick(event.device_index)
                name = joystick.get_name()

                if name not in joystick_names_seen:
                    joystick_names_seen.add(name)
                    instance_id = joystick.get_instance_id()
                    joysticks[instance_id] = joystick
                    print(f"Manette connectée : {name} (Instance {instance_id})")
                    update_players(joysticks)
                else:
                    print(f"Manette ignorée : {name}")

            #Check if a player is removed  
            elif event.type == pygame.JOYDEVICEREMOVED:
                if event.instance_id in joysticks:
                    del joysticks[event.instance_id]
                    print("Manette déconnectée")
                    update_players(joysticks)

            #Check if a player is ready or not
            elif event.type == pygame.JOYBUTTONDOWN and event.button == 2:
                if event.instance_id in joysticks:
                    ready(event.instance_id)
                    print("appui button 2")

            elif event.type == pygame.KEYDOWN:
                #Check if a keyboard player is added or removed
                if event.key == pygame.K_a:
                    if 'keyboard' not in joysticks.values():
                        joysticks[len(joysticks)] = 'keyboard'
                        update_players(joysticks)
                        break
                    else:
                        to_remove = None
                        for index, device in joysticks.items():
                            if device == 'keyboard':
                                to_remove = index
                                break

                        if to_remove is not None:
                            del joysticks[to_remove]
                            update_players(joysticks)

                #Check if a keyboard player is ready or not
                if event.key == pygame.K_e:
                    for index, device in joysticks.items():
                        if device == 'keyboard':
                            ready(index)

class Button:
    def __init__(self, text, x, y, width, height, instance_id, color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.instance_id = instance_id
        self.color = color

    def draw(self, screen, text_color):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        text_surface = font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.color = DARK_GRAY if self.rect.collidepoint(pos) else GRAY

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            return

if __name__ == "__main__":
    getPlayer()