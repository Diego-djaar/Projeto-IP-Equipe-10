import pygame
import sys
from random import randint, choice
from . import eventos
from .planet import Planet
from . import boosts
from .score import display_score
from .collision import collision_group_group, collision_sprite_group
from .tiro import Tiro
from . import player
from . import planet
from . import display
from . import time
from . import argumentos
from . import tiro
from . import asteroide


def main():
    # ------
    # INICIALIZAÇÃO
    # ------

    pygame.init()

    # Eventos
    eventos.EVENTOS_LISTA = []

    # Display
    screen_w, screen_h = pygame.display.Info().current_w, pygame.display.Info().current_h
    display.DISPLAY = pygame.display.set_mode((screen_w/1.2, screen_h/1.2))
    display.DISPLAY_W, display.DISPLAY_H = display.DISPLAY.get_size()
    pygame.display.set_caption('Alien rescue')
    display.FONT = pygame.font.Font(None, 30)

    # Variáveis de jogo
    player.GAME_MODE = 'normal'
    player.GAME_ACTIVE = False
    boosts.BOOSTS_COLETADOS_DICT = dict(shield=0, speed=0, slow=0)
    boosts.DESACELERAR = False

    # Tempo
    time.CLOCK = pygame.time.Clock()
    time.START_TIME = 0

    # Fundo
    display.GALAXY_SURF = dict()
    display.GALAXY_SURF['normal'] = pygame.image.load('graphics/background/galaxy.png').convert()
    display.GALAXY_SURF['normal'] = pygame.transform.rotozoom(display.GALAXY_SURF['normal'], 0, 0.8)

    display.GALAXY_SURF['cinza'] = pygame.image.load('graphics_cinza/background/galaxy.png').convert()
    display.GALAXY_SURF['cinza'] = pygame.transform.rotozoom(display.GALAXY_SURF['cinza'], 0, 0.8)

    # Planetas
    eventos.EVENTOS_LISTA.append(eventos.Evento('criar planeta', 100, 300, 0))
    eventos.EVENTOS_LISTA.append(eventos.Evento('criar planeta', 300, 500, 0))
    planet.PLANET_GROUP = pygame.sprite.Group()

    # Asteroides
    eventos.EVENTOS_LISTA.append(eventos.Evento('criar asteroide', 80, 200, 100))
    asteroide.ASTEROIDE_GROUP = pygame.sprite.Group()

    # Boosts
    eventos.EVENTOS_LISTA.append(eventos.Evento('criar boost', 500, 700, 700))
    boosts.BOOST_GROUP = pygame.sprite.Group()

    # Velocidade dos objetos
    eventos.EVENTOS_LISTA.append(eventos.Evento('planeta velocidade', 400, 400, 400))
    planet.PLANET_SPEED_ATUAL = planet.PLANET_SPEED_BASE

    eventos.EVENTOS_LISTA.append(eventos.Evento('boost velocidade', 400, 400, 400))
    boosts.BOOST_SPEED_ATUAL = boosts.BOOST_SPEED_BASE

    # Player
    player.PLAYER_GROUP = pygame.sprite.GroupSingle()
    player.PLAYER_GROUP.add(player.Player())

    # Tiros
    tiro.TIRO_GROUP = pygame.sprite.Group()
    tiro.TIRO_SPEED = pygame.USEREVENT + 6
    pygame.time.set_timer(tiro.TIRO_SPEED, 4000)
    tiro.TIRO_RECT_LIST = []

    # Boost de slow:
    slow_cancel = pygame.USEREVENT + 7

    if argumentos.DEBUG:
        mouse_pos = pygame.sprite.Sprite()
        mouse_pos.image = pygame.image.load('./graphics/planet/planet_1.png').convert_alpha()
        mouse_pos.rect = pygame.Rect(0, 0, 5, 5)
        mouse_pos.image = pygame.transform.scale(mouse_pos.image, (mouse_pos.rect.height, mouse_pos.rect.width))
        mouse_pos_g = pygame.sprite.GroupSingle(mouse_pos)

    # ------
    # LOOP PRINCIPAL
    # ------

    while True:
        if not boosts.DESACELERAR:
            delta_tempo = time.CLOCK.tick(100)*0.06
        else:
            delta_tempo = time.CLOCK.tick(100)*0.03

        # ------
        # EVENTOS PYGAME
        # ------

        for event in pygame.event.get():
            player.PLAYER_GROUP.sprite.event_handler(event, delta_tempo)

            if event.type == pygame.QUIT:
                # Sair do jogo
                pygame.quit()
                sys.exit()

            # Ativar o boost do slow:
            if pygame.key.get_pressed()[pygame.K_c] and boosts.BOOSTS_COLETADOS_DICT["slow"] > 0 and not boosts.DESACELERAR:
                boosts.BOOSTS_COLETADOS_DICT['slow'] -= 1
                boosts.DESACELERAR = True

                # Alterar imagens dos boosts
                for boost in boosts.BOOST_GROUP:
                    boost.image = boost.image_dir['cinza']

                # Alterar imagens dos planetas
                for planeta in planet.PLANET_GROUP:
                    planeta.image = planeta.image_dir['cinza']

                pygame.time.set_timer(slow_cancel, 5000)

            # Cancelar slow:
            if event.type == slow_cancel:
                # Alterar imagens dos boosts
                for boost in boosts.BOOST_GROUP:
                    boost.image = boost.image_dir['normal']

                # Alterar imagens dos planetas
                for planeta in planet.PLANET_GROUP:
                    planeta.image = planeta.image_dir['normal']

                pygame.time.set_timer(slow_cancel, 0)
                boosts.DESACELERAR = False

            if not player.GAME_ACTIVE:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # (Re)começar o jogo
                    player.GAME_ACTIVE = True
                    # Reiniciar variáveis
                    boosts.BOOSTS_COLETADOS_DICT = dict(shield=0, speed=0, slow=0)
                    player.PLAYER_GROUP.sprite.rect.y = display.DISPLAY_H*0.6
                    player.PLAYER_GROUP.sprite.gravity = 0
                    time.START_TIME = int(pygame.time.get_ticks() / 1000)

        # ------
        # EVENTOS DEFINIDOS
        # ------

        for evento in eventos.EVENTOS_LISTA:
            evento_tipo = evento.coletar()

            if player.GAME_ACTIVE:
                # Eventos com o jogo ativo

                # Aceleração dos planetas e boosts
                if evento_tipo == 'planeta velocidade':
                    if planet.PLANET_SPEED_ATUAL <= 20:
                        planet.PLANET_SPEED_ATUAL += 0.5

                if evento_tipo == 'boost velocidade':
                    if boosts.BOOST_SPEED_ATUAL <= 20:
                        boosts.BOOST_SPEED_ATUAL += 0.5

                if evento_tipo == 'criar planeta':
                    # Criar um planeta de tipo aleatório
                    planet.PLANET_GROUP.add(
                        Planet(choice(['small', 'small', 'medium']), planet.PLANET_SPEED_ATUAL))

                if evento_tipo == 'criar boost':
                    # Criar um boost aleatório
                    boosts.BOOST_GROUP.add(boosts.Boost(choice(['shield', 'speed', 'slow']), boosts.BOOST_SPEED_ATUAL))

                if evento_tipo == 'criar asteroide':
                    # Criar um asteroide
                    asteroide.ASTEROIDE_GROUP.add(asteroide.Asteroide('small', asteroide.ASTEROIDE_SPEED_ATUAL))

        if player.GAME_ACTIVE:
            # Ações a cada frame no jogo ativo

            # Tornar tela cinza se boost de slow.
            if boosts.DESACELERAR:
                player.GAME_MODE = 'cinza'
            else:
                player.GAME_MODE = 'normal'

            # Desenha o fundo galáctico
            display.DISPLAY.blit(display.GALAXY_SURF[player.GAME_MODE], (0, 0))

            # Atualizar eventos
            for evento in eventos.EVENTOS_LISTA:
                evento.update(delta_tempo)

            # Player
            player.PLAYER_GROUP.update(delta_tempo)
            player.PLAYER_GROUP.draw(display.DISPLAY)

            # Planets
            planet.PLANET_GROUP.update(delta_tempo)
            planet.PLANET_GROUP.draw(display.DISPLAY)

            # Asteroides
            asteroide.ASTEROIDE_GROUP.update(delta_tempo)
            asteroide.ASTEROIDE_GROUP.draw(display.DISPLAY)

            # Boosts
            boosts.BOOST_GROUP.update(delta_tempo)
            boosts.BOOST_GROUP.draw(display.DISPLAY)

            # Display (score e boosts)
            display_score()
            boosts.display_boosts(boosts.BOOSTS_COLETADOS_DICT)

            # Tiros
            tiro.TIRO_GROUP.update()
            tiro.TIRO_GROUP.draw(display.DISPLAY)

            # Colisões entre tiro e planetas
            for (tiros, _) in collision_group_group(tiro.TIRO_GROUP, planet.PLANET_GROUP):
                tiros.kill()

            # Colisões entre tiro e asteroides
            for (tiros, asteroides) in collision_group_group(tiro.TIRO_GROUP, asteroide.ASTEROIDE_GROUP):
                tiros.kill()
                asteroides.kill()

            # Detectar colisão entre jogador e algum planeta
            if collision_sprite_group(player.PLAYER_GROUP.sprite, planet.PLANET_GROUP)\
                    and player.PROTEGIDO is False:
                # Bater num planeta qualquer
                player.GAME_ACTIVE = False

            # Detectar colisão entre jogador e algum asteroide
            if collision_sprite_group(player.PLAYER_GROUP.sprite, asteroide.ASTEROIDE_GROUP)\
                    and player.PROTEGIDO is False:
                # Bater num asteroide qualquer
                player.GAME_ACTIVE = False

            # Colisões entre jogador e os boosts
            for boost in collision_sprite_group(player.PLAYER_GROUP.sprite, boosts.BOOST_GROUP):
                boosts.BOOSTS_COLETADOS_DICT[boost.type] += 1
                boost.kill()
        else:
            # Jogo inativo
            display.DISPLAY.fill('Purple')
            planet.PLANET_GROUP.empty()
            boosts.BOOST_GROUP.empty()
            tiro.TIRO_GROUP.empty()
            asteroide.ASTEROIDE_GROUP.empty()

            # Reset da velocidade dos objetos:
            boosts.BOOST_SPEED_ATUAL = boosts.BOOST_SPEED_BASE
            planet.PLANET_SPEED_ATUAL = planet.PLANET_SPEED_BASE

        # Debug
        if argumentos.DEBUG:
            from itertools import chain
            mouse_pos.rect.center = pygame.mouse.get_pos()
            # mouse_pos_g.draw(display.DISPLAY)
            for sprite in chain(planet.PLANET_GROUP, player.PLAYER_GROUP, boosts.BOOST_GROUP, tiro.TIRO_GROUP):
                if pygame.sprite.spritecollide(sprite, mouse_pos_g, False, pygame.sprite.collide_mask):
                    pygame.draw.rect(display.DISPLAY, (255, 255, 255), sprite.rect, 5)

        pygame.display.update()

        display.DISPLAY.unlock()


if __name__ == "__main__" or __name__ == "__game__":
    main()
