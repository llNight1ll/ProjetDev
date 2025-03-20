import pygame

from engine.engine import detectCollison

from entities import list_objects


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.x_velocity = 10
        self.y_velocity = 10
        self.jump_power = -15
        self.image = pygame.image.load('assets/player.png')
        self.rect = self.image.get_rect()
        self.isGrounded = False
        self.frame_movement = [0,0]

        self.rect.x += 200  # Déplacer le joueur à X = 100
        

    def move(self, x_velocity1):

        self.rect.x += x_velocity1
        detectCollison(self, list_objects, x_velocity = x_velocity1, y_velocity = 0)


    def rotateSprite(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def jump(self):
        if self.isGrounded:
            self.y_velocity = self.jump_power  # Impulsion vers le haut (valeur négative)
            self.isGrounded = False
            detectCollison(self, list_objects, x_velocity=0, y_velocity = self.y_velocity)
