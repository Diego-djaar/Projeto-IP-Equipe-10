import pygame
import sys
import math
from random import uniform, choice
from . import display
from . import player


PLANET_GROUP: pygame.sprite.Group
PLANET_TIMER: int
PLANET_RECT_LIST = []
PLANET_0_IMAGE: dict = None
PLANET_1_IMAGE: dict = None
PLANET_SPEED_EVENT: int
PLANET_SPEED_BASE = 6
PLANET_SPEED_ATUAL = 6


class Planet(pygame.sprite.Sprite):
    def __init__(self, typo, speed):
        # Define planetas de cada tipo
        super().__init__()
        current_module = sys.modules[__name__]

        if typo == 'small':
            if current_module.PLANET_0_IMAGE is None:
                current_module.PLANET_0_IMAGE =\
                    dict(normal=pygame.image.load('graphics/planet/planet_0.png').convert_alpha(),
                         cinza=pygame.image.load('graphics_cinza/planet/planet_0.png').convert_alpha())
                current_module.PLANET_0_IMAGE['normal'] = pygame.transform.rotozoom(current_module.PLANET_0_IMAGE['normal'], 0, 0.4)
                current_module.PLANET_0_IMAGE['cinza'] = pygame.transform.rotozoom(current_module.PLANET_0_IMAGE['cinza'], 0, 0.4)

            self.image_dir = current_module.PLANET_0_IMAGE
            self.image = self.image_dir[player.GAME_MODE]
            self.speed = speed

        if typo == 'medium':
            if current_module.PLANET_1_IMAGE is None:
                current_module.PLANET_1_IMAGE =\
                    dict(normal=pygame.image.load('graphics/planet/planet_1.png').convert_alpha(),
                         cinza=pygame.image.load('graphics_cinza/planet/planet_1.png').convert_alpha())
                current_module.PLANET_1_IMAGE['normal'] = pygame.transform.rotozoom(current_module.PLANET_1_IMAGE['normal'], 0, 0.6)
                current_module.PLANET_1_IMAGE['cinza'] = pygame.transform.rotozoom(current_module.PLANET_1_IMAGE['cinza'], 0, 0.6)

            self.image_dir = current_module.PLANET_1_IMAGE
            self.image = self.image_dir[player.GAME_MODE]
            self.speed = speed - 2

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
