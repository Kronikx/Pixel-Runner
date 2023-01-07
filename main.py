import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
        self.walk = [walk_1, walk_2]
        self.index = 0
        self.jump = pygame.image.load("graphics/player/jump.png").convert_alpha()

        self.image = self.walk[self.index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if (self.rect.bottom >= 300): self.rect.bottom = 300

    def animation(self):
        if self.rect.bottom < 300:
            # Jump
            self.image = self.jump
        else:
            # walk
            self.index += 0.1
            if (self.index >= len(self.walk)): self.index = 0
            self.image = self.walk[int(self.index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
        
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation(self):
        self.index += 0.1
        if (self.index >= len(self.frames)): self.index = 0
        self.image = self.frames[int(self.index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation()
        self.rect.x -= 6
        self.destroy()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = retro_font.render(f"Score: {current_time}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)
    return current_time

def display_instructions(score):
    heading_surf = retro_font.render("Pixel Runner", False, (111, 196, 169))
    heading_rect = heading_surf.get_rect(center = (400, 80))
    
    if score: instructions_surf = retro_font.render(f"Your score: {score}", False, (111, 196, 169))
    else: instructions_surf = retro_font.render("Press space to run", False, (111, 196, 169))
    instructions_rect = instructions_surf.get_rect(center = (400, 330))

    screen.blit(heading_surf, heading_rect)
    screen.blit(instructions_surf, instructions_rect)

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True

pygame.init()
screen = pygame.display.set_mode((800,400)) # Creates the window and sets it to 800 width and 400 height
pygame.display.set_caption('Pixel Runner') # Changing the windows title
clock = pygame.time.Clock() # Creating a clock object
retro_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False 
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.09)
bg_music.play(loops = -1)

# Base Surfaces
sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

# Player
player = pygame.sprite.GroupSingle()
player.add(Player())

# Obstacles
obstacle_group = pygame.sprite.Group()

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT +2
pygame.time.set_timer(snail_animation_timer, 300)

fly_animation_timer = pygame.USEREVENT +2
pygame.time.set_timer(fly_animation_timer, 200)

# Contents for starting/end screen
player_stand = pygame.image.load('graphics/player/player_stand.png')
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400,200))

# Loop to keep the display surf running
while True:
    # This tells pygame to end the game when the window is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() # Ending the loop
        
        if not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacles(choice(['fly', 'snail', 'snail', 'snail'])))

    # State management
    if game_active:
        # Displaying the games base
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf, (0,300))

        # Score
        score = display_score()

        # Player
        player.draw(screen)
        player.update()

        # Obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collisions
        game_active = collision_sprite()
    
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        display_instructions(score)

    pygame.display.update() # Updates the display
    clock.tick(60) # Telling pygame not to run faster than 60 fps