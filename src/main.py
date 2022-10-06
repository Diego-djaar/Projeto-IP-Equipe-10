import sys
import pygame
from pygame.locals import *
from astros import Sol, Planeta, Lua
from vetor import Vetor
from pygame.sprite import Group

pygame.init()
# Define uma tela para o jogo
resolucao = (1600, 900)
tela = pygame.display.set_mode(resolucao)


sol = Sol()
terra = Planeta(Vetor(400, 450), 'sprites/Terra.png', 50, Vetor(0, 0.36), 200)
lua = Lua(Vetor(335, 450), 'sprites/Lua.png', 20, Vetor(0, 0.78), 60)

planetas = Group(terra)
luas_da_terra = Group(lua)

# Marca a diferença de tempo
relogio = pygame.time.Clock()
dt = relogio.tick(75)

while True:
    # Recebe os eventos do jogo
    for event in pygame.event.get():
        # Evento de sair do jogo
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Chamar as funções para todos os sprites aplicáveis
    tela.fill((0, 0, 0))
    sol.update(tela, dt)
    planetas.update(tela, dt, [sol])
    luas_da_terra.update(tela, dt, [terra], terra)

    # Debug
    if True:
        for astro in [sol, lua, terra]:
            if astro.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(tela, (255, 255, 255), astro.rect, 5)

    # Determina a diferença de tempo do frame. Usado em velocidades
    dt = relogio.tick(75)

    # Atualiza a tela a cada loop
    pygame.display.update()
