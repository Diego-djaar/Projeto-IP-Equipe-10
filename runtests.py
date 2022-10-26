import tests.criar_planeta
import src.display as display
import pygame
import traceback


def parse(value: Exception | str):
    if type(value) is str:
        res = value
    else:
        res = f'Error:\n {"".join(traceback.format_tb(value.__traceback__))} {value}'
    return res


pygame.init()
screen_w, screen_h = pygame.display.Info().current_w, pygame.display.Info().current_h
display.DISPLAY = pygame.display.set_mode((screen_w/1.2, screen_h/1.2))
display.DISPLAY_W, display.DISPLAY_H = display.DISPLAY.get_size()
pygame.display.set_caption('Alien rescue')
display.FONT = pygame.font.Font(None, 30)

# Testes
print(f'criar planeta test {parse(tests.criar_planeta.criar_planeta_test())}')
