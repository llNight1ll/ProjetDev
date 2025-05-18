import pygame
import sys
from scene.screen import WIDTH



# Colors
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 120, 255)

# Font
font = pygame.font.SysFont(None, 40)

# Music start

volume = 0

pygame.mixer.music.load("assets/music/music1.mp3")
pygame.mixer.music.set_volume(float(volume))
pygame.mixer.music.play(-1)

#Define slider
class Slider:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - 400//2, 300, 400, 10)
        self.color = GRAY
        self.handle_x = int(self.rect.x + volume * self.rect.width)
        self.handle_radius = 15


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        pygame.draw.circle(screen, BLUE, (self.handle_x, self.rect.centery), self.handle_radius)
    
    def modifyRes(self, size):
        self.rect = pygame.Rect(size[0] // 2 -  self.rect.width// 2, self.rect.y, self.rect.width, self.rect.height)
        self.handle_x = int(self.rect.x + volume * self.rect.width)
        



slider = Slider()

slider.handle_x = int(slider.rect.x + volume * slider.rect.width)





def update_volume(mouse_x):
    global volume
    slider.handle_x = max(slider.rect.left, min(mouse_x, slider.rect.right))
    relative_x = slider.handle_x - slider.rect.left
    new_volume = relative_x / slider.rect.width
    volume = new_volume
    pygame.mixer.music.set_volume(new_volume)
    return new_volume


def update_volume_controller(action):
    global volume
    new_volume = 0
    if action == 1:
        handle_x = max(slider.rect.left, min(slider.handle_x + slider.rect.width//100, slider.rect.right))
        slider.handle_x = handle_x
        volume = max(0, min(volume + 0.01, 1.0))
        new_volume = volume

    else :
        handle_x = max(slider.rect.left, min(slider.handle_x - slider.rect.width//100, slider.rect.right))
        slider.handle_x = handle_x
        volume = max(0, min(volume - 0.01, 1.0))
        new_volume = volume

    print(new_volume)

    pygame.mixer.music.set_volume(new_volume)
    return new_volume


def settings(screen, SCREEN_WIDTH, joysticks):
    s_Width = SCREEN_WIDTH
    clock = pygame.time.Clock()
    dragging = False

    while True:
        screen.fill(WHITE)

        title = font.render("Settings", True, DARK_GRAY)
        screen.blit(title, (s_Width // 2 - title.get_width() // 2, 100))

        vol_label = font.render("Music volume", True, DARK_GRAY)
        screen.blit(vol_label, (s_Width // 2 - vol_label.get_width() // 2, 230))

        slider.draw(screen)

        # Show music volume in percent
        volume_text = font.render(f"{int(pygame.mixer.music.get_volume() * 100)}%", True, DARK_GRAY)
        screen.blit(volume_text, (s_Width // 2 - volume_text.get_width() // 2, 350))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if abs(event.pos[0] - slider.handle_x) <= slider.handle_radius and abs(event.pos[1] - slider.rect.centery) <= slider.handle_radius:
                        dragging = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    update_volume(event.pos[0])

            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                s_Width = event.size[0]
                slider.modifyRes(event.size)



            elif event.type == pygame.JOYDEVICEADDED:
                joystick = pygame.joystick.Joystick(event.device_index)
                joystick.init()
                joysticks[joystick.get_instance_id()] = joystick
                print(f"Manette connectée : {joystick.get_name()}")

            elif event.type == pygame.JOYDEVICEREMOVED:
                if event.instance_id in joysticks:
                    del joysticks[event.instance_id]
                    print("Manette déconnectée")
                


            elif event.type == pygame.JOYBUTTONDOWN and event.button == 14:
                update_volume_controller(1)

            elif event.type == pygame.JOYBUTTONDOWN and event.button == 13:
                update_volume_controller(-1)

            elif event.type == pygame.JOYHATMOTION:
                if event.value == (1, 0):
                    update_volume_controller(1)
                elif event.value == (-1, 0):
                    update_volume_controller(-1)


        pygame.display.flip()
        clock.tick(60)







      