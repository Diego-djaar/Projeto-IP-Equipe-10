import pygame
import sys
import math
from random import uniform, choice
from . import display
from . import player
from . import collision
from . import game
from . import tiro

INIMIGO_GROUP: pygame.sprite.Group
INIMIGO_TIMER: int
INIMIGO_IMAGE: pygame.Surface = None
INIMIGO_SPEED_EVENT: int
INIMIGO_SPEED_BASE = 7
INIMIGO_SPEED_ATUAL = 7


class Inimigo(pygame.sprite.Sprite):
    pontos_de_vida = 2

    def __init__(self, speed):
        super().__init__()
        current_module = sys.modules[__name__]
        inimigo_normal = pygame.image.load('graphics/inimigo/inimigo.png').convert_alpha()
        inimigo_explodido = pygame.image.load('graphics/inimigo/paf.png').convert_alpha()
        if current_module.INIMIGO_IMAGE is None:
            current_module.INIMIGO_IMAGE = self.image = inimigo_normal
        self.animacao = [inimigo_normal, inimigo_explodido]
        self.image = self.animacao[0]
        self.image = pygame.transform.rotozoom(self.image, 0, 0.5)
        self.speed = speed

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect(
            midleft=(display.DISPLAY_W*1.5, uniform(0, display.DISPLAY_H)))
        self.gravity = 0
        self.atingido = False
        # hora de morte
        self.hm = 0

    def dano(self):
        if self.atingido is False and self.pontos_de_vida == 1:
            self.atingido = True
            self.hm = pygame.time.get_ticks() + 140
        else:
            self.pontos_de_vida -= 1

    def aproximar(self):
        if self.rect.y < player.PLAYER_GROUP.sprite.rect.y:
            self.rect.y += 1.5
        elif self.rect.y > player.PLAYER_GROUP.sprite.rect.y:
            self.rect.y -= 1.5

    def explodir(self):
        self.image = self.animacao[1]
        self.image = pygame.transform.rotozoom(self.image, 0, 0.4)
        agora = pygame.time.get_ticks()
        if agora > self.hm:
            self.kill()

    def try_destroy(self):
        if self.rect.x < -1000:
            self.kill()
        elif self.atingido is True:
            self.explodir()

    def movement(self, delta_tempo: float):
        self.rect.x -= self.speed*delta_tempo

    def update(self, delta_tempo: float):
        self.movement(delta_tempo)
        self.try_destroy()
        self.aproximar()
