from typing import Tuple
import pygame
from pygame.locals import *
from vetor import Vetor


class Sprite:
    # Define um sprite base
    sprite: pygame.Surface
    rect: Rect
    posicao: Vetor

    def __init__(self, posicao: Vetor, imagem_arquivo: str, dimensoes: Tuple[float, float]):
        # Definir sprite dimensionado
        self.sprite = pygame.image.load(imagem_arquivo).convert_alpha()
        self.sprite = pygame.transform.smoothscale(
            self.sprite, (dimensoes[0], dimensoes[1]))
        # Definir rect com base no argumento da posição
        self.rect = self.sprite.get_rect()
        self.posicao = posicao
        self.rect.x = self.posicao.x
        self.rect.y = self.posicao.y

    def desenhar(self, tela: pygame.Surface):
        self.rect.x = self.posicao.x
        self.rect.y = self.posicao.y
        # Desenha o sprite na tela
        tela.blit(self.sprite, self.rect)
