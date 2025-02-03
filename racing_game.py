import pygame
from pathlib import Path
import sys
from random import randint

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Racing Game')

game_over = False

# DYNAMIC PATH FOR EXE

BASE_PATH =  Path(getattr(sys, '_MEIPASS', Path(__file__).parent))

# SOUNDS

collision_sound = pygame.mixer.Sound(BASE_PATH / 'sounds' / 'collision.mp3')
background_music = (BASE_PATH / 'sounds' / 'background_music.mp3')
game_over_music = (BASE_PATH / 'sounds' / 'gameover.mp3')


def play_music(sound):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)
    
play_music(background_music)

# FONTS

font_small = pygame.font.Font(None, 20)  # for FPS
font_medium = pygame.font.Font(None, 25)  # for score
font_large = pygame.font.Font(None, 50)  # for Game Over

# COLORS

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)


# score

score = 0

try:
    with open('highscore.txt', 'r') as file:
        content = file.read().strip()
        high_score = int(content) if content.isdigit() else 0
except (FileNotFoundError, ValueError):
        high_score = 0


def save_high_score(score):
    global high_score

    if score > high_score:
        high_score = score
        with open("highscore.txt", 'w') as file:
            file.write(str(int(high_score)))


# CLASS: CAR

class Car:
    def __init__(self, image, speed, position_x, position_y):
        # print(f"Scaling image: {image}") # FPS TEST TEST
        self.image = pygame.image.load(BASE_PATH / 'images' / image)
        self.image = pygame.transform.scale(self.image, (30, 50))
        self.speed = speed
        self.position_x = position_x
        self.position_y = position_y        

    def draw(self, screen):
        screen.blit(self.image, (self.position_x, self.position_y))
        
    def move(self, keys, road_offset, road_width):
        if keys[pygame.K_LEFT] and self.position_x > road_offset - 20:  # <---
            self.position_x -= self.speed
        if keys[pygame.K_RIGHT] and self.position_x < road_offset + road_width + 20 - self.image.get_width():  # --->
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
        self.image = pygame.image.load(BASE_PATH / 'images' / image)
        # self.image = pygame.transform.scale(self.image, (road_width, screen_height))
        # print(self.image.get_width(), self.image.get_height())


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
        screen.blit(self.image, (0, self.y1))
        screen.blit(self.image, (0, self.y2))

# CLASS: OBSTACLE

class Obstacle:
    def __init__(self, image, position_x, position_y, speed):
        self.image = pygame.image.load(BASE_PATH / 'images' / image)
        self.image = pygame.transform.scale(self.image, (30, 50))

        self.position_x = position_x
        self.position_y = position_y
        
        self.base_speed = speed
        self.speed = speed


    def move(self, screen_height, road_width, road_offset, all_obstacles):
        self.speed = self.base_speed + int(score/500) # Increase speed basing on score
        
        self.position_y += self.speed + int(background.speed * 0.5)

        if self.position_y > screen_height:
            self.position_y = -50
            valid_position = False

            while not valid_position:
                new_x = road_offset - 10 + randint(0, road_width + 20)

                valid_position = all(abs(new_x - obstacle.position_x) > 50 for obstacle in all_obstacles if obstacle != self)
        
            self.position_x = new_x

    def draw(self, screen):
        screen.blit(self.image, (self.position_x, self.position_y))

    def get_rect(self):
        return self.image.get_rect(topleft=(self.position_x, self.position_y))
    
    def draw_rect(self, screen): #red border - delete after tests
        pygame.draw.rect(screen, (255, 0, 0), self.get_rect(), 2)

# CLASS: MENU

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.options = ['Start', 'Options', 'Exit']
        self.current_option = 0
        
        self.font = pygame.font.Font(None, 50)
        self.white = (255,255,255)
        self.red = (255,0,0)
        self.black = (0,0,0)

    def run(self):
        while True:
            self.screen.fill(self.black)
            self.draw()
            pygame.display.flip()
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if self.handle_input(event):
                        return

    def draw(self):
        for i, option in enumerate(self.options):
            color = self.red if i == self.current_option else self.white
            text_surface = self.font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(400,300 + i * 60))
            self.screen.blit(text_surface, text_rect)
            
    def handle_input(self, event):
        if event.key == pygame.K_DOWN:
            self.current_option = (self.current_option + 1) % len(self.options)
        elif event.key == pygame.K_UP:
            self.current_option = (self.current_option - 1) % len(self.options)
        elif event.key == pygame.K_RETURN:
            if self.current_option == 0: #game start
                return True
            elif self.current_option == 1: #settings
                self.settings_screen()
            elif self.current_option == 2: #exit
                pygame.quit()
                exit()
        return False
    
    def settings_screen(self):
        volume = pygame.mixer.music.get_volume()
        self.settings_options = ["Volume", "Back"]
        self.current_setting = 0
        
        
        while True:
            self.screen.fill(self.black)
            
            self.draw_controls_info()
            
            self.draw_settings()
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.current_setting = (self.current_setting + 1) % len(self.settings_options)
                    elif event.key == pygame.K_UP:
                        self.current_setting = (self.current_setting - 1) % len(self.settings_options)
                    elif event.key == pygame.K_LEFT and self.current_setting == 0:
                        volume = max(0.0, volume - 0.1)
                        pygame.mixer.music.set_volume(volume)
                    elif event.key == pygame.K_RIGHT and self.current_setting == 0:
                        volume = min(1.0, volume + 0.1)
                        pygame.mixer.music.set_volume(volume)
                    elif event.key == pygame.K_RETURN and self.current_setting == 1:
                        return
                    elif event.key == pygame.K_ESCAPE:
                        return
    
    def draw_controls_info(self):
        controls_text = [
            "Controls:",
            "/\ Speed Up",
            "V  Brake",
            "<- Move Left",
            "-> Move Right",
            "Enter Select",
            "ESC Back"
        ]

        for j, line in enumerate(controls_text):
            controls_font = pygame.font.Font(None, 25)
            controls_surface = controls_font.render(line, True, self.white)
            controls_rect = controls_surface.get_rect(center=(400, 50 + j * 30))
            self.screen.blit(controls_surface, controls_rect)
    
    def draw_settings(self): 
        volume = pygame.mixer.music.get_volume()
        
        for i, option in enumerate(self.settings_options):
            color = self.red if i == self.current_setting else self.white
            text_surface = self.font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(400, 300 + i * 60))
            self.screen.blit(text_surface, text_rect)
            
            if option == "Volume":
                bar_filled = round(volume * 10)
                volume_bar = "|" * bar_filled + '-' * (10 - bar_filled)
                volume_surface = self.font.render(f'[{volume_bar}]', True, self.white)
                volume_rect = volume_surface.get_rect(center=(600, 300 + i * 60))
                self.screen.blit(volume_surface, volume_rect)
    
      


obstacles = [
    Obstacle('enemy_car.png', 300, -50, 5),
    Obstacle('enemy_car.png', 400, -200, 6),
]

background = Background('road5.png', 200, 800, 600)
player_car = Car('car.png', 5, 400, 540)


def draw_text(screen, text, font, x, y, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x,y))
    
    screen.blit(text_surface, text_rect)


# GAME OVER MODULE

def game_over_screen():
    global high_score
    save_high_score(score)

    play_music(game_over_music)

    while True:
        screen.fill((255,255,255))

        draw_text(screen, 'GAME OVER - R to Restart, ESC to Quit', font_large, 400, 300, black)
        draw_text(screen, f'High score: {int(high_score)}', font_large,400,250,red)
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
    global player_car, obstacles, background, game_over, score
    
    player_car = Car('car.png', 5, 400, 540)
    
    obstacles = [
    Obstacle('enemy_car.png', 300, -50, 5),
    Obstacle('enemy_car.png', 400, -200, 6),
]
    
    background.speed = 5
    score = 0

    
    play_music(background_music)

    game_over = False
    

# MENU LOOP
    
menu = Menu(screen)
menu.run()       

# main game loop

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    if game_over:
        game_over_screen()
        continue
        
    screen.fill(black)
    
    background.speed = player_car.speed
    background.move()
    background.draw(screen)

    # draw_text(screen, f'FPS: {int(clock.get_fps())}', font_small, 50, 10, white)
    draw_text(screen, f'Score: {int(score)}', font_medium, 700, 40, black)
    draw_text(screen, f'High score: {int(high_score)}', font_medium, 700, 10, black)


    # player_car.draw_rect(screen) #red border - delete after tests
    for obstacle in obstacles:
        obstacle.move(600, 200, (800 - 200) // 2, obstacles)
        
        if player_car.get_rect().colliderect(obstacle.get_rect()):
            collision_sound.play()
            game_over = True
            
        # obstacle.draw_rect(screen) #red border - delete after tests
        
        obstacle.draw(screen)
    
    # print(f"FPS: {clock.get_fps()}") $ FPS TEST TEST

    player_car.draw(screen)
    keys = pygame.key.get_pressed()
    player_car.move(keys, background.x_offset, background.road_width)
    
    if not game_over:   
        if player_car.speed == 10:
            score += 1.2
        else:
            score += 1
    
    pygame.display.flip()
    
    clock.tick(60)
    
    
pygame.quit()