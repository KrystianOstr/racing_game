import pygame
from random import randint

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Racing Game')

game_over = False

background_color = (0,0,0)

# score

score = 0

try:
    with open('highscore.txt', 'r') as file:
        content = file.read().strip()
        high_score = int(content) if content.isdigit() else 0
except (FileNotFoundError, ValueError):
        high_score = 0

# DRAW SCORE
def draw_score(screen, score):
    if player_car.speed == 10:
        score += 3
    else:
        score += 1

    font = pygame.font.Font(None, 25)
    score_text = font.render(f'Score: {int(score)}', True, (255,255,255))
    screen.blit(score_text, (650, 10 ))
    return score

# DRAW FPS

def draw_fps(screen, clock):
    font = pygame.font.Font(None, 20)
    fps_text = font.render(f'FPS: {int(clock.get_fps())}', True, (255,255,255))
    screen.blit(fps_text, (10, 10))


# CLASS: CAR

class Car:
    def __init__(self, image, speed, position_x, position_y):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (30, 50))
        self.speed = speed
        self.position_x = position_x
        self.position_y = position_y        

    def draw(self, screen):
        screen.blit(self.image, (self.position_x, self.position_y))
        
    def move(self, keys, road_offset, road_width):
        if keys[pygame.K_LEFT] and self.position_x > road_offset: # <----
            self.position_x -= self.speed
        if keys[pygame.K_RIGHT] and self.position_x < road_offset + road_width - self.image.get_width(): # ---->
            self.position_x += self.speed
        
        
        if keys[pygame.K_UP]:
            self.speed = 10
        if keys[pygame.K_DOWN]:
            self.speed = 5
            
    def get_rect(self):
        return self.image.get_rect(topleft=(self.position_x, self.position_y))
    
    def draw_rect(self, screen): #red border - delete after tests
        pygame.draw.rect(screen, (255, 0, 0), self.get_rect(), 2)

            
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
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (30, 50))

        self.position_x = position_x
        self.position_y = position_y

        self.speed = speed


    def move(self, screen_height, road_width, road_offset, all_obstacles):
        self.position_y += self.speed + int(background.speed * 0.5)

        if self.position_y > screen_height:
            self.position_y = -50

            valid_position = False

            while not valid_position:
                new_x = road_offset + randint(0, road_width - 50)
                valid_position = all(abs(new_x - obstacle.position_x) > 50 for obstacle in all_obstacles if obstacle != self)
        
            self.position_x = new_x

    def draw(self, screen):
        screen.blit(self.image, (self.position_x, self.position_y))

    def get_rect(self):
        return self.image.get_rect(topleft=(self.position_x, self.position_y))
    
    def draw_rect(self, screen): #red border - delete after tests
        pygame.draw.rect(screen, (255, 0, 0), self.get_rect(), 2)


obstacles = [
    Obstacle('./images/enemy_car.png', 300, -50, 5),
    Obstacle('./images/enemy_car.png', 400, -200, 6),
]

background = Background('./images/road2.png', 200, 800, 600)
player_car = Car('./images/car.png', 5, 400, 540)


# GAME OVER MODULE

def game_over_screen():
    font = pygame.font.Font(None, 50)
    text = font.render("GAME OVER - R to Restart, ESC to Quit", True, (0,0,0))
    text_rect = text.get_rect(center=(400,300))
    
    while True:
        screen.fill((255,255,255))
        screen.blit(text, text_rect)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()


# RESET GAME

def reset_game():
    global player_car, obstacles, background, game_over
    
    player_car = Car('./images/car.png', 5, 400, 540)
    
    obstacles = [
    Obstacle('./images/enemy_car.png', 300, -50, 5),
    Obstacle('./images/enemy_car.png', 400, -200, 6),
]
    
    background.speed = 5

    game_over = False
    
# main game loop

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    if game_over:
        game_over_screen()
        continue
        
    screen.fill(background_color)
    
    draw_fps(screen, clock)
    score = draw_score(screen, score)


    background.speed = player_car.speed
    background.move()
    background.draw(screen)

    player_car.draw_rect(screen) #red border - delete after tests
    for obstacle in obstacles:
        obstacle.move(600, 200, (800 - 200) // 2, obstacles)
        
        if player_car.get_rect().colliderect(obstacle.get_rect()):
            game_over = True
            
        obstacle.draw_rect(screen) #red border - delete after tests
        
        
        obstacle.draw(screen)
    
    player_car.draw(screen)
    keys = pygame.key.get_pressed()
    player_car.move(keys, background.x_offset, background.road_width)
    
    # if player_car.speed == 10:
    #     score += 1.2
    # else:
    #     score += 1
    
    pygame.display.flip()
    
    clock.tick(60)
    
    
pygame.quit()