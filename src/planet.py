import pygame
import math
from random import randint, choice
from . import display


PLANET_GROUP: pygame.sprite.Group
PLANET_TIMER: int
PLANET_RECT_LIST = []


class Planet(pygame.sprite.Sprite):
    def __init__(self, typo):
        super().__init__()
        if typo == 'small':
            self.image = pygame.image.load('graphics/planet/planet_0.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, 0.4)
            self.speed = 6
        elif typo == 'medium':
            self.image = pygame.image.load('graphics/planet/planet_1.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, 0.6)
            self.speed = 5
        # elif type == 'large':
            # self.image = pygame.image.load('graphics/planet/planet_3.png').convert_alpha()
            # self.speed = 5
        self.rect = self.image.get_rect(midleft=(display.DISPLAY_W*1.5, randint(0, display.DISPLAY_H)))
        self.gravity = 0

    def destroy(self):
        if self.rect.x < -self.rect.w:
            self.kill()

    def update(self):
        self.rect.x -= self.speed
        self.destroy()
