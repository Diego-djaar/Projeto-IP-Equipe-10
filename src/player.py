import pygame
import sys
import math
from random import randint, choice

from src import boosts
from . import display
from . import collision
from .tiro import Tiro
from . import tiro

PLAYER_GROUP: pygame.sprite.GroupSingle
GAME_ACTIVE: bool
GAME_MODE: str = 'normal'


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/player/player_0.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.35)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect(center=(display.DISPLAY_W*0.25, display.DISPLAY_H*0.7))
        self.gravity = 0
        self.tiro = tiro

    def event_handler(self, event, _delta_tempo: float):
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
        # ALTERAÇÕES
        # retorna largura e altura da imagem
        # self.size = self.image.get_size() # isso não faz nada
        # ajusta tamanho do sprite
        #self.image = pygame.transform.scale(self.image, (int(self.size[0] * 0.7), int(self.size[1] * 0.7)))
        #self.image = pygame.transform.scale(self.image, (120, 80))
        # ajusta rect também (que não tava acompanhando ajuste de tamanho de 'image')
        #self.rect = self.image.get_rect()
        #self.rect = self.rect.inflate(160, 160)

    def atirar(self):
        if tiro.TIRO_TIMER <= 0:
            tiro.TIRO_GROUP.add(Tiro(self.rect.centerx + 100, self.rect.centery + 100))
            tiro.TIRO_TIMER = tiro.TIRO_INTERVALO

    def update(self, delta_tempo: float):
        if not boosts.DESACELERAR:
            self.apply_gravity(delta_tempo)
        else:
            # Não ser afetado pelo boost
            self.apply_gravity(delta_tempo*2)

        keys = pygame.key.get_pressed()

        # Move para cima ao usar seta para cima
        if keys[pygame.K_UP]:
            if not boosts.DESACELERAR:
                self.gravity -= 0.6*delta_tempo
            else:
                # Não ser afetado pelo boost
                self.gravity -= 1.2*delta_tempo

        if keys[pygame.K_SPACE]:
            self.atirar()
        if tiro.TIRO_TIMER > 0:
            tiro.TIRO_TIMER -= delta_tempo
