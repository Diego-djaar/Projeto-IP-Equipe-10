from math import sqrt
from typing import Tuple
from pygame.locals import *
from sprite import Sprite
from vetor import Vetor

# constante_gravitacional
G = 0.05


class Planeta(Sprite):
    # Define um planeta qualquer
    velocidade: Vetor
    massa: float

    def __init__(self,  posicao: Vetor, imagem_arquivo: str, tamanho: float, velocidade: Vetor, massa: float):
        self.velocidade = velocidade
        self.massa = massa
        dimensoes = (tamanho, tamanho)
        super().__init__(posicao, imagem_arquivo, dimensoes)

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
