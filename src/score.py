import pygame
import sys
import math
from random import randint, choice
from . import display
from . import time

SCORE: int = 0


def display_score():
    # Mostra o score atual na tela
    current_module = sys.modules[__name__]
    current_time = current_module.SCORE
    score_surf = display.FONT.render(f'Score: {current_time:0.0f}', False, (200, 150, 200))
    score_rect = score_surf.get_rect(topleft=(50, 50))
    display.DISPLAY.blit(score_surf, score_rect)
    return current_time
