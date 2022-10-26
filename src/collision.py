from typing import List, Tuple
import pygame
from pygame import sprite
from pygame.sprite import Sprite
from . import player
from . import planet
from . import boosts


def collision_sprite_group(sprite_origem: Sprite, grupo: sprite.Group):
    # Detectar colisões entre um sprite e um grupo de sprites.
    # Retornar colisões detectadas
    colisoes: List[Sprite] = pygame.sprite.spritecollide(sprite_origem, grupo, False, pygame.sprite.collide_mask)
    return colisoes


def collision_group_group(grupo_origem: sprite.Group, grupo_destino: sprite.Group):
    # Detectar colisões entre um grupo de sprites e outro grupo.
    # Retornar todas as colisões detectadas, 1 para 1
    colisoes: List[Tuple[Sprite, Sprite]] = []
    for objeto in grupo_origem:
        for outro in pygame.sprite.spritecollide(objeto, grupo_destino, False, pygame.sprite.collide_mask):
            colisoes.append((objeto, outro))

    return colisoes
