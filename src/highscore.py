import pygame
import math
from random import randint, choice
from . import display
from . import time


def display_hscore(hscore):
    # High Score
    score_surf = display.FONT.render(f'Highest Score: {hscore:0.0f}', False, (250, 150, 200))
    score_rect = score_surf.get_rect(center=(display.DISPLAY_W/2, display.DISPLAY_H/2))

    # Mensagem em tela
    text1 = display.FONT.render('Aperter a tecla "espaço" para continuar', True, (250, 150, 200))
    textdefault = text1.get_rect(center=(display.DISPLAY_W/2, display.DISPLAY_H/2+50))

    display.DISPLAY.blit(score_surf, score_rect)
    display.DISPLAY.blit(text1, textdefault)
