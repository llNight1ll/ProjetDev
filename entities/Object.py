import pygame   

list_objects = []


rect_x, rect_y = 300, 600
rect_width, rect_height = 200, 50

platform1 =pygame.Rect(rect_x, rect_y, rect_width, rect_height)

platform2 =pygame.Rect(rect_x + 400, rect_y - 100, rect_width, rect_height)

wall1 =pygame.Rect(0, 0, 10, 720)

list_objects.append(platform1)
list_objects.append(platform2)


list_objects.append(wall1)