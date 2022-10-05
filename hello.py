import sys
import pygame
from pygame.locals import *

pygame.init()
# Define uma tela para o jogo
resolucao = ((500, 500))
tela = pygame.display.set_mode(resolucao)

while True:
    # Recebe os eventos do jogo
    for event in pygame.event.get():
        # Evento de sair do jogo
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    # Atualiza a tela a cada loop
    pygame.display.update()
