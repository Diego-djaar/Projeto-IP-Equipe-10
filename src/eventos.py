# usar isso ao invés de pygame.USEREVENT

from random import uniform
from typing import List, Tuple


class Evento:
    nome: str
    recarga_total_max: float
    recarga_total_min: float
    recarga_atual: float
    recarga_inicial: float
    ativado = False
    travado = False

    def __init__(self, nome: str, recarga_total_min: float, recarga_total_max: float, recarga_inicial: float, travado=False) -> None:
        self.nome = nome
        self.recarga_total_max = recarga_total_min
        self.recarga_total_min = recarga_total_max
        self.recarga_atual = self.recarga_inicial = recarga_inicial
        self.travado = travado

    def update(self, delta_tempo):
        if not self.travado:
            if self.recarga_atual <= 0:
                self.ativado = True
            elif not self.ativado:
                self.recarga_atual -= delta_tempo

    def coletar(self):
        if self.ativado:
            self.recarga_atual = uniform(self.recarga_total_min, self.recarga_total_max)
            self.ativado = False
            return self.nome
        return None

    def reiniciar(self, tempo=None):
        if tempo is None:
            tempo = self.recarga_inicial
        self.recarga_atual = tempo
        self.ativado = False
        self.travado = False

    def travar(self, travado=True):
        self.travado = travado


EVENTOS_LISTA_DICT: dict
