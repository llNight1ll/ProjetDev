import pygame
from scene import getPlayer

def controller(players, control_mode, bullets, events):
    # handle quit button
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()

        for player in players:
            if not player.wasBumped:
            # Keyboard mode management
                if control_mode == getPlayer.ControlMode.KEYBOARD :
                    # actions keys
                    if event.type == pygame.KEYDOWN:
                        # 1st player key
                        if player.PlayerID == 1:
                            if event.key == pygame.K_SPACE:
                                player.jump()
                            if event.key == pygame.K_e:
                                player.dash(1)

                        # 2nd player key
                        if player.PlayerID == 2:
                            if event.key == pygame.K_UP:
                                player.jump()
                            if event.key == pygame.K_g:
                                player.dash(1)



                elif control_mode == getPlayer.ControlMode.CONTROLLER and player.PlayerID >= 0:
                    if hasattr(event, "instance_id") and event.instance_id == player.PlayerID:
                        if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                            player.jump()
                        if event.type == pygame.JOYAXISMOTION and event.axis == 5:
                            joystick = pygame.joystick.Joystick(player.PlayerID)

                            direction = joystick.get_axis(0)

                            if abs(direction) > 0.5:
                                if (direction > 0) :
                                    player.dash(1)
                                else :
                                    player.dash(-1)


                        if event.type == pygame.JOYBUTTONDOWN and ( event.button == 10 or event.button == 5):
                            joystick = pygame.joystick.Joystick(player.PlayerID)
                            dx = joystick.get_axis(2)
                            dy = joystick.get_axis(3)
                            player.shoot(dx,dy, bullets)


    for player in players:
        if not player.wasBumped:
            if control_mode == getPlayer.ControlMode.KEYBOARD:
                # player keyboard movement keys
                keys = pygame.key.get_pressed()
                # 1st player key
                if player.PlayerID == 1:
                    if keys[pygame.K_q]:
                        player.move(-1)
                        player.frame_movement[0] = -1
                    if keys[pygame.K_d]:
                        player.move(1)
                        player.frame_movement[0] = 1
                # 2nd player key
                if player.PlayerID == 2:
                    if keys[pygame.K_LEFT]:
                        player.move(-1)
                        player.frame_movement[0] = -1
                    if keys[pygame.K_RIGHT]:
                        player.move(1)
                        player.frame_movement[0] = 1
            
            if control_mode == getPlayer.ControlMode.CONTROLLER and player.PlayerID >= 0:
                if pygame.joystick.get_count() > 0:
                    for i in range(pygame.joystick.get_count()):
                        joystick = pygame.joystick.Joystick(i)

                        if joystick.get_instance_id() == player.PlayerID:

                            dx = joystick.get_axis(2)
                            dy = joystick.get_axis(3)
                            player.pistol.update(dy,dx)

                            if joystick.get_axis(0) < -0.1:
                                player.move(-1)
                            elif joystick.get_axis(0) > 0.1:
                                player.move(1)

