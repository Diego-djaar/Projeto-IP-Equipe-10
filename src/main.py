import sys
import pygame
from pygame.locals import *
from astros import Sol, Planeta
from vetor import Vetor

pygame.init()
# Define uma tela para o jogo
resolucao = (1000, 1000)
tela = pygame.display.set_mode(resolucao)


sol = Sol()
sol.velocidade.x = 0.2
terra = Planeta((40, 70), 'sprites/Terra.png', 50, Vetor(0.3, 0.1))

# Marca a diferença de tempo
relogio = pygame.time.Clock()
dt = 0

while True:
    # Recebe os eventos do jogo
    for event in pygame.event.get():
        # Evento de sair do jogo
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Chamar as funções para todos os sprites aplicáveis
    tela.fill((0, 0, 0))
    sol.movimento(dt)
    sol.desenhar(tela)
    terra.movimento(dt)
    terra.desenhar(tela)

    # Determina a diferença de tempo do frame. Usado em velocidades
    dt = relogio.tick(75)

    # Atualiza a tela a cada loop
    pygame.display.update()
