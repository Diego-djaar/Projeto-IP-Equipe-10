import sys
import time
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
import jogo
import nave


pygame.init()

# Define uma tela para o jogo
resolucao = (1600, 900)
tela = pygame.display.set_mode(resolucao)
display.set_caption('Alien Rescue')
background = scale(load('images/espaco3.jpeg'), resolucao)


# Carregar globais porém só após inicializar o pygame
nave.EXPLOSAO_IMAGEM = pygame.image.load(
    'sprites/explosao.png').convert_alpha()

# Nave espacial + mísseis:
grupo_misseis = Group()
jogador_nave = Nave(False, False, False, grupo_misseis)
grupo_nave = Group(jogador_nave)


sol = Sol()
terra = Planeta(Vetor(400, 450), 'sprites/Terra.png', 50, Vetor(0, 0.36), 200)
lua = Lua(Vetor(335, 450), 'sprites/Lua.png', 20, Vetor(0, 0.78), 60)

planetas = Group(terra)
luas_da_terra = Group(lua)
astros.lista_de_astros = [sol, terra, lua]

# Marca a diferença de tempo
relogio = pygame.time.Clock()
dt = relogio.tick(75)
tempo_game_over = 200

while True:
    # Recebe os eventos do jogo
    for event in pygame.event.get():
        # Evento de sair do jogo
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == K_SPACE:
                for todos in grupo_nave:
                    todos.atirar()

    # Chamar as funções para todos os sprites aplicáveis
    tela.blit(background, (0, 0))
    sol.update(tela, dt)
    planetas.update(tela, dt, [sol])
    luas_da_terra.update(tela, dt, [terra], terra)

    grupo_nave.update(tela, dt)
    grupo_misseis.update(tela, dt)

    # Debug
    if True:
        for astro in [sol, lua, terra, jogador_nave]:
            if astro.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(tela, (255, 255, 255), astro.rect, 5)

    # Determina a diferença de tempo do frame. Usado em velocidades
    dt = relogio.tick(75)

    # Atualiza a tela a cada loop
    pygame.display.update()

    # Game Over
    if jogo.GAME_OVER == True:
        tempo_game_over -= dt
        if tempo_game_over < 0:
            # TODO: animação de game over
            pygame.quit()
            sys.exit()
