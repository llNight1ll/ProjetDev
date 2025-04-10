import pygame
import os
import sys
from scene import game

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
IsReady = []
joysticks = {}

buttons = []

def update_players():
    global players, buttons, IsReady
    players = [pygame.Rect(300 * i, 600, 200, 50) for i in range(len(joysticks))]

    buttons.clear()
    IsReady.clear()
    
    for i in range(len(joysticks)):
        buttons.append(Button(f"Player {i}", 300 * i, 600, 200, 50, i, colors[i]))
        IsReady.append(False)



def ready(player_id):
    print(player_id)
    if IsReady[player_id] :
        IsReady[player_id] = False
        return False

    else :  
        IsReady[player_id] = True
        return True

        


            
def getPlayer():
    global IsReady
    running = True
    while running:

        #Check if all players are ready
        start = True

        if not IsReady :
          start = False  
        for status in IsReady:
            if status is False:
                start = False
                break
        if start :
            game.game(screen,screen_width, screen_height, clock, len(IsReady))
            pygame.quit()
            sys.exit()
            break


        screen.fill((50, 50, 50))
        
        # Draw players
        print(joysticks)
        for button in buttons :
            is_ready = IsReady[button.player_id]
            if is_ready is True:
                button.draw(screen, LIGHT_GREEN)
            elif is_ready is False:
                button.draw(screen, WHITE)
        
        print(IsReady)
        pygame.display.flip()
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #Check if a player is added

            elif event.type == pygame.JOYDEVICEADDED:
                joystick = pygame.joystick.Joystick(event.device_index)
                joysticks[joystick.get_instance_id()] = joystick
                print(f"Manette connectée: {joystick.get_name()}")
                update_players()

            #Check if a player is removed  
            elif event.type == pygame.JOYDEVICEREMOVED:
                if event.instance_id in joysticks:
                    del joysticks[event.instance_id]
                    print("Manette déconnectée")
                    update_players()

            #Check if a player is  ready or not
            elif event.type == pygame.JOYBUTTONDOWN and event.button == 2:
                if event.instance_id in joysticks:
                    ready(event.instance_id -1)
                    print("appui button 2")

            elif event.type == pygame.KEYDOWN:

                #Check if a keyboard player is added or removed
                if event.key == pygame.K_a:
                    if 'keyboard' not in joysticks.values():
                        joysticks[len(joysticks)] = 'keyboard'
                        update_players()
                        break
                    else:
                        to_remove = None
                        for index, device in joysticks.items():
                            if device == 'keyboard':
                                to_remove = index
                                break

                        if to_remove is not None:
                            del joysticks[to_remove]
                            update_players()



                #Check if a keyboard player is ready or not

                if event.key == pygame.K_e:
                   for index, device in joysticks.items():
                        if device == 'keyboard':
                            ready(index)

    
    








class Button:
    def __init__(self, text, x, y, width, height, player_id, color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.player_id = player_id
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