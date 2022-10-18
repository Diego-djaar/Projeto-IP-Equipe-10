import pygame
from . import player
from . import planet
from . import boosts


def collision_sprite():
    # Detectar colisão entre jogador e planetas
    if pygame.sprite.spritecollide(player.PLAYER_GROUP.sprite, planet.PLANET_GROUP, False):
        planet.PLANET_GROUP.empty()
        player.GAME_ACTIVE = False

    # Detectar colisão entre jogador e os boosts
    if pygame.sprite.spritecollideany(player.PLAYER_GROUP.sprite, boosts.BOOST_GROUP):
        boost_types = pygame.sprite.spritecollide(player.PLAYER_GROUP.sprite, boosts.BOOST_GROUP, True)
        for sprite in boost_types:
            if sprite.type in boosts.BOOSTS_COLETADOS_DICT:
                boosts.BOOSTS_COLETADOS_DICT[sprite.type] += 1
            else:
                boosts.BOOSTS_COLETADOS_DICT[sprite.type] = 1
