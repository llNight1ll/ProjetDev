import pygame

from entities import Player

def controller(player, eye):
    

    # handle quit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        # Vérifie que l'événement est bien une touche pressée avant d'accéder à event.key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Si la touche espace est pressée
                player.jump()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            eye.shoot()
                
        if event.type == pygame.JOYBUTTONDOWN:
                print(event)
        if event.type == pygame.JOYBUTTONUP:
            print(event)
        if event.type == pygame.JOYAXISMOTION:
            print(event)
        if event.type == pygame.JOYHATMOTION:
            print(event)
 
     # Vérifie les touches enfoncées en continu
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        player.move(-player.x_velocity)
        player.frame_movement[0] = -1
        
    
    if keys[pygame.K_d]:
        player.move(player.x_velocity)
        player.frame_movement[0] = 1
    
    # Mise à jour de la position de l'œil autour du joueur
    mouse_pos = pygame.mouse.get_pos()
    eye.update(mouse_pos)
    eye.move()