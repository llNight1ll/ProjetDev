import pygame

from pygame.math import Vector2

from engine.engine import detectCollison
from engine.engine import applyFriction
from engine.engine import applyGravity
from entities import list_objects

from engine.controller import controller

import random

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
        self.health = 3
        self.max_health = 3
        self.power = 10
        self.x_velocity = 0.5
        self.max_x_velocity = 15
        self.y_velocity = 10
        self.max_y_velocity = 11
        self.jump_power = 25
        self.bumpPower = 3

        self.timer = 0
        self.wasBumped = False
        self.bumpCooldown = 0
        self.bumpCooldownTime = 30

        self.currentSpeed = Vector2(0, 0)

        self.CurrentFrameDistance = Vector2(0, 0)

        self.skin_number = random.randint(1, 4)
        self.image_idle = pygame.transform.scale_by(pygame.image.load(f'assets/player{self.skin_number}.png').convert(), 0.07)
        self.image_attack = pygame.image.load('assets/player_sheet_attack.png').convert_alpha()

        self.frame_index = 0

        self.image =  self.image_idle
        self.rect = self.image.get_rect()

        
        self.isGrounded = False
        self.isAttacking = False
        self.isTakingDamage = False
        self.frame_movement = [0,0]


        self.frame_width = 64
        self.frame_height = 64

        self.spawnPointID = random.randint(0, len(SPAWN_POINTS) - 1)
        self.rect.x = SPAWN_POINTS[self.spawnPointID][0]
        self.rect.y = SPAWN_POINTS[self.spawnPointID][1]

        self.PlayerID = ID

        self.isDead = False
        

    def update(self):
        if self.isTakingDamage:
            return

        # move player at each frame
        if self.currentSpeed.x > self.max_x_velocity*3:
            self.CurrentFrameDistance.x += self.max_x_velocity*3
        else:
            self.CurrentFrameDistance.x += self.currentSpeed.x
        self.CurrentFrameDistance.y += self.currentSpeed.y

        if self.currentSpeed.y > self.max_y_velocity:
            self.currentSpeed.y = self.max_y_velocity

        # make the vector slow down on X axis
        if not self.wasBumped:
            applyFriction(self)
            applyGravity(self)

        # check if player is colliding with an object
        detectCollison(self)

        if self.wasBumped:
            self.bumpCooldown += 1
            if self.bumpCooldown > self.bumpCooldownTime:
                self.wasBumped = False
                self.bumpCooldown = 0
            
        self.rect.x += self.CurrentFrameDistance.x
        self.rect.y += self.CurrentFrameDistance.y

        self.CurrentFrameDistance = Vector2(0, 0)

    def move(self, direction):
        target_speed = direction * self.max_x_velocity
        self.currentSpeed.x += (target_speed - self.currentSpeed.x) * self.x_velocity 
        

    def rotateSprite(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def jump(self):
        if self.isGrounded:
            self.currentSpeed.y = -self.jump_power
            self.isGrounded = False
    
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

    def handleDamage(self):
        self.health -= 1
        self.currentSpeed = Vector2(0, 0)
        self.CurrentFrameDistance = Vector2(0, 0)
        self.wasBumped = False
        self.bumpCooldown = 0
        self.isGrounded = False
        self.isTakingDamage = True
        
        self.spawnPointID = random.randint(0, len(SPAWN_POINTS) - 1)
        self.rect.x = SPAWN_POINTS[self.spawnPointID][0]
        self.rect.y = SPAWN_POINTS[self.spawnPointID][1]
        
        if self.health == 0:
            self.isDead = True





        








