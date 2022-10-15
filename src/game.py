import pygame
import sys
from random import randint, choice
from .planet import Planet
from .boosts import Boost, display_boosts
from .score import display_score
from .collision import collision_sprite
from . import player
from . import planet
from . import boosts
from . import display
from . import time


def main():
    pygame.init()

    screen_w, screen_h = pygame.display.Info().current_w, pygame.display.Info().current_h

    display.DISPLAY = pygame.display.set_mode((screen_w/1.2, screen_h/1.2))
    display.DISPLAY_W, display.DISPLAY_H = display.DISPLAY.get_size()

    pygame.display.set_caption('Allien rescue')
    clock = pygame.time.Clock()
    display.FONT = pygame.font.Font(None, 30)

    # ---------
    # VARIABLES
    # ---------
    player.GAME_ACTIVE = False
    time.START_TIME = 0  # angle = speed_var = 0
    boosts.NUM_BOOST = [0, 0]

    # -----
    # TIMER
    # -----
    planet.PLANET_TIMER = pygame.USEREVENT + 1
    pygame.time.set_timer(planet.PLANET_TIMER, 3000)

    boosts.BOOST_TIMER = pygame.USEREVENT + 2
    pygame.time.set_timer(boosts.BOOST_TIMER, 15000)

    # --------
    # SURFACES
    # --------
    galaxy_surf = pygame.image.load('graphics/background/galaxy.png').convert()
    galaxy_surf = pygame.transform.rotozoom(galaxy_surf, 0, 0.8)

    # ------
    # GROUPS
    # ------
    planet.PLANET_GROUP = pygame.sprite.Group()
    planet.PLANET_RECT_LIST = []

    boosts.BOOST_GROUP = pygame.sprite.Group()
    boosts.BOOST_RECT_LIST = []

    player.PLAYER = pygame.sprite.GroupSingle()
    player.PLAYER.add(player.Player())

    #x = display.DISPLAY_W*1.5
    #y = 100

    while True:
        for event in pygame.event.get():

            player.PLAYER.sprite.event_handler(event)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if player.GAME_ACTIVE:
                if event.type == planet.PLANET_TIMER:
                    planet.PLANET_GROUP.add(
                        Planet(choice(['small', 'small', 'medium'])))
                if event.type == boosts.BOOST_TIMER:
                    boosts.BOOST_GROUP.add(Boost(choice(['shield', 'speed'])))
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    player.GAME_ACTIVE = True
                    planet.PLANET_RECT_LIST.clear()
                    boosts.BOOST_RECT_LIST.clear()
                    player.PLAYER.sprite.rect.y = display.DISPLAY_H*0.6
                    player.PLAYER.sprite.gravity = 0  # speed_var = 0
                    time.START_TIME = int(pygame.time.get_ticks() / 1000)

        display.DISPLAY.blit(galaxy_surf, (0, 0))

        if player.GAME_ACTIVE:
            # Player
            player.PLAYER.draw(display.DISPLAY)
            player.PLAYER.update()

            # Planets
            planet.PLANET_GROUP.draw(display.DISPLAY)
            planet.PLANET_GROUP.update()

            # Boosts
            boosts.BOOST_GROUP.draw(display.DISPLAY)
            boosts.BOOST_GROUP.update()

            # Score and text display
            display_score()
            display_boosts(boosts.NUM_BOOST)

            collision_sprite()
        else:
            display.DISPLAY.fill('Purple')
            planet.PLANET_GROUP.empty()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__" or __name__ == "__game__":
    main()
