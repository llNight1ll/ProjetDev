import pygame
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed=30):
        super().__init__()
        self.image = pygame.Surface((10, 7))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))

        # Normalize direction
        length = math.hypot(direction[0], direction[1])
        if length != 0:
            self.direction = (direction[0] / length, direction[1] / length)
        else:
            self.direction = (0, 0)

        self.speed = speed

    def update(self):
        dx = self.direction[0] * self.speed
        dy = self.direction[1] * self.speed
        self.rect.x += dx
        self.rect.y += dy

        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()

        if (self.rect.right < 0 or self.rect.left > screen_width or
            self.rect.bottom < 0 or self.rect.top > screen_height):
            self.kill()