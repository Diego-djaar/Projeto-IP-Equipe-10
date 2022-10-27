# usar isso ao invés de pygame.USEREVENT

from random import uniform
from typing import List, Tuple


class Evento:
    nome: str
    recarga_total_max: float
    recarga_total_min: float
    recarga_atual: float
    ativado = False

    def __init__(self, nome: str, recarga_total_max: float, recarga_total_min: float, recarga_inicial: float) -> None:
        self.nome = nome
        self.recarga_total_max = recarga_total_max
        self.recarga_total_min = recarga_total_min
        self.recarga_atual = recarga_inicial

    def update(self, delta_tempo):
        if self.recarga_atual <= 0:
            self.ativado = True
        elif not self.ativado:
            self.recarga_atual -= delta_tempo

    def coletar(self):
        if self.ativado:
            self.recarga_atual = uniform(self.recarga_total_max, self.recarga_total_min)
            self.ativado = False
            return self.nome
        return None


EVENTOS_LISTA: List[Evento]
