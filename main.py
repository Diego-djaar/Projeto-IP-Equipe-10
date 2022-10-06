import pygame
from pygame.locals import QUIT, KEYUP, KEYDOWN, K_SPACE
from pygame import event
from pygame import display
from pygame.image import load
from pygame.transform import scale
from pygame.sprite import Sprite, Group, GroupSingle

pygame.init()

# Sprite do personagem principal:
class Nave(Sprite):
    def __init__(self, escudo, velocidade, impacto, misseis):
        super().__init__()
        self.speed = 2
        self.misseis = misseis

        # Booleanas que representam os buffs (se existem ou não):
        self.escudo = escudo
        self.velocidade = velocidade
        self.impacto = impacto

        self.image = load('images/espaconave.png')
        self.rect = self.image.get_rect()

    def atirar(self):
        self.misseis.add(
            Bombas(*self.rect.center)
        )

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pygame.K_UP]:
            self.rect.y -= self.speed

        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

# Classe das bombas:
class Bombas(Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = load('images/missil.png')
        self.rect = self.image.get_rect(center=(x,y))

    def update(self):
        self.rect.x += 5

        if self.rect.x > resolucao[0]:
            self.kill()

# Definindo a tela:
resolucao = 1280, 720
tela = display.set_mode(resolucao)
display.set_caption('Alien Rescue')
background = scale(load('images/espaco3.jpeg'), resolucao)

# Nave espacial + mísseis:
grupo_misseis = Group()
nave = Nave(False, False, False, grupo_misseis)
grupo_nave = GroupSingle(nave)

# Loop do jogo:
while True:
    # Eventos:
    for evento in event.get():
        if evento.type == QUIT:
            pygame.quit()

        if evento.type == KEYUP:
            if evento.key == K_SPACE:
                nave.atirar()

    grupo_nave.draw(tela)
    grupo_nave.update()
    grupo_misseis.draw(tela)
    grupo_misseis.update()

    # Display e background:
    display.update()
    tela.blit(background, (0, 0))