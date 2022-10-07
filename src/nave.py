from email.headerregistry import Group
from typing import List
import pygame
from pygame.locals import QUIT, KEYUP, KEYDOWN, K_SPACE
from pygame import event
from pygame import display
from pygame.image import load
from pygame.sprite import Sprite
from astros import Planeta
from objeto import Objeto
from vetor import Vetor
import astros


class Nave(Objeto):
    speed: int
    escudo: bool
    velocidade: bool
    impacto: bool
    misseis: Group

    # Sprite do personagem principal:
    def __init__(self, escudo, velocidade, impacto, misseis):
        super().__init__(Vetor(0, 0), 'images/espaconave.png', (80, 80))
        self.speed = 2
        self.misseis = misseis

        # Booleanas que representam os buffs (se existem ou não):
        self.escudo = escudo
        self.velocidade = velocidade
        self.impacto = impacto

    def atirar(self):
        # Atira uma bomba
        self.misseis.add(
            Bombas(*self.rect.center)
        )

    def update(self):
        # Movimentação da nave
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pygame.K_UP]:
            self.rect.y -= self.speed

        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed


class Bombas(Planeta):
    # Classe das bombas:
    def __init__(self, x, y):
        # posicao: Vetor, imagem_arquivo: str, tamanho: float, velocidade: Vetor, massa: float
        super().__init__(Vetor(x, y), 'images/missil.png', 20, Vetor(0.5, 0), 0)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, tela: pygame.Surface, dt: float):
        if abs(self.rect.x) > 1600 or abs(self.rect.y) > 900:
            self.kill()
        super().update(tela, dt, astros.lista_de_astros)
