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
        jogador_padrao = pygame.image.load('graphics/player/player_0.png').convert_alpha()
        jogador_escudo = pygame.image.load('graphics/player/player_azul.png').convert_alpha()
        self.animacao = [jogador_padrao, jogador_escudo]
        self.indx_anim = 0

        self.image = self.animacao[self.indx_anim]
        self.image = pygame.transform.rotozoom(self.image, 0, 0.35)
        self.rect = self.image.get_rect(center=(display.DISPLAY_W*0.25, display.DISPLAY_H*0.7))
        self.gravity = 0
        self.efeito_escudo = 0
        self.escudo = False

    def event_handler(self, event, delta_tempo: float):
        pygame.key.set_repeat(80)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.gravity -= 4*delta_tempo
            if event.key == pygame.K_CAPSLOCK:
                self.efeito_escudo = 1000

    def apply_gravity(self, delta_tempo: float):
        #global game_active
        self.gravity += 0.25*delta_tempo
        self.rect.y += self.gravity*delta_tempo
        if self.rect.top > display.DISPLAY_H+200 or self.rect.bottom < -200:
            current_module = sys.modules[__name__]
            current_module.GAME_ACTIVE = False

    def estado_animacao(self):
        if self.escudo is True:
            self.indx_anim = 1
        else:
            self.indx_anim = 0
        self.image = self.animacao[self.indx_anim]
        self.image = pygame.transform.rotozoom(self.image, 0, 0.35)

    def update(self, delta_tempo: float):
        self.apply_gravity(delta_tempo)
        self.estado_animacao()
        if self.efeito_escudo > 0:
            self.escudo = True
            self.efeito_escudo -= 4
        else:
            self.escudo = False