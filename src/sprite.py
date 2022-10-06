from typing import Tuple
import pygame
from pygame.locals import *


class Sprite:
    # Define um sprite base
    sprite: pygame.Surface
    rect: Rect

    def __init__(self, posicao: Tuple[float, float], imagem_arquivo: str, dimensoes: Tuple[float, float]):
        # Definir sprite dimensionado
        self.sprite = pygame.image.load(imagem_arquivo).convert_alpha()
        self.sprite = pygame.transform.smoothscale(
            self.sprite, (dimensoes[0], dimensoes[1]))
        # Definir rect com base no argumento da posição
        self.rect = self.sprite.get_rect()
        self.rect.x = posicao[0]
        self.rect.y = posicao[1]

    def desenhar(self, tela: pygame.Surface):
        # Desenha o sprite na tela
        tela.blit(self.sprite, self.rect)
