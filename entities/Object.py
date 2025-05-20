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

platform1 =  Object((0,255,0), pygame.Rect(rect_x - 50, rect_y - 50, rect_width, rect_height), 5) 

platform2 =  Object((0,255,0), pygame.Rect(rect_x + 350, rect_y - 200, rect_width, rect_height), 5)

platform3 =  Object((0,255,0), pygame.Rect(rect_x + 800, rect_y - 50, rect_width, rect_height), 5) 


wall1 =  Object((100,100,225), pygame.Rect(0, 0, 5, 720), 5) 
wall2 =  Object((100,100,225), pygame.Rect(1495, 0, 5, 720), 5) 

ground =  Object((100,100,225), pygame.Rect(0, 720 , 1920, 5), 5) 
roof =  Object((100,100,225), pygame.Rect(0, 0, 1920, 5), 5) 






list_objects.append(platform1)
list_objects.append(platform2)
list_objects.append(platform3)
list_objects.append(wall1)
list_objects.append(wall2)
list_objects.append(roof)
list_objects.append(ground)

print(list_objects)



