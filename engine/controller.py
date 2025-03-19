import pygame

from entities import Player

def controller(player):
    

    # handle quit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        # Vérifie que l'événement est bien une touche pressée avant d'accéder à event.key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Si la touche espace est pressée
                player.jump()
                
    
 
     # Vérifie les touches enfoncées en continu
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        player.move(-player.x_velocity)
        player.frame_movement[0] = -1
        
    
    if keys[pygame.K_d]:
        player.move(player.x_velocity)
        player.frame_movement[0] = 1