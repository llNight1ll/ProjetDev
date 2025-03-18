import pygame

pygame.init()   

WIDTH, HEIGHT = 1080, 720
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAVITY = 0.5  
GROUND_Y = 720

list_objects = []


rect_x, rect_y = 300, 600
rect_width, rect_height = 200, 50

platform1 =pygame.Rect(rect_x, rect_y, rect_width, rect_height)

platform2 =pygame.Rect(rect_x + 400, rect_y - 100, rect_width, rect_height)

wall1 =pygame.Rect(0, 0, 10, 720)

list_objects.append(platform1)
list_objects.append(platform2)


list_objects.append(wall1)



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

        self.rect.x += 200  # Déplacer le joueur à X = 100
        

    def move(self, x_velocity):
        
        self.rect.x += x_velocity

    def rotateSprite(self):
        self.image = pygame.transform.flip(self.image, True, False)

        
def detectCollison(self, list_objects):

    for obj in list_objects:
         if self.rect.colliderect(obj):
                # Top collision
                if self.y_velocity < 0 and self.rect.top < obj.bottom  and (self.rect.right < obj.right or self.rect.left > obj.left):
                    self.rect.top = obj.bottom    # Ajuste la position
                    self.y_velocity = 0

                    print("collison au dessus")
                 
                elif self.y_velocity > 0 and self.rect.bottom > obj.top and(self.rect.right < obj.right or self.rect.left > obj.left):
                    self.rect.bottom = obj.top  # Ajuste la position
                    self.y_velocity = 0  # Stop la chute
                    self.isGrounded = True
                    print("sur le sol")
               

                # Collision latérale (empêche de traverser l'objet sur les côtés)
                else :
                        
                    if self.rect.right > obj.left and self.rect.left < obj.right:
                        print("touche un mur")
                        if self.rect.centerx < obj.centerx:  # Collision à gauche
                            self.rect.right = obj.left
                        else:  # Collision à droite
                            self.rect.left = obj.right
                            print("touche un mur")

    

def gravity(self):
     
    self.y_velocity += GRAVITY
    self.rect.y += self.y_velocity

    if self.rect.bottom >= GROUND_Y:
        self.rect.bottom = GROUND_Y
        self.y_velocity = 0
        self.isGrounded = True



def jump(self):
    if self.isGrounded:
        self.y_velocity = self.jump_power  # Impulsion vers le haut (valeur négative)
        self.isGrounded = False
# create game's window

pygame.display.set_caption('Mygame')
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock() 

background = pygame.image.load('assets/bck.png')

offset_X = 0
offset_Y = 0

player = Player()



running = True

while running: 
    
    screen.blit(background, (offset_X,offset_Y))

    screen.blit(player.image, player.rect)

    for obj in list_objects:

        pygame.draw.rect(screen, (0,255,0), obj, 5)





    # handle quit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        # Vérifie que l'événement est bien une touche pressée avant d'accéder à event.key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Si la touche espace est pressée
                jump(player)
 
     # Vérifie les touches enfoncées en continu
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        player.move(-player.x_velocity)
        
    
    if keys[pygame.K_d]:
        player.move(player.x_velocity)
    
    gravity(player)
    detectCollison(player, list_objects)


    # Mettre à jour l'affichage
    pygame.display.flip()
    clock.tick(60)  # 60 FPS