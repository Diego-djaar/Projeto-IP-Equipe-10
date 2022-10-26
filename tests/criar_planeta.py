import src.planet as planet
import src.display as display
import pygame


def criar_planeta_test():
    try:
        planeta_small = planet.Planet('small', 6)
        planeta_medio = planet.Planet('medium', 6)
        planetas_grupo = pygame.sprite.Group([planeta_small, planeta_medio])

        planetas_grupo.update(1)

        assert planeta_small.rect.x == display.DISPLAY_W*1.5 - 6, (planeta_small.rect.x, display.DISPLAY_W*1.5 - 6)
        assert planeta_medio.rect.x == display.DISPLAY_W*1.5 - (6 - 2), (planeta_medio.rect.x, display.DISPLAY_W*1.5 - 5)

    except Exception as error:
        return error
    return 'Success'
