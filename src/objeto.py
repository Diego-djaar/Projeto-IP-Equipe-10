from typing import Tuple
import pygame
from pygame.locals import *
from vetor import Vetor
from pygame.sprite import Sprite


class Objeto(Sprite):
    # Define um objeto base
    rect: Rect
    posicao: Vetor

    def __init__(self, posicao: Vetor, imagem_arquivo: str, dimensoes: Tuple[float, float]):
        super().__init__()
        # Definir sprite dimensionado
        self.image = pygame.image.load(imagem_arquivo).convert_alpha()
        self.image = pygame.transform.smoothscale(
            self.image, dimensoes)
        # Definir rect com base no argumento da posição
        self.rect = self.image.get_rect()
        self.posicao = posicao
        self.rect.x = self.posicao.x
        self.rect.y = self.posicao.y

    def update(self, tela: pygame.Surface) -> None:
        self.desenhar(tela)
        return super().update()

    def desenhar(self, tela: pygame.Surface = None):
        # Desenha o objeto na tela
        self.rect.x = self.posicao.x
        self.rect.y = self.posicao.y
        if tela is not None:
            tela.blit(self.image, self.rect)
