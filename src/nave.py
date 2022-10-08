from email.headerregistry import Group
from typing import List
import pygame
from pygame.locals import QUIT, KEYUP, KEYDOWN, K_SPACE
from pygame import Rect, Surface, event
from pygame import display
from pygame.image import load
from pygame.sprite import Sprite
from astros import Planeta
from objeto import Objeto
from vetor import Vetor
import astros
import jogo

EXPLOSAO_IMAGEM: Surface


class Nave(Objeto):
    explosao_imagem: Surface
    velocidade: int
    escudo: bool
    velocidade_buff: bool
    impacto: bool
    misseis: Group
    dimensoes = (80, 80)
    morto = False

    # Sprite do personagem principal:
    def __init__(self, escudo, velocidade, impacto, misseis):
        super().__init__(Vetor(0, 0), 'images/espaconave.png', self.dimensoes)
        self.velocidade = 0.2
        self.misseis = misseis
        self.explosao_imagem = EXPLOSAO_IMAGEM

        # Booleanas que representam os buffs (se existem ou não):
        self.escudo = escudo
        self.velocidade_buff = velocidade
        self.impacto = impacto

    def atirar(self):
        if not self.morto:
            # Atira uma bomba
            self.misseis.add(
                Bombas(*self.rect.center)
            )

    def update(self, tela: pygame.Surface, dt: float):
        # Movimentação da nave
        if not self.morto:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                self.posicao.x -= self.velocidade*dt

            if keys[pygame.K_RIGHT]:
                self.posicao.x += self.velocidade*dt

            if keys[pygame.K_UP]:
                self.posicao.y -= self.velocidade*dt

            if keys[pygame.K_DOWN]:
                self.posicao.y += self.velocidade*dt

            for missil in self.misseis:
                self.colisao(missil)
            for astro in astros.lista_de_astros:
                self.colisao(astro)

        super().update(tela)

    def colisao(self, outro):
        # Se colidiria com uma bomba ou tipo derivado de bomba
        if issubclass(type(outro), Bombas):
            ativacao = outro.ativacao
            outro.colisao(self)
        # Se colidiria com um planeta ou tipo derivado
        elif issubclass(type(outro), Planeta):
            ativacao = True
        # Se colidiria com tipo não especificado
        else:
            print(f'colidiu com {type(outro)}')
            ativacao = False

        if self.rect.colliderect(outro.rect) and ativacao:
            # TODO: código para receber dano
            self.image = self.explosao_imagem
            self.image = pygame.transform.smoothscale(
                self.image, self.dimensoes)
            self.morto = True
            jogo.GAME_OVER = True


class Bombas(Planeta):
    explosao_imagem: Surface
    # Classe das bombas:
    ativacao: bool = False
    tempo_ativacao = 210
    explodiu = False
    tempo_explosao = 150
    tamanho = 20
    velocidade_inicial = Vetor(0.5, 0)

    def __init__(self, x, y):
        self.explosao_imagem = EXPLOSAO_IMAGEM
        super().__init__(Vetor(x, y), 'images/missil.png',
                         self.tamanho, self.velocidade_inicial, 0)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, tela: pygame.Surface, dt: float):

        if self.explodiu:
            # Deixar a explosão na tela por um tempo
            self.velocidade = Vetor(0, 0)
            self.tempo_explosao -= dt
            if self.tempo_explosao < 0:
                self.kill()

        # Não ativar imediatamente quando lançada
        if self.tempo_ativacao > 0:
            self.tempo_ativacao -= dt
        else:
            self.ativacao = True

        if abs(self.rect.x) > 3000 or abs(self.rect.y) > 2200:
            self.kill()
        for astro in astros.lista_de_astros:
            self.colisao(astro)
        super().update(tela, dt, astros.lista_de_astros)

    def colisao(self, outro: Planeta):
        if not self.explodiu and self.ativacao:
            # Não adianta colidir se já explodiu
            if self.rect.colliderect(outro.rect):
                self.explodiu = True
                self.velocidade = Vetor(0, 0)
                self.image = self.explosao_imagem
                self.image = pygame.transform.smoothscale(
                    self.image, (self.tamanho, self.tamanho))
                return True
