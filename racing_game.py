import pygame
from random import randint

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Racing Game')

background_color = (0,0,0)

# DRAW FPS

font = pygame.font.Font(None, 20)
def draw_fps(screen, clock):
    fps_text = font.render(f'FPS: {int(clock.get_fps())}', True, (255,255,255))
    screen.blit(fps_text, (10, 10))


# CLASS: CAR

class Car:
    def __init__(self, image, speed, position_x, position_y):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.speed = speed
        self.position_x = position_x
        self.position_y = position_y        

    def draw(self, screen):
        screen.blit(self.image, (self.position_x, self.position_y))
        
    def move(self, keys, screen_width, screen_hight):
        if keys[pygame.K_LEFT] and self.position_x > 0: # <----
            self.position_x -= self.speed
        if keys[pygame.K_RIGHT] and self.position_x < screen_width - self.image.get_width(): # ---->
            self.position_x += self.speed
        if keys[pygame.K_UP]:
            self.speed += 5
        if keys[pygame.K_DOWN]:
            self.speed -= 5
            
# CLASS: BACKGROUND

class Background:
    def __init__(self, image, road_width, screen_width, screen_height):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (road_width, screen_height))

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.road_width = road_width

        self.x_offset = (screen_width - road_width) // 2

        self.y1 = 0
        self.y2 = -self.screen_height

        self.speed = 5

    def move(self):
        self.y1 += self.speed
        self.y2 += self.speed

        if self.y1 >= self.screen_height:
            self.y1 = self.y2 - self.screen_height
        if self.y2 >= self.screen_height:
            self.y2 = self.y1 - self.screen_height


    def draw(self, screen):
        screen.blit(self.image, (self.x_offset, self.y1))
        screen.blit(self.image, (self.x_offset, self.y2))

# CLASS: OBSTACLE

class Obstacle:
    def __init__(self, image, position_x, position_y, speed):
        self.image = pygame.image.load('./images/car.png')
        self.image = pygame.transform.scale(self.image, (50, 50))


    def move(self, speed):
        pass

    def draw(self, screen):
        pass














background = Background('./images/road2.png', 200, 800, 600)
player_car = Car('./images/car.png', 5, 400, 540)

# main game loop

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    screen.fill(background_color)
    
    draw_fps(screen, clock)


    background.speed = player_car.speed
    background.move()
    background.draw(screen)
    
    player_car.draw(screen)
    keys = pygame.key.get_pressed()
    player_car.move(keys, 800, 600)
    
    
    pygame.display.flip()
    
    clock.tick(60)
    
    
pygame.quit()