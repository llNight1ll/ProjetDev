import pygame

from entities import Player

from engine.controller import controller

from engine.engine import applyGravity

from entities import Player

from entities import list_objects




pygame.init()   



WIDTH, HEIGHT = 1080, 720
WHITE = (255, 255, 255)
RED = (255, 0, 0)



# create game's window

pygame.display.set_caption('Mygame')
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock() 

background = pygame.image.load('assets/bck.png')

offset_X = 0
offset_Y = 0

player = Player.Player()




running = True

while running: 
    
    screen.blit(background, (offset_X,offset_Y))

    screen.blit(player.image, player.rect)

    for obj in list_objects:

        pygame.draw.rect(screen, (0,255,0), obj, 5)





    controller(player)

    
    applyGravity(player, list_objects)


    # Mettre à jour l'affichage
    pygame.display.flip()
    clock.tick(60)  # 60 FPS