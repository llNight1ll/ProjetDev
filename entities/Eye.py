import pygame
import math

class Eye(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.image.load('assets/eye.png')
        self.rect = self.image.get_rect()
        self.player = player
        self.radius = 50
        self.angle = 0
        self.speed = 15
        self.direction = pygame.Vector2(0, 0)
        self.is_shooting = False

    def update(self, mouse_pos):
        if not self.is_shooting:
            # Calculer angle
            dx = mouse_pos[0] - self.player.rect.centerx
            dy = mouse_pos[1] - self.player.rect.centery
            self.angle = math.atan2(dy, dx)

            # Autour joueur
            self.rect.centerx = self.player.rect.centerx + self.radius * math.cos(self.angle)
            self.rect.centery = self.player.rect.centery + self.radius * math.sin(self.angle)

    def shoot(self):
        if not self.is_shooting:
            self.is_shooting = True
            self.direction = pygame.Vector2(math.cos(self.angle), math.sin(self.angle))

    def move(self):
        if self.is_shooting:
            self.rect.x += self.direction.x * self.speed
            self.rect.y += self.direction.y * self.speed
