import pygame
import os
from pygame.locals import *
#Called before init
os.environ['SDL_VIDEO_CENTERED'] = '1' 

#Called before set_mode
info = pygame.display.Info()

screen_width, screen_height = 1920, 1080

WIDTH, HEIGHT = screen_width, screen_height
WHITE = (255, 255, 255)
RED = (255, 0, 0)

joysticks = {}


pygame.init()

# create game's window

pygame.display.set_caption('Mygame')
screen = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)
clock = pygame.time.Clock() 

# Colors
WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
DARK_GRAY = (100, 100, 100)
pygame.font.init()

#Fonts and sizes
font = pygame.font.Font(None, 50)

