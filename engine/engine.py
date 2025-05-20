import pygame

from entities import list_objects


GRAVITY = 1
FRICTION = 0.90

DEAD_SPEED = 28


def detectCollison(self):
    if self.isTakingDamage:
        return

    CollisionTestRect = self.rect.copy()
    CollisionTestRect.x += self.CurrentFrameDistance.x

    # check on x axis
    for obj in list_objects:
        if CollisionTestRect.colliderect(obj.object):
            # if force was to high then explode
            if self.currentSpeed.x > DEAD_SPEED or self.currentSpeed.x < -DEAD_SPEED:
                self.isTakingDamage = True
                self.handleDamage()
                self.isTakingDamage = False
                return

            # reset test rect to check on y axis
            CollisionTestRect.x -= self.CurrentFrameDistance.x

            if self.CurrentFrameDistance.x > 0: 
                self.CurrentFrameDistance.x = obj.object.left - self.rect.right
            else:
                self.CurrentFrameDistance.x = obj.object.right - self.rect.left
    
    # check on y axis
    CollisionTestRect.y += self.CurrentFrameDistance.y

    for obj in list_objects:
        if CollisionTestRect.colliderect(obj.object):
            # if colision when going down then on ground
            if self.CurrentFrameDistance.y > 0:
                self.isGrounded = True
                self.CurrentFrameDistance.y = obj.object.top - self.rect.bottom
            else:
                self.CurrentFrameDistance.y = obj.object.bottom - self.rect.top
                self.currentSpeed.y = 0


def applyGravity(self):
    if self.isTakingDamage:
        return
        
    self.currentSpeed.y += GRAVITY
    detectCollison(self)

def applyFriction(self):
    if self.isTakingDamage:
        return
        
    # stop if to slow
    if abs(self.currentSpeed.x) < 0.1:
        self.currentSpeed.x = 0
        return
    
    self.currentSpeed.x *= FRICTION

    # max speed handle
    if abs(self.currentSpeed.x) > self.max_x_velocity:
        self.currentSpeed.x = self.max_x_velocity * (1 if self.currentSpeed.x > 0 else -1)

#fonction that check collisons between players
def checkPlayerCollision(Players):
    for i, player in enumerate(Players):
        for j, other_player in enumerate(Players):
            # don't check himself
            if i != j:
                #check for colision
                if player.rect.colliderect(other_player.rect) and not player.wasBumped and not player.isDead:  
                    #check if the player should push of be pushed
                    if abs(player.currentSpeed.x) > abs(other_player.currentSpeed.x):
                        if player.rect.x < other_player.rect.x:
                            other_player.currentSpeed.x += abs(player.currentSpeed.x) * player.bumpPower
                        else:
                            other_player.currentSpeed.x -= abs(player.currentSpeed.x) * player.bumpPower
                            
                        #push player up 
                        other_player.currentSpeed.y -= player.bumpPower
                        other_player.isGrounded = False
                        other_player.wasBumped = True


