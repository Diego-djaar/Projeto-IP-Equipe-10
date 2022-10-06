class Vetor:
    # Vetor em duas dimensões
    x: float
    y: float

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def modulo_quadrado(self):
        return self.x**2+self.y**2

    def multiplicar_escalar(self, escalar: float):
        novo_x = self.x*escalar
        novo_y = self.y*escalar
        return Vetor(novo_x, novo_y)

    def soma_vetores(self, outro):
        novo_x = self.x+outro.x
        novo_y = self.y+outro.y
        return Vetor(novo_x, novo_y)
