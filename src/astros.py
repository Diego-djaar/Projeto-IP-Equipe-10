import pygame
from math import sqrt
from typing import List, Tuple
from pygame.locals import *
from objeto import Objeto
from vetor import Vetor

# constante_gravitacional
G = 0.05


class Planeta(Objeto):
    # Define um planeta qualquer
    delta_velocidade = Vetor(0, 0)
    velocidade: Vetor
    massa: float

    def __init__(self,  posicao: Vetor, imagem_arquivo: str, tamanho: float, velocidade: Vetor, massa: float):
        self.velocidade = velocidade
        self.massa = massa
        dimensoes = (tamanho, tamanho)
        super().__init__(posicao, imagem_arquivo, dimensoes)

    def update(self, tela: pygame.Surface, dt: float, atracao_gravitacional: list = None) -> None:
        # Guardar a diferença de velocidade até o próximo update
        self.delta_velocidade = Vetor(0, 0)
        self.movimento(dt)
        if atracao_gravitacional is not None:
            for planeta in atracao_gravitacional:
                self.gravitacao(planeta, dt)
        return super().update(tela)

    def movimento(self, dt: float):
        # Movimentação com base na velocidade: velocidade * dTempo
        self.posicao.x += self.velocidade.x*dt
        self.posicao.y += self.velocidade.y*dt

    def gravitacao(self, outro, dt: float):
        # Vetor entre as posições dos planetas
        vetor = Vetor(outro.posicao.x-self.posicao.x,
                      outro.posicao.y-self.posicao.y)

        # Calculo da força gravitacional
        distancia_quadrado = vetor.modulo_quadrado()
        direcao = vetor.multiplicar_escalar(1/sqrt(distancia_quadrado))

        # Fórmula: dv = G.m2.dt/d^2
        dv = (G*outro.massa*dt)/distancia_quadrado
        # Velocidade vetorial
        dvel = Vetor.multiplicar_escalar(direcao, dv)
        # Somar dv à velocidade
        self.delta_velocidade = Vetor.soma_vetores(self.delta_velocidade, dvel)
        self.velocidade = Vetor.soma_vetores(self.velocidade, dvel)


class Sol(Planeta):
    # Define o Sol no centro do mapa
    imagem_arquivo = 'sprites/Sol.png'
    posicao = Vetor(750, 400)
    tamanho = 100
    velocidade: Vetor = Vetor(0, 0)
    massa = 1000

    def __init__(self):
        super().__init__(self.posicao, self.imagem_arquivo,
                         self.tamanho, self.velocidade, self.massa)


class Lua(Planeta):
    # Satélite natural
    def __init__(self, posicao: Vetor, imagem_arquivo: str, tamanho: float, velocidade: Vetor, massa: float):
        super().__init__(posicao, imagem_arquivo, tamanho, velocidade, massa)

    def update(self, tela: pygame.Surface, dt: float, atracao_gravitacional: list = None, orbita: Planeta = None) -> None:
        update = super().update(tela, dt, atracao_gravitacional)
        if orbita is not None:
            self.orbita(orbita)
        return update

    def orbita(self, primario: Planeta):
        # Manter a Lua presa a um determinado Planeta, ao aplicar a mesma aceleracao
        self.delta_velocidade = Vetor.soma_vetores(
            self.delta_velocidade, primario.delta_velocidade)
        self.velocidade = Vetor.soma_vetores(
            self.velocidade, primario.delta_velocidade)
