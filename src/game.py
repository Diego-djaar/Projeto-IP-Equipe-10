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

    # ------
    # INICIALIZAÇÃO
    # ------

    # Display
    display.DISPLAY = pygame.display.set_mode((screen_w/1.2, screen_h/1.2))
    display.DISPLAY_W, display.DISPLAY_H = display.DISPLAY.get_size()
    pygame.display.set_caption('Alien rescue')
    display.FONT = pygame.font.Font(None, 30)

    # Variáveis de jogo
    player.GAME_ACTIVE = False
    boosts.BOOSTS_COLETADOS_DICT = dict(shield=0, speed=0)

    # Tempo
    clock = pygame.time.Clock()
    time.START_TIME = 0

    # Surfaces
    galaxy_surf = pygame.image.load('graphics/background/galaxy.png').convert()
    galaxy_surf = pygame.transform.rotozoom(galaxy_surf, 0, 0.8)

    # Planetas
    planet.PLANET_TIMER = pygame.USEREVENT + 1
    pygame.time.set_timer(planet.PLANET_TIMER, 3000)
    planet.PLANET_GROUP = pygame.sprite.Group()
    planet.PLANET_RECT_LIST = []

    # Boosts
    boosts.BOOST_TIMER = pygame.USEREVENT + 2
    pygame.time.set_timer(boosts.BOOST_TIMER, 15000)
    boosts.BOOST_GROUP = pygame.sprite.Group()
    boosts.BOOST_RECT_LIST = []

    # Velocidade dos objetos:
    planet.PLANET_SPEED = pygame.USEREVENT + 3
    pygame.time.set_timer(planet.PLANET_SPEED, 4000)
    planet_speed = 6
    boosts.BOOST_SPEED = pygame.USEREVENT + 4
    pygame.time.set_timer(boosts.BOOST_SPEED, 4000)
    boost_speed = 4

    # Player
    player.PLAYER_GROUP = pygame.sprite.GroupSingle()
    player.PLAYER_GROUP.add(player.Player())

    # ------
    # LOOP PRINCIPAL
    # ------

    while True:
        delta_tempo = clock.tick(100)*0.06

        for event in pygame.event.get():
            # Eventos
            player.PLAYER_GROUP.sprite.event_handler(event)

            if event.type == pygame.QUIT:
                # Sair do jogo
                pygame.quit()
                sys.exit()

            if player.GAME_ACTIVE:
                # Eventos com o jogo ativo
                if event.type == planet.PLANET_SPEED:
                    if planet_speed <= 20:
                        planet_speed += 0.5
                if event.type == boosts.BOOST_SPEED:
                    if boost_speed <= 20:
                        boost_speed += 0.5
                if event.type == planet.PLANET_TIMER:
                    # Criar um planeta de tipo aleatório
                    planet.PLANET_GROUP.add(
                        Planet(choice(['small', 'small', 'medium']), planet_speed))
                if event.type == boosts.BOOST_TIMER:
                    # Criar um boost aleatório
                    boosts.BOOST_GROUP.add(Boost(choice(['shield', 'speed']), boost_speed))
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # (Re)começar o jogo
                    player.GAME_ACTIVE = True
                    planet.PLANET_RECT_LIST.clear()
                    boosts.BOOST_RECT_LIST.clear()
                    boosts.BOOSTS_COLETADOS_DICT.clear()
                    player.PLAYER_GROUP.sprite.rect.y = display.DISPLAY_H*0.6
                    player.PLAYER_GROUP.sprite.gravity = 0
                    time.START_TIME = int(pygame.time.get_ticks() / 1000)

        # Desenha o fundo galáctico
        display.DISPLAY.blit(galaxy_surf, (0, 0))

        if player.GAME_ACTIVE:
            # Ações a cada frame no jogo ativo

            # Player
            player.PLAYER_GROUP.update(delta_tempo)
            player.PLAYER_GROUP.draw(display.DISPLAY)

            # Planets
            planet.PLANET_GROUP.update(delta_tempo)
            planet.PLANET_GROUP.draw(display.DISPLAY)

            # Boosts
            boosts.BOOST_GROUP.update(delta_tempo)
            boosts.BOOST_GROUP.draw(display.DISPLAY)

            # Score and text display
            display_score()
            display_boosts(boosts.BOOSTS_COLETADOS_DICT)

            collision_sprite()
        else:
            # Jogo inativo
            display.DISPLAY.fill('Purple')
            planet.PLANET_GROUP.empty()
            boosts.BOOST_GROUP.empty()

        pygame.display.update()


if __name__ == "__main__" or __name__ == "__game__":
    main()
