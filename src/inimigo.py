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
        self.interromper = False

    def check_collision(self):
        if len(collision.collision_sprite_group(self, tiro.TIRO_GROUP)) > 0:


    def hora_morte(self):
        hora_apagar_inimigo = pygame.time.get_ticks() + 300
        return hora_apagar_inimigo

    def aproximar(self):
        if self.rect.y < player.PLAYER_GROUP.sprite.rect.y:
            self.rect.y += 2
        elif self.rect.y > player.PLAYER_GROUP.sprite.rect.y:
            self.rect.y -= 2

    def explodir(self):
        self.image = self.animacao[1]
        self.image = pygame.transform.rotozoom(self.image, 0, 0.5)

    def try_destroy(self):
        if self.rect.x < -1000:
            self.kill()
        elif self.check_collision() and self.interromper = False:


    def movement(self, delta_tempo: float):
        self.rect.x -= self.speed*delta_tempo

    def update(self, delta_tempo: float):
        self.movement(delta_tempo)
        self.try_destroy()
        self.aproximar()
        self.check_collision()
