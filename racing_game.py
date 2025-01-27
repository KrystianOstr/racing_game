import pygame

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
        if keys[pygame.K_UP]: # speed up
            self.speed = 10 
        if keys[pygame.K_DOWN]: # speed down
            self.speed = 5
            
            


player_car = Car('./images/car.png', 5, 400, 540)




# main game loop

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    screen.fill(background_color)
    
    draw_fps(screen, clock)
    player_car.draw(screen)
    keys = pygame.key.get_pressed()
    player_car.move(keys, 800, 600)
    
    
    pygame.display.flip()
    
    clock.tick(60)
    
    
pygame.quit()