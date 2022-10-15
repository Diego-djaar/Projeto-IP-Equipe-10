import math
import pygame
from random import randint
from . import display


BOOST_GROUP: pygame.sprite.GroupSingle
NUM_BOOST = [0, 0]
BOOST_RECT_LIST = []
BOOST_TIMER: int


class Boost(pygame.sprite.Sprite):
    def __init__(self, typo):
        super().__init__()
        self.type = typo
        if self.type == 'shield':
            self.image = pygame.image.load('graphics/boost/shield_0.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, 0.4)
        elif self.type == 'speed':
            self.image = pygame.image.load('graphics/boost/speed_0.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, 0.35)
        self.wave = randint(70, 100)
        self.rect = self.image.get_rect(midleft=(display.DISPLAY_W*1.5, randint(display.DISPLAY_H*0.3, display.DISPLAY_H*0.7)))
        self.angle = 0
        self.speed = randint(4, 6)
        self.height = randint(display.DISPLAY_H*0.3, display.DISPLAY_H*0.7)

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
    for n in range(len(num_boost)):
        boosts_surf = display.FONT.render(
            f'{num_boost[n]}', False, (250, 200, 250))
        boosts_rect = boosts_surf.get_rect(
            center=(display.DISPLAY_W-120+n*50, 50))
        display.DISPLAY.blit(boosts_surf, boosts_rect)
