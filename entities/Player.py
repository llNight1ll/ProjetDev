import pygame

from engine.engine import detectCollison
from engine.engine import applyFriction

from entities import list_objects

SPAWN_POINTS = [
    (300, 445),
    (700, 295), 
    (1150, 445),
    (1550, 615), 
    (700, 615), 
    (70, 615) 
]

class Player(pygame.sprite.Sprite):
    def __init__(self, ID):
        super().__init__()
        self.health = 100
        self.max_health = 100
        self.power = 10
        self.x_velocity = 5
        self.y_velocity = 10
        self.jump_power = -15

        self.timer = 0




        self.image_idle =  pygame.image.load('assets/player.png').convert_alpha()
        self.image_attack =  pygame.image.load('assets/player_sheet_attack.png').convert_alpha()

        self.frame_index = 0

        self.image =  self.image_idle
        self.rect = self.image.get_rect()

        
        self.isGrounded = False
        self.isAttacking = False
        self.frame_movement = [0,0]


        self.frame_width = 64
        self.frame_height = 64

        self.rect.x += 200  # Déplacer le joueur à X = 100
        self.PlayerID = ID
        

    def move(self, x_velocity1):

        self.rect.x += x_velocity1
        detectCollison(self, list_objects, x_velocity = x_velocity1, y_velocity = 0)
        applyFriction(self)



    def rotateSprite(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def jump(self):
        if self.isGrounded:
            self.y_velocity = self.jump_power  # Impulsion vers le haut (valeur négative)
            self.isGrounded = False
            detectCollison(self, list_objects, x_velocity=0, y_velocity = self.y_velocity)
    
    def attack(self):
        self.isAttacking = True
        self.play_animation(140,103,4)


    def play_animation(self, frame_width, frame_height, frame_number):
        frame_time = 5

        self.image = self.image_attack


        frames = [self.image.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)) for i in range(frame_number)]



        self.image = frames[self.frame_index]

        self.timer +=1

        if (self.timer > frame_time or self.frame_index == 0 ):

            self.frame_index = (self.frame_index + 1) % frame_number
            self.timer = 0
        

        if (self.frame_index == frame_number - 1 and self.timer >= frame_time):
            self.frame_index = 0
            self.image = self.image_idle
            self.timer = 0
            self.isAttacking = False





        








