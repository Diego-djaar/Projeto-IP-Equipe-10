import pygame
import sys
import math
from random import uniform, choice
from . import display


ASTEROIDE_GROUP: pygame.sprite.Group
ASTEROIDE_TIMER: int
ASTEROIDE_IMAGE: pygame.Surface = None
ASTEROIDE_SPEED_EVENT: int
ASTEROIDE_SPEED_BASE = 7
ASTEROIDE_SPEED_ATUAL = 7


class Asteroide(pygame.sprite.Sprite):
    def __init__(self, typo, speed):
        # Define planetas de cada tipo
        super().__init__()
        current_module = sys.modules[__name__]

        if typo == 'small':
            if current_module.ASTEROIDE_IMAGE is None:
                current_module.ASTEROIDE_IMAGE = self.image = pygame.image.load('graphics/asteroide/asteroide.png').convert_alpha()
            self.image = current_module.ASTEROIDE_IMAGE
            self.image = pygame.transform.rotozoom(self.image, 0, 0.7)
            self.speed = speed

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect(
            midleft=(display.DISPLAY_W*1.5, uniform(0, display.DISPLAY_H)))
        self.gravity = 0

    def try_destroy(self):
        if self.rect.x < -1000:
            self.kill()

    def movement(self, delta_tempo: float):
        self.rect.x -= self.speed*delta_tempo

    def update(self, delta_tempo: float):
        self.movement(delta_tempo)
        self.try_destroy()
