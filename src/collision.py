import pygame

from . import player
from . import planet
from . import boosts


def collision_sprite():
    #global game_active
    if pygame.sprite.spritecollide(player.PLAYER.sprite, planet.PLANET_GROUP, False):
        planet.PLANET_GROUP.empty()
        player.GAME_ACTIVE = False
    # checa colisão entre o jogador e os boosts
    if pygame.sprite.spritecollideany(player.PLAYER.sprite, boosts.BOOST_GROUP):
        boost_types = pygame.sprite.spritecollide(player.PLAYER.sprite, boosts.BOOST_GROUP, True)
        for sprite in boost_types:
            if sprite.type == 'shield':
                boosts.NUM_BOOST[0] += 1
            elif sprite.type == 'speed':
                boosts.NUM_BOOST[1] += 1
