import pygame
import sys
import math
from random import randint, choice
from . import display
from . import collision
from .tiro import Tiro
from . import tiro
from . import boosts

PLAYER_GROUP: pygame.sprite.GroupSingle
GAME_ACTIVE: bool
PROTEGIDO: bool


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        jogador_padrao = pygame.image.load('graphics/player/player_0.png').convert_alpha()
        jogador_escudo = pygame.image.load('graphics/player/player_azul.png').convert_alpha()
        self.animacao = [jogador_padrao, jogador_escudo]
        self.indx_anim = 0

        self.image = self.animacao[self.indx_anim]
        self.image = pygame.transform.rotozoom(self.image, 0, 0.35)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect(center=(display.DISPLAY_W*0.25, display.DISPLAY_H*0.7))
        self.gravity = 0
        self.efeito_escudo = 0
        self.tiro = tiro

    def event_handler(self, _event, _delta_tempo: float):
        pygame.key.set_repeat(80)
        # Nada a fazer (movido)

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
            tiro.TIRO_GROUP.add(Tiro(self.rect.centerx + 100, self.rect.centery + 100))
            tiro.TIRO_TIMER = tiro.TIRO_INTERVALO

    def estado_animacao(self):
        if self.efeito_escudo > 0:
            self.indx_anim = 1
        else:
            self.indx_anim = 0
        self.image = self.animacao[self.indx_anim]
        self.image = pygame.transform.rotozoom(self.image, 0, 0.35)

    def update(self, delta_tempo: float):
        self.apply_gravity(delta_tempo)
        self.estado_animacao()
        if self.efeito_escudo > 0:
            current_module = sys.modules[__name__]
            current_module.PROTEGIDO = True
            self.efeito_escudo -= 4*delta_tempo
        else:
            current_module = sys.modules[__name__]
            current_module.PROTEGIDO = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_CAPSLOCK] and boosts.BOOSTS_COLETADOS_DICT["shield"] > 0:
            self.efeito_escudo = 1000
            boosts.BOOSTS_COLETADOS_DICT["shield"] -= 1

        # Move para cima ao usar seta para cima
        if keys[pygame.K_UP]:
            self.gravity -= 0.6*delta_tempo

        if keys[pygame.K_SPACE]:
            self.atirar()
        if tiro.TIRO_TIMER > 0:
            tiro.TIRO_TIMER -= delta_tempo
