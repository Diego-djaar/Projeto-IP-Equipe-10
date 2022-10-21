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
