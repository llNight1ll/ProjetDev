import pygame   

list_objects = []



class Object(pygame.sprite.Sprite):
    def __init__(self, rgb, obj, width, image = None):
        super().__init__()
        self.image = image
        self.rgb = rgb
        self.object = obj
        self.width = width



rect_x, rect_y = 300, 600
rect_width, rect_height = 200, 50

platform1 =  Object((0,255,0), pygame.Rect(rect_x, rect_y, rect_width, rect_height), 5) 

platform2 =  Object((0,255,0), pygame.Rect(rect_x + 400, rect_y - 100, rect_width, rect_height), 5) 

wall1 =  Object((0,255,0), pygame.Rect(0, 0, 10, 720), 5) 






list_objects.append(platform1)
list_objects.append(platform2)
list_objects.append(wall1)




