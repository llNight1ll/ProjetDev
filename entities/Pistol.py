import pygame
import math

class Pistol(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.transform.scale_by( pygame.image.load('assets/pistol.png').convert_alpha(),0.07)
        self.baseImage = self.image
        self.rect = self.image.get_rect()
        self.player = player
        self.radius = 70
        self.angle = 0
        self.is_shooting = False

    def update(self, dy, dx):
        deadzone = 0.2

        if not self.is_shooting:
            if abs(dx) > deadzone or abs(dy) > deadzone:
                self.angle = math.atan2(dy, dx)
                angle_degrees = -math.degrees(self.angle)
                self.image = pygame.transform.rotate(self.baseImage, angle_degrees)
                self.rect = self.image.get_rect()


            self.rect.centerx = self.player.rect.centerx + self.radius * math.cos(self.angle)
            self.rect.centery = self.player.rect.centery + self.radius * math.sin(self.angle)


    def shoot(self):
        if not self.is_shooting:
            self.is_shooting = True
            self.direction = pygame.Vector2(math.cos(self.angle), math.sin(self.angle))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
