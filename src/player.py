import pygame
import sys
import math
from random import randint, choice
from . import display
from . import collision
from .tiro import Tiro
from . import tiro

PLAYER_GROUP: pygame.sprite.GroupSingle
GAME_ACTIVE: bool


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/player/player_0.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.35)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect(center=(display.DISPLAY_W*0.25, display.DISPLAY_H*0.7))
        self.gravity = 0
        self.tiro = tiro

    def event_handler(self, event, delta_tempo: float):
        pygame.key.set_repeat(80)
        if event.type == pygame.KEYDOWN:
            # Nada a fazer (movido)
            pass

    def apply_gravity(self, delta_tempo: float):
        # Cai para baixo
        self.gravity += 0.25*delta_tempo
        self.rect.y += self.gravity*delta_tempo
        if self.rect.top > display.DISPLAY_H+200 or self.rect.bottom < -200:
            # Morre ao sair do display
            current_module = sys.modules[__name__]
            current_module.GAME_ACTIVE = False

    def atirar(self):
        if tiro.TIRO_TIMER <= 0:
            tiro.TIRO_GROUP.add(Tiro(self.rect.midright[0] + 100, self.rect.midright[1] + 94))
            tiro.TIRO_TIMER = tiro.TIRO_INTERVALO

    def update(self, delta_tempo: float):
        self.apply_gravity(delta_tempo)

        keys = pygame.key.get_pressed()

        # Move para cima ao usar seta para cima
        if keys[pygame.K_UP]:
            self.gravity -= 0.6*delta_tempo

        if keys[pygame.K_SPACE]:
            self.atirar()
        if tiro.TIRO_TIMER > 0:
            tiro.TIRO_TIMER -= delta_tempo
