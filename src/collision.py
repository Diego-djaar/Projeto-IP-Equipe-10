import pygame
from pygame import sprite
from pygame.sprite import Sprite
from . import player
from . import planet
from . import boosts


def collision_sprite(sprite_origem: Sprite, grupo: sprite.Group):
    # Detectar colisão entre um sprite e um grupo de sprites
    if pygame.sprite.spritecollide(sprite_origem, grupo, False, pygame.sprite.collide_mask):
        return True

    return False


def collision_group(grupo_origem: sprite.Group, grupo_destino: sprite.Group, action):
    # Detectar colisão entre um grupo de sprites e outro grupo. Executar código para cada sprite de acordo
    for objeto in grupo_origem:
        if pygame.sprite.spritecollide(objeto, grupo_destino, False, pygame.sprite.collide_mask):
            action(objeto)
