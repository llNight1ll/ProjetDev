import pygame



def controller(players, eye):

    # handle quit button
    for event in pygame.event.get():


        if event.type == pygame.QUIT:
            pygame.quit()
        
  

        for player in players :

            if player.PlayerID < 0 :

                # Vérifie que l'événement est bien une touche pressée avant d'accéder à event.key
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and player.PlayerID == -1:
                        player.jump()
                    elif event.key == pygame.K_UP and player.PlayerID == -2:
                        player.jump()
                    
                    if event.key == pygame.K_LSHIFT and player.PlayerID == -1:
                        player.attack()
                    elif event.key == pygame.K_RSHIFT and player.PlayerID == -2:
                        player.attack()
                    
                    if event.key == pygame.K_g and player.PlayerID == -1:
                        player.move(player.frame_movement[0] *200)
                    elif event.key == pygame.K_RCTRL and player.PlayerID == -2:
                        player.move(player.frame_movement[0] *200)

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        eye.shoot()

            if player.PlayerID >= 0 and hasattr(event, "instance_id") and event.instance_id == player.PlayerID :
                if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                    player.jump()

                if event.type == pygame.JOYBUTTONDOWN and event.button == 2 and not player.isAttacking :
                    player.attack()

                if event.type == pygame.JOYAXISMOTION and event.axis == 5 :
                        player.move(70)


    for player in players:


        if pygame.joystick.get_count() > 0:
            for i in range(pygame.joystick.get_count()):
                joystick = pygame.joystick.Joystick(i)
                if joystick.get_instance_id() == player.PlayerID:
                    if joystick.get_axis(0) < -0.1:
                        player.move(-player.x_velocity)
                    elif joystick.get_axis(0) > 0.1:
                        player.move(player.x_velocity)


    # Vérifie les touches enfoncées en continu
    keys = pygame.key.get_pressed()
    if player.PlayerID == -1:
        if keys[pygame.K_q]:
            player.move(-player.x_velocity)
            player.frame_movement[0] = -1
        
    
        if keys[pygame.K_d]:
            player.move(player.x_velocity)
            player.frame_movement[0] = 1

    if player.PlayerID == -2:# just tu try multiplayer system with keyboard (add hardcoded player in game for testing)
        if keys[pygame.K_LEFT]:
            player.move(-player.x_velocity)
            player.frame_movement[0] = -1
        
        if keys[pygame.K_RIGHT]:
            player.move(player.x_velocity)
            player.frame_movement[0] = 1
        
    # Mise à jour de la position de l'œil autour du joueur
    mouse_pos = pygame.mouse.get_pos()
    eye.update(mouse_pos)
    eye.move()