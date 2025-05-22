import pygame

from pygame.math import Vector2

from engine.engine import detectCollison
from engine.engine import applyFriction
from engine.engine import applyGravity
from entities.Pistol import Pistol

from entities.Bullet import Bullet

import random


spawn_points = [
    (100,720),
    (1280-100, 720),
    (1280//3, 720),
    (1280-1280//3, 720),
    (1280//2, 100)

]

class Player(pygame.sprite.Sprite):
    def __init__(self, ID):
        super().__init__()
        self.health = 3
        self.max_health = 3
        self.hp = 4
        self.max_hp = 4
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

        self.skin_number = ID + 1
        self.image_idle = pygame.transform.scale_by(pygame.image.load(f'assets/player{self.skin_number}.png').convert(), 0.07)

        self.frame_index = 0

        self.image =  self.image_idle
        self.baseImage =  self.image_idle
        self.rect = self.image.get_rect()

        
        self.isGrounded = False
        self.isAttacking = False
        self.isTakingDamage = False
        self.frame_movement = [0,0]


        self.frame_width = 64
        self.frame_height = 64

        self.spawnPointID = ID
        self.rect.x = spawn_points[self.spawnPointID][0]
        self.rect.y = spawn_points[self.spawnPointID][1] - self.rect.height

        self.PlayerID = ID

        self.isDead = False
        

        self.last_shot_time = 0
        self.shoot_cooldown = 700

        self.pistol = Pistol(self)

        self.canDash = True
        self.isDashing = False
        self.dashCooldown = 200
        self.dashCooldownTimer = 0
        self.dashDuration = 10
        self.dashTimer = 0
        self.dashSpeed = 50

    def dash(self, direction):
        if self.canDash and not self.isDashing and direction != 0:
            self.isDashing = True
            self.canDash = False
            self.dashTimer = 0
            self.dashDirection = direction
            self.currentSpeed.y = 0
            
    def update(self):
        if self.isTakingDamage:
            return
        # Is Dashing
        if self.isDashing:
            self.CurrentFrameDistance.x += self.dashDirection * self.dashSpeed
            self.dashTimer += 1
            if self.dashTimer >= self.dashDuration:
                self.isDashing = False
        else :
        
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

        # Gestion du cooldown du dash
        if not self.canDash and not self.isDashing:
            self.dashCooldownTimer += 1
            if self.dashCooldownTimer >= self.dashCooldown:
                self.canDash = True
                self.dashCooldownTimer = 0



    def move(self, direction):
        target_speed = direction * self.max_x_velocity
        self.currentSpeed.x += (target_speed - self.currentSpeed.x) * self.x_velocity 
        

    def rotateSprite(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def jump(self):
        if self.isGrounded:
            self.currentSpeed.y = -self.jump_power
            self.isGrounded = False


    def handleDamage(self):
        self.health -= 1
        self.currentSpeed = Vector2(0, 0)
        self.CurrentFrameDistance = Vector2(0, 0)
        self.wasBumped = False
        self.bumpCooldown = 0
        self.isGrounded = False
        self.isTakingDamage = True
        self.hp = self.max_hp
        
        self.rect.x = spawn_points[4][0]
        self.rect.y = spawn_points[4][1]
        if self.health == 0:
            self.isDead = True

    def shoot(self,dx,dy, bullets):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_shot_time >= self.shoot_cooldown:

            deadzone = 0.2

            if abs(dx) > deadzone or abs(dy) > deadzone:
                direction = (dx, dy)
                bullet = Bullet(self.rect.center[0], self.rect.center[1], direction, self.PlayerID)
                bullets.add(bullet)


                self.last_shot_time = current_time
    def resize(self, scale_x, scale_y):

    
        old_x, old_y = self.rect.x, self.rect.y


        new_size = (int(self.rect.width * scale_x), int(self.rect.height * scale_y))


        self.image =  pygame.transform.scale(self.baseImage, new_size)
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = (int(old_x * scale_x), int(old_y * scale_y))



        
        
def resizePoints(scale_x, scale_y):
    for i in range(len(spawn_points)):
        x, y = spawn_points[i]
        spawn_points[i] = (int(x * scale_x), int(y * scale_y))








