import pygame
import sys
from scene import getPlayer
from scene.settings import settings

from scene.screen import *

screen = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)

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
        return

    def isHoverController(self, action):
        if action is True:
            self.color = DARK_GRAY
        else :
           self.color = GRAY

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback(joysticks)
    
    def modifyRes(self, size):
        self.rect = pygame.Rect(size[0] // 2 -  self.rect.width// 2, self.rect.y, self.rect.width, self.rect.height)
        

# Fonctions des boutons
def play_game_controller(joysticks):
    getPlayer.getPlayer(joysticks, getPlayer.ControlMode.CONTROLLER)

def play_game_keyboard(joysticks):
    getPlayer.getPlayer(joysticks, getPlayer.ControlMode.KEYBOARD)

def open_settings(joysticks):
    settings(screen, WIDTH, joysticks)

def quit_game():
    pygame.quit()
    sys.exit()

# Create buttons for default resolution
buttons = [
    Button("Play with Controller", WIDTH // 2 - 400//2 , 150, 400, 50, play_game_controller),
    Button("Play with Keyboard", WIDTH // 2 - 400//2, 250, 400, 50, play_game_keyboard),
    Button("Settings", WIDTH // 2 - 200//2, 350, 200, 50, open_settings),
    Button("Quit", WIDTH // 2 - 200//2, 450, 200, 50, quit_game)
]

buttonSelected = 0
buttons[buttonSelected].isHoverController(True)

def selectButton(action) :
    print("appuie " + str(action))
    global buttonSelected
    if action == 0:
        buttons[buttonSelected].callback(joysticks)
    if action == 1:
        buttons[buttonSelected].isHoverController(False)
        if buttonSelected == len(buttons)-1 :
            buttonSelected = 0
            buttons[buttonSelected].isHoverController(True)

        else :
            buttonSelected += 1
            buttons[buttonSelected].isHoverController(True)
            print(buttonSelected)


    elif action == -1:
        buttons[buttonSelected].isHoverController(False)

        if buttonSelected == 0 :
            buttonSelected = len(buttons) -1
            buttons[buttonSelected].isHoverController(True)

        else :
            buttonSelected -= 1
            buttons[buttonSelected].isHoverController(True)

    
    

def menu():
    global screen
    running = True
    

    while running:
        screen.fill((50, 50, 50))
        
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                running = False
            elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, RESIZABLE)
                for button in buttons:
                    button.modifyRes(event.size)
    
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in buttons:
                    button.check_click(event.pos)

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
                selectButton(0)

            elif event.type == pygame.JOYBUTTONDOWN and event.button == 12:
                selectButton(1)

            elif event.type == pygame.JOYBUTTONDOWN and event.button == 11:
                selectButton(-1)

            elif event.type == pygame.JOYHATMOTION:
                if event.value == (0, -1):
                    selectButton(1)
                elif event.value == (0, 1):
                    selectButton(-1)


    
    pygame.quit()
    sys.exit()

 


if __name__ == "__main__":
    menu()


