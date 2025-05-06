import pygame



def test(player, eye):

        event = getEvent()


        if pygame.QUIT in [e.type for e in event]:
            pygame.quit()
        
        if  player.PlayerID < 0 and pygame.KEYDOWN in [e.type for e in event] : 
                


                if player.PlayerID == -1 and pygame.K_SPACE in [e.key for e in event] : 
                    player.jump()

                elif player.PlayerID == -2 and pygame.K_UP in [e.key for e in event] : 
                    player.jump()
                
                if player.PlayerID == -1 and pygame.K_LSHIFT in [e.key for e in event] : 
                    player.attack()
                elif player.PlayerID == -2 and pygame.K_RSHIFT in [e.key for e in event] :  
                    player.attack()
                
                if player.PlayerID == -1 and pygame.K_g in [e.key for e in event] : 
                    player.move(player.frame_movement[0] *200)

                elif player.PlayerID == -1 and pygame.K_RCTRL in [e.key for e in event] : 
                    player.move(player.frame_movement[0] *200)

                if pygame.MOUSEBUTTONDOWN in [e.type for e in event] : 
                    eye.shoot()

        if player.PlayerID >= 0 and hasattr(event, "instance_id") and event.instance_id == player.PlayerID :
            if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                player.jump()

            if event.type == pygame.JOYBUTTONDOWN and event.button == 2 and not player.isAttacking :
                player.attack()

            if event.type == pygame.JOYAXISMOTION and event.axis == 5 :
                    player.move(70)

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



def getEvent():
    event = pygame.event.get()
    return event