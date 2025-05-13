import pygame


GRAVITY = 0.5  
GROUND_Y = 720



def detectCollison(self, list_objects,  x_velocity, y_velocity):
                
    for obj in list_objects:

        if self.rect.colliderect(obj.object):

            if y_velocity > 0:
                self.rect.bottom = obj.object.top
                self.isGrounded = True
                self.y_velocity = 0

            elif y_velocity < 0:
                    self.rect.top = obj.object.bottom
                    self.y_velocity = 0

            elif x_velocity > 0:
                self.rect.right = obj.object.left

            elif x_velocity < 0:
                self.rect.left = obj.object.right


def applyGravity(self, list_objects):
     
    self.currentSpeed.y += GRAVITY

    detectCollison(self, list_objects, x_velocity=0, y_velocity = self.currentSpeed.y)

    if self.rect.bottom >= GROUND_Y:
        self.rect.bottom = GROUND_Y
        self.currentSpeed.y = 0
        self.isGrounded = True

def applyFriction(self):
    # stop if to slow
    if abs(self.currentSpeed.x) < 0.1:
        self.currentSpeed.x = 0
        return
    
    self.currentSpeed.x *= self.x_velocity

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
                if player.rect.colliderect(other_player.rect) and not other_player.wasBumped:  
                    #check if the player is on the left or right of the other player
                    if player.rect.x < other_player.rect.x:  
                        other_player.rect.x += 6 * player.bumpPower
                    else:
                        other_player.rect.x -= 6 * player.bumpPower
                    #push player up 
                    other_player.rect.y -= 2 * player.bumpPower


