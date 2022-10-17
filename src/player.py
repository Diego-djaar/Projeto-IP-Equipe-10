import pygame
import sys
import math
from random import randint, choice
from . import display
from . import collision


PLAYER_GROUP: pygame.sprite.GroupSingle
GAME_ACTIVE: bool


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/player/player_0.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.35)
        self.rect = self.image.get_rect(center=(display.DISPLAY_W*0.25, display.DISPLAY_H*0.7))
        self.gravity = 0

    def event_handler(self, event):
        pygame.key.set_repeat(80)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.gravity -= 3

    def apply_gravity(self):
        #global game_active
        self.gravity += 0.25
        self.rect.y += self.gravity
        if self.rect.top > display.DISPLAY_H+200 or self.rect.bottom < -200:
            current_module = sys.modules[__name__]
            current_module.GAME_ACTIVE = False

    def update(self):
        self.apply_gravity()
