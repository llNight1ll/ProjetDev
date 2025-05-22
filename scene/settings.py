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



    # Initialisation responsive
    WIDTH, HEIGHT = screen.get_size()
    ui = resize_elements((WIDTH, HEIGHT))
    title_font = ui["title_font"]
    text_font = ui["text_font"]
    back_button = ui["back_button"]
    scale = ui["scale"]
    scale_x = ui["scale_x"]
    scale_y = ui["scale_y"]


    running = True
    while running:
        screen.fill((50, 50, 50))

        title = font.render("Settings", True, DARK_GRAY)
        screen.blit(title, (s_Width // 2 - title.get_width() // 2, 100))

        vol_label = font.render("Music volume", True, DARK_GRAY)

        contrl1 = font.render("Left Joystick: Movement  ", True, DARK_GRAY)

        contrl2 = font.render("Right Joystick: Aim the gun  ", True, DARK_GRAY)

        contrl3 = font.render("Button 1 (Cross/A): Jump (only from the ground) / Select a button in the menu ", True, DARK_GRAY)

        contrl4 = font.render("Button 2 (R2/RT) + Left Joystick: Dash (long cooldown)  ", True, DARK_GRAY)

        contrl5 = font.render("Button 3 (R1/RB) + Right Joystick: Shoot (short cooldown)", True, DARK_GRAY)






        screen.blit(vol_label, (s_Width // 2 - vol_label.get_width() // 2, 170))

        screen.blit(contrl1, (s_Width // 2 - contrl1.get_width() // 2, 200 * 2))

        screen.blit(contrl2, (s_Width // 2 - contrl2.get_width() // 2, 200 * 2 + 10 + contrl1.get_height()))

        screen.blit(contrl3, (s_Width // 2 - contrl3.get_width() // 2, 200 * 2  + 10 + 2*contrl1.get_height()))

        screen.blit(contrl4, (s_Width // 2 - contrl4.get_width() // 2, 200*2 + 10 + 3*contrl1.get_height()))

        screen.blit(contrl5, (s_Width // 2 - contrl5.get_width() // 2, 200*2 + 10 + 4*contrl1.get_height()))

        slider.draw(screen)

        # Show music volume in percent
        volume_text = font.render(f"{int(pygame.mixer.music.get_volume() * 100)}%", True, DARK_GRAY)
        screen.blit(volume_text, (s_Width // 2 - volume_text.get_width() // 2, 350))


        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    running = False

            elif event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                running = False


            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                ui = resize_elements(event.size)
                title_font = ui["title_font"]
                text_font = ui["text_font"]
                back_button = ui["back_button"]
                scale = ui["scale"]
                scale_x = ui["scale_x"]
                scale_y = ui["scale_y"]

                WIDTH, HEIGHT = event.size
                
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
        # back button
        pygame.draw.rect(screen, GRAY, back_button, border_radius=10)
        back_text = text_font.render("Back", True, WHITE)
        back_text_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_text_rect)

        pygame.display.flip()
        clock.tick(60)







BASE_WIDTH = 1280
BASE_HEIGHT = 720

def resize_elements(screen_size):
    width, height = screen_size
    scale_x = width / BASE_WIDTH
    scale_y = height / BASE_HEIGHT
    scale = min(scale_x, scale_y)

    title_font = pygame.font.Font(None, int(72 * scale))
    text_font = pygame.font.Font(None, int(36 * scale))

    # Bouton "Back" responsive
    back_button = pygame.Rect(width // 2 - int(100 * scale), height - int(100 * scale), int(200 * scale), int(50 * scale))

    return {
        "scale": scale,
        "scale_x": scale_x,
        "scale_y": scale_y,
        "title_font": title_font,
        "text_font": text_font,
        "back_button": back_button,
        "width": width,
    }