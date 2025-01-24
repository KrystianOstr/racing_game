import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Racing Game')

background_color = (0,0,0)

# CLASS: CAR

class Car:
    def __init__(self, image, speed, position_x, position_y):
        self.image = image
        self.speed = speed
        self.position_x = position_x
        self.position_y = position_y        







# main game loop

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    screen.fill(background_color)
    
    pygame.display.flip()
    
    
pygame.quit()