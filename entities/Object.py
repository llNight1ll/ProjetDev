import pygame   

class Map(pygame.sprite.Sprite):
    def __init__(self, background, objects):

        self.background = background
        self.baseBackground = background
        self.objects = objects
    def resize(self, scale_x, scale_y, width, height):
        for object in self.objects :
                object.resize(scale_x, scale_y)
        self.background = pygame.transform.scale(self.baseBackground, (width, height))
    def draw(self, screen):
        screen.blit(self.background, self.background.get_rect())
        for object in self.objects:
            pygame.draw.rect(screen, object.rgb, object.object)


class Object(pygame.sprite.Sprite):
    def __init__(self, rgb, rect, width):
        super().__init__()
        self.rgb = rgb
        self.object = rect
        self.width = width

    def resize(self, scale_x, scale_y):
        self.object.x = int(self.object.x * scale_x)
        self.object.y = int(self.object.y * scale_y)
        self.object.width = int(self.object.width * scale_x)
        self.object.height = int(self.object.height * scale_y)
        if self.width is not  None :
            self.width = int(self.width * (scale_x + scale_y) / 2)


rect_width, rect_height = 200, 25


platform1 =  Object((0,0,0), pygame.Rect(1280 // 12, 500 , rect_width, rect_height), 5) 

platform2 =  Object((0,0,0), pygame.Rect(1280 - 1280 // 12 - rect_width, 500 , rect_width, rect_height), 5)

platform3 =  Object((0,0,0), pygame.Rect( 1280//2 -rect_width//2,   300, rect_width, rect_height), 5) 

print(platform1.object.left,platform1.object.top)
print(platform2.object.left,platform2.object.top)
print(platform3.object.left,platform3.object.top)


wall1 =  Object((100,100,225), pygame.Rect(-100, 0, 100, 820), 100) 
wall2 =  Object((100,100,225), pygame.Rect(1280, 0, 100, 820), 100) 

ground =  Object((100,100,225), pygame.Rect(-100, 720, 1420, 40), 5) 
roof =  Object((100,100,225), pygame.Rect(-100, -40, 1420, 40), 5) 



objects = [
    
    platform1,
    platform2,
    platform3,
    wall1,
    wall2,
    ground,
    roof

]

map1 = Map(pygame.image.load('assets/bck2.png').convert(), objects)

