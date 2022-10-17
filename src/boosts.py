import math
import sys
import pygame
from random import randint
from . import display


BOOST_GROUP: pygame.sprite.GroupSingle
BOOSTS_COLETADOS_DICT: dict
BOOST_RECT_LIST = []
BOOST_TIMER: int
SHIELD_IMAGE: pygame.Surface = None
SPEED_IMAGE: pygame.Surface = None
SLOW_IMAGE: pygame.Surface = None
BOOST_SPEED: int


class Boost(pygame.sprite.Sprite):
    def __init__(self, typo, speed):
        super().__init__()
        self.type = typo
        current_module = sys.modules[__name__]

        if self.type == 'shield':
            if current_module.SHIELD_IMAGE is None:
                current_module.SHIELD_IMAGE = self.image = pygame.image.load('graphics/boost/shield_0.png').convert_alpha()
            self.image = current_module.SHIELD_IMAGE
            self.image = pygame.transform.rotozoom(self.image, 0, 0.4)

        elif self.type == 'speed':
            if current_module.SPEED_IMAGE is None:
                current_module.SPEED_IMAGE = self.image = pygame.image.load('graphics/boost/speed_0.png').convert_alpha()
            self.image = current_module.SPEED_IMAGE
            self.image = pygame.transform.rotozoom(self.image, 0, 0.35)
        
        # Definindo boost de desacelerar o tempo:
        elif self.type == 'slow':
            if current_module.SLOW_IMAGE is None:
                current_module.SLOW_IMAGE = self.image = pygame.image.load('graphics/boost/slow_0.png').convert_alpha()
            self.image = current_module.SLOW_IMAGE
            self.image = pygame.transform.rotozoom(self.image, 0, 0.2)
        
        self.wave = randint(70, 100)
        self.rect = self.image.get_rect(midleft=(display.DISPLAY_W*1.5, randint(display.DISPLAY_H*0.3, display.DISPLAY_H*0.7)))
        self.angle = 0
        self.speed = speed
        self.height = randint(display.DISPLAY_H*0.3, display.DISPLAY_H*0.7)

    def movement(self, delta_tempo: float):
        self.rect.x -= self.speed*delta_tempo
        self.rect.y = self.wave*math.sin(self.angle)+self.height
        self.angle += 0.03*delta_tempo

    def destroy(self):
        if self.rect.x < -self.rect.y:
            self.kill()

    def update(self, delta_tempo: float):
        self.movement(delta_tempo)
        self.destroy()

# ---------
# FUNCTIONS
# ---------


def display_boosts(num_boost: dict):
    index = 0
    for boost in num_boost:
        boosts_surf = display.FONT.render(f'{boost}: {num_boost[boost]}', False, (250, 200, 250))
        boosts_rect = boosts_surf.get_rect(center=(display.DISPLAY_W-120, 50*index+50))
        display.DISPLAY.blit(boosts_surf, boosts_rect)
        index += 1
