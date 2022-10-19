import pygame
import sys
import math
from . import display

TIRO_GROUP: pygame.sprite.Group
TIRO_TIMER = 0
TIRO_INTERVALO = 10
TIRO_RECT_LIST = []
TIRO_SPEED: int


class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load('sprites/tiro.png')
        self.rect = self.image.get_rect(center=(x, y))

        # ALTERAÇÕES
        # retorna largura e altura da imagem
        self.size = self.image.get_size()
        # ajusta tamanho do sprite
        self.image = pygame.transform.scale(self.image, (int(self.size[0] * 0.3), int(self.size[1] * 0.3)))
        ##############

    def update(self):
        self.rect.x += 10

        if self.rect.x > 2000:
            self.kill()