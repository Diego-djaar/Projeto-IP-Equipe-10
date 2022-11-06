import math
import sys
import pygame
from random import randint, uniform
from src import player
from . import display


BOOST_GROUP: pygame.sprite.Group
BOOSTS_COLETADOS_DICT: dict
SHIELD_IMAGE: dict = None
SPEED_IMAGE: dict = None
SLOW_IMAGE: dict = None
BOOST_SPEED_BASE = 4
BOOST_SPEED_ATUAL = 4
DESACELERAR = False
HYPERSPEED = False


class Boost(pygame.sprite.Sprite):
    def __init__(self, typo, speed):
        # Define boosts de cada tipo
        super().__init__()
        self.type = typo
        current_module = sys.modules[__name__]

        if self.type == 'shield':
            if current_module.SHIELD_IMAGE is None:
                current_module.SHIELD_IMAGE =\
                    dict(normal=pygame.image.load('graphics/boost/shield_0.png').convert_alpha(),
                         cinza=pygame.image.load('graphics_cinza/boost/shield_0.png').convert_alpha())
                current_module.SHIELD_IMAGE['normal'] = pygame.transform.rotozoom(current_module.SHIELD_IMAGE['normal'], 0, 1)
                current_module.SHIELD_IMAGE['cinza'] = pygame.transform.rotozoom(current_module.SHIELD_IMAGE['cinza'], 0, 1)

            self.image_dir = current_module.SHIELD_IMAGE
            self.image = self.image_dir[player.GAME_MODE]

        elif self.type == 'speed':
            if current_module.SPEED_IMAGE is None:
                current_module.SPEED_IMAGE =\
                    dict(normal=pygame.image.load('graphics/boost/speed_0.png').convert_alpha(),
                         cinza=pygame.image.load('graphics_cinza/boost/speed_0.png').convert_alpha())
                current_module.SPEED_IMAGE['normal'] = pygame.transform.rotozoom(current_module.SPEED_IMAGE['normal'], 0, 1)
                current_module.SPEED_IMAGE['cinza'] = pygame.transform.rotozoom(current_module.SPEED_IMAGE['cinza'], 0, 1)

            self.image_dir = current_module.SPEED_IMAGE
            self.image = self.image_dir[player.GAME_MODE]

        # Definindo boost de desacelerar o tempo:
        elif self.type == 'slow':
            if current_module.SLOW_IMAGE is None:
                current_module.SLOW_IMAGE =\
                    dict(normal=pygame.image.load('graphics/boost/slow_0.png').convert_alpha(),
                         cinza=pygame.image.load('graphics_cinza/boost/slow_0.png').convert_alpha())
                current_module.SLOW_IMAGE['normal'] = pygame.transform.rotozoom(current_module.SLOW_IMAGE['normal'], 0, 1)
                current_module.SLOW_IMAGE['cinza'] = pygame.transform.rotozoom(current_module.SLOW_IMAGE['cinza'], 0, 1)

            self.image_dir = current_module.SLOW_IMAGE
            self.image = self.image_dir[player.GAME_MODE]

        self.wave = randint(70, 100)
        self.rect = self.image.get_rect(midleft=(display.DISPLAY_W*1.5, uniform(display.DISPLAY_H*0.3, display.DISPLAY_H*0.7)))
        # Angulo entre 0 e 2pi
        self.angle = uniform(0, 6.2831)
        self.speed = speed
        self.height = uniform(display.DISPLAY_H*0.3, display.DISPLAY_H*0.7)

    def movement(self, delta_tempo: float):
        # Movimento ondulatório
        self.rect.x -= self.speed*delta_tempo
        self.rect.y = self.wave*math.sin(self.angle)+self.height
        self.angle += 0.03*delta_tempo

    def try_destroy(self):
        # Destruir ao sair da tela
        if self.rect.x < -1000:
            self.kill()

    def update(self, delta_tempo: float):
        self.movement(delta_tempo)
        self.try_destroy()


def display_boosts(boosts_dict: dict):
    # Mostrar os boosts coletados de cada tipo na tela
    index = 0
    for boost in boosts_dict:
        boosts_surf = display.FONT.render(f'{boost}: {boosts_dict[boost]}', False, (250, 200, 250))
        boosts_rect = boosts_surf.get_rect(center=(display.DISPLAY_W-120, 50*index+50))
        display.DISPLAY.blit(boosts_surf, boosts_rect)
        index += 1
