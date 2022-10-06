from typing import Tuple
from pygame.locals import *
from sprite import Sprite
from vetor import Vetor


class Planeta(Sprite):
    # Define um planeta qualquer
    velocidade: Vetor

    def __init__(self,  posicao: Tuple[float, float], imagem_arquivo: str, tamanho: float, velocidade: Vetor):
        self.velocidade = velocidade
        dimensoes = (tamanho, tamanho)
        super().__init__(posicao, imagem_arquivo, dimensoes)

    def movimento(self, dt: float):
        # Movimentação com base na velocidade: velocidade * dTempo
        self.rect.x += self.velocidade.x*dt
        self.rect.y += self.velocidade.y*dt


class Sol(Planeta):
    # Define o Sol no centro do mapa
    imagem_arquivo = 'sprites/Sol.png'
    posicao = (450, 450)
    tamanho = 100
    velocidade: Vetor = Vetor(0, 0)

    def __init__(self):
        super().__init__(self.posicao, self.imagem_arquivo, self.tamanho, self.velocidade)
