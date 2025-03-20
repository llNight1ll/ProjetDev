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
     
    self.y_velocity += GRAVITY
    self.rect.y += self.y_velocity

    detectCollison(self, list_objects, x_velocity=0, y_velocity = self.y_velocity)


    if self.rect.bottom >= GROUND_Y:
        self.rect.bottom = GROUND_Y
        self.y_velocity = 0
        self.isGrounded = True

