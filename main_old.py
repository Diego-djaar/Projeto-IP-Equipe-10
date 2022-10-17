import pygame
import math
from sys import exit
from random import randint, choice

# ---------
# CLASSES
# ---------


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(
            'graphics/player/player_0.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.35)
        self.rect = self.image.get_rect(center=(display_w*0.25, display_h*0.7))
        self.gravity = 0

    def event_handler(self, event):
        pygame.key.set_repeat(80)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.gravity -= 3

    def apply_gravity(self):
        global game_active
        self.gravity += 0.25
        self.rect.y += self.gravity
        if self.rect.top > display_h+200 or self.rect.bottom < -200:
            game_active = False

    def update(self):
        self.apply_gravity()


class Planet(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'small':
            self.image = pygame.image.load(
                'graphics/planet/planet_0.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, 0.4)
            self.speed = 6
        elif type == 'medium':
            self.image = pygame.image.load(
                'graphics/planet/planet_1.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, 0.6)
            self.speed = 5
        # elif type == 'large':
            # self.image = pygame.image.load('graphics/planet/planet_3.png').convert_alpha()
            # self.speed = 5
        self.rect = self.image.get_rect(
            midleft=(display_w*1.5, randint(0, display_h)))
        self.gravity = 0

    def destroy(self):
        if self.rect.x < -self.rect.w:
            self.kill()

    def update(self):
        self.rect.x -= self.speed
        self.destroy()


class Boost(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type
        if self.type == 'shield':
            self.image = pygame.image.load(
                'graphics/boost/shield_0.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, 0.4)
        elif self.type == 'speed':
            self.image = pygame.image.load(
                'graphics/boost/speed_0.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, 0.35)
        self.wave = randint(70, 100)
        self.rect = self.image.get_rect(
            midleft=(display_w*1.5, randint(display_h*0.3, display_h*0.7)))
        self.angle = 0
        self.speed = randint(4, 6)
        self.height = randint(display_h*0.3, display_h*0.7)

    def movement(self):
        self.rect.x -= self.speed
        self.rect.y = self.wave*math.sin(self.angle)+self.height
        self.angle += 0.03

    def destroy(self):
        if self.rect.x < -self.rect.y:
            self.kill()

    def update(self):
        self.movement()
        self.destroy()

# ---------
# FUNCTIONS
# ---------


def display_boosts(num_boost):
    global display_w
    for n in range(len(num_boost)):
        boosts_surf = font.render(f'{num_boost[n]}', False, (250, 200, 250))
        boosts_rect = boosts_surf.get_rect(center=(display_w-120+n*50, 50))
        display.blit(boosts_surf, boosts_rect)


def display_score():
    global start_time, display
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = font.render(f'Score: {current_time}', False, (200, 150, 200))
    score_rect = score_surf.get_rect(topleft=(50, 50))
    display.blit(score_surf, score_rect)
    return current_time


def collision_sprite():
    global game_active
    if pygame.sprite.spritecollide(player.sprite, planet_group, False):
        planet_group.empty()
        game_active = False
    # checa colisão entre o jogador e os boosts
    if pygame.sprite.spritecollideany(player.sprite, boost_group):
        boost_types = pygame.sprite.spritecollide(
            player.sprite, boost_group, True)
        for sprite in boost_types:
            if sprite.type == 'shield':
                num_boost[0] += 1
            elif sprite.type == 'speed':
                num_boost[1] += 1


pygame.init()

screen_w, screen_h = pygame.display.Info(
).current_w, pygame.display.Info().current_h
display = pygame.display.set_mode((screen_w/1.2, screen_h/1.2))
display_w, display_h = display.get_size()

pygame.display.set_caption('Allien rescue')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)

# ---------
# VARIABLES
# ---------
game_active = False
start_time = angle = speed_var = 0
num_boost = [0, 0]

# -----
# TIMER
# -----
planet_timer = pygame.USEREVENT + 1
pygame.time.set_timer(planet_timer, 3000)

boost_timer = pygame.USEREVENT + 2
pygame.time.set_timer(boost_timer, 15000)

# --------
# SURFACES
# --------
galaxy_surf = pygame.image.load('graphics/background/galaxy.png').convert()
galaxy_surf = pygame.transform.rotozoom(galaxy_surf, 0, 0.8)

# ------
# GROUPS
# ------
planet_group = pygame.sprite.Group()
planet_rect_list = []

boost_group = pygame.sprite.Group()
boost_rect_list = []

player = pygame.sprite.GroupSingle()
player.add(Player())

x = display_w*1.5
y = 100

while True:
    for event in pygame.event.get():

        player.sprite.event_handler(event)

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == planet_timer:
                planet_group.add(Planet(choice(['small', 'small', 'medium'])))
            if event.type == boost_timer:
                boost_group.add(Boost(choice(['shield', 'speed'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                planet_rect_list.clear()
                boost_rect_list.clear()
                player.sprite.rect.y = display_h*0.6
                player.sprite.gravity = speed_var = 0
                start_time = int(pygame.time.get_ticks() / 1000)

    display.blit(galaxy_surf, (0, 0))

    if game_active:
        # Player
        player.draw(display)
        player.update()

        # Planets
        planet_group.draw(display)
        planet_group.update()

        # Boosts
        boost_group.draw(display)
        boost_group.update()

        # Score and text display
        display_score()
        display_boosts(num_boost)

        collision_sprite()
    else:
        display.fill('Purple')
        planet_group.empty()

    pygame.display.update()
    clock.tick(60)
