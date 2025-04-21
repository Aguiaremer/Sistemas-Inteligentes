import random

class Grafo:
    def __init__(self, n_cidades, peso_min=1, peso_max=100, semente=None):
        if n_cidades > 15:
            raise ValueError("ERRO: mais que 15 cidades vai dar ruim")
        
        self.n = n_cidades
        self.peso_min = peso_min
        self.peso_max = peso_max
        self.semente = semente
        self.grafo = [[0] * self.n for _ in range(self.n)]

        if semente is not None:
            random.seed(semente)
        
        self._gerar_grafo()

    def _gerar_grafo(self):
        for i in range(self.n):
            for j in range(i + 1, self.n):
                peso = random.randint(self.peso_min, self.peso_max)
                self.grafo[i][j] = peso
                self.grafo[j][i] = peso

    def calcular_distancia(self, rota):
        distancia = 0
        for i in range(len(rota) - 1):
            distancia += self.grafo[rota[i]][rota[i+1]]
        distancia += self.grafo[rota[-1]][rota[0]]  # Volta pra cidade inicial
        return distancia