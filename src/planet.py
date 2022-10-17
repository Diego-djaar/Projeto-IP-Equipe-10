import pygame
import sys
import math
from random import randint, choice
from . import display


PLANET_GROUP: pygame.sprite.Group
PLANET_TIMER: int
PLANET_RECT_LIST = []
PLANET_0_IMAGE: pygame.Surface = None
PLANET_1_IMAGE: pygame.Surface = None
PLANET_SPEED: int


class Planet(pygame.sprite.Sprite):
    def __init__(self, typo, speed):
        super().__init__()
        current_module = sys.modules[__name__]

        if typo == 'small':
            if current_module.PLANET_0_IMAGE is None:
                current_module.PLANET_0_IMAGE = self.image = pygame.image.load('graphics/planet/planet_0.png').convert_alpha()
            self.image = current_module.PLANET_0_IMAGE
            self.image = pygame.transform.rotozoom(self.image, 0, 0.4)
            self.speed = speed

        elif typo == 'medium':
            if current_module.PLANET_1_IMAGE is None:
                current_module.PLANET_1_IMAGE = self.image = pygame.image.load('graphics/planet/planet_1.png').convert_alpha()
            self.image = current_module.PLANET_1_IMAGE
            self.image = pygame.transform.rotozoom(self.image, 0, 0.6)
            self.speed = speed - 2
        # elif type == 'large':
            # self.image = pygame.image.load('graphics/planet/planet_3.png').convert_alpha()
            # self.speed = 5
        self.rect = self.image.get_rect(midleft=(display.DISPLAY_W*1.5, randint(0, display.DISPLAY_H)))
        self.gravity = 0

    def destroy(self):
        if self.rect.x < -self.rect.w:
            self.kill()

    def update(self, delta_tempo: float):
        self.rect.x -= self.speed*delta_tempo
        self.destroy()
