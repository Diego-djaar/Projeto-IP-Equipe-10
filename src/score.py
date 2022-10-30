from tkinter import S
import pygame
import math
from random import randint, choice
from . import display
from . import time


def display_score():
    # Mostra o score atual na tela
    current_time = int(pygame.time.get_ticks() / 1000) - time.START_TIME
    score_surf = display.FONT.render(f'Score: {current_time}', False, (200, 150, 200))
    score_rect = score_surf.get_rect(topleft=(50, 50))
    display.DISPLAY.blit(score_surf, score_rect)
    return current_time
