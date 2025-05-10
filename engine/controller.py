import pygame
from scene import getPlayer

def controller(players, eye, control_mode):
    # handle quit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        for player in players:
            if control_mode == getPlayer.ControlMode.KEYBOARD and player.PlayerID == 'keyboard':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.jump()
                    if event.key == pygame.K_LSHIFT:
                        player.attack()
                    if event.key == pygame.K_g:
                        player.move(player.frame_movement[0] * 200)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        eye.shoot()

            elif control_mode == getPlayer.ControlMode.CONTROLLER and player.PlayerID >= 0:
                if hasattr(event, "instance_id") and event.instance_id == player.PlayerID:
                    if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                        player.jump()
                    if event.type == pygame.JOYBUTTONDOWN and event.button == 2 and not player.isAttacking:
                        player.attack()
                    if event.type == pygame.JOYAXISMOTION and event.axis == 5:
                        player.move(70)

    for player in players:
        if control_mode == getPlayer.ControlMode.KEYBOARD and player.PlayerID == 'keyboard':
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                player.move(-player.x_velocity)
                player.frame_movement[0] = -1
            if keys[pygame.K_d]:
                player.move(player.x_velocity)
                player.frame_movement[0] = 1

        elif control_mode == getPlayer.ControlMode.CONTROLLER and player.PlayerID >= 0:
            if pygame.joystick.get_count() > 0:
                for i in range(pygame.joystick.get_count()):
                    joystick = pygame.joystick.Joystick(i)
                    if joystick.get_instance_id() == player.PlayerID:
                        if joystick.get_axis(0) < -0.1:
                            player.move(-player.x_velocity)
                        elif joystick.get_axis(0) > 0.1:
                            player.move(player.x_velocity)

    # Mise à jour de la position de l'œil autour du joueur
    mouse_pos = pygame.mouse.get_pos()
    eye.update(mouse_pos)
    eye.move()