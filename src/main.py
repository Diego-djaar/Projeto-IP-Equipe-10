import sys
import pygame
from pygame.locals import *
from astros import Sol, Planeta, Lua
from vetor import Vetor
from pygame.sprite import Group
import pygame
from nave import Nave
from pygame.locals import QUIT, KEYUP, KEYDOWN, K_SPACE
from pygame import event
from pygame import display
from pygame.image import load
from pygame.transform import scale
from pygame.sprite import Sprite, Group, GroupSingle
import astros


pygame.init()
# Define uma tela para o jogo
resolucao = (1600, 900)
tela = pygame.display.set_mode(resolucao)
display.set_caption('Alien Rescue')
background = scale(load('images/espaco3.jpeg'), resolucao)

# Nave espacial + mísseis:
grupo_misseis = Group()
nave = Nave(False, False, False, grupo_misseis)
grupo_nave = GroupSingle(nave)


sol = Sol()
terra = Planeta(Vetor(400, 450), 'sprites/Terra.png', 50, Vetor(0, 0.36), 200)
lua = Lua(Vetor(335, 450), 'sprites/Lua.png', 20, Vetor(0, 0.78), 60)

planetas = Group(terra)
luas_da_terra = Group(lua)
astros.lista_de_astros = [sol, terra, lua]

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
        if event.type == KEYUP:
            if event.key == K_SPACE:
                nave.atirar()

    # Chamar as funções para todos os sprites aplicáveis
    tela.blit(background, (0, 0))
    sol.update(tela, dt)
    planetas.update(tela, dt, [sol])
    luas_da_terra.update(tela, dt, [terra], terra)

    grupo_nave.update(None, dt)
    grupo_nave.draw(tela)
    grupo_misseis.update(None, dt)
    grupo_misseis.draw(tela)

    # Debug
    if True:
        for astro in [sol, lua, terra]:
            if astro.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(tela, (255, 255, 255), astro.rect, 5)

    # Determina a diferença de tempo do frame. Usado em velocidades
    dt = relogio.tick(75)

    # Atualiza a tela a cada loop
    pygame.display.update()
