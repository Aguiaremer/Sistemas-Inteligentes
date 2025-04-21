import heapq
import time

class AEstrela:
    def __init__(self, grafo):
        """
        Inicializa a classe AEstrela com um objeto da classe Grafo.
        
        grafo_obj: instância da classe Grafo
        """
        self.grafo = grafo.grafo
        self.n = grafo.n
        self.cidade_inicial = 0
        self.tempo_execucao = 0
        self.caminho = []
        self.custo_total = float('inf')

    def heuristica(self, atual, restantes):
        """
        Heurística baseada na menor saída + menor retorno para a cidade inicial.
        """
        if not restantes:
            return self.grafo[atual][self.cidade_inicial]

        menor_saida = min(self.grafo[atual][c] for c in restantes)
        menor_retorno = min(self.grafo[c][self.cidade_inicial] for c in restantes)
        return menor_saida + menor_retorno

    def executar(self):
        """
        Executa o algoritmo A* para resolver o problema do caixeiro viajante.
        """
        inicio = time.time()

        fila = []
        heapq.heappush(
            fila,
            (0, 0, self.cidade_inicial, [self.cidade_inicial], set([self.cidade_inicial]))
        )

        while fila:
            f, g, atual, caminho, visitados = heapq.heappop(fila)

            if len(visitados) == self.n:
                self.caminho = caminho + [self.cidade_inicial]
                self.custo_total = g + self.grafo[atual][self.cidade_inicial]
                break

            for prox in range(self.n):
                if prox not in visitados:
                    novo_g = g + self.grafo[atual][prox]
                    novo_visitados = visitados | {prox}
                    novo_caminho = caminho + [prox]

                    h = self.heuristica(prox, set(range(self.n)) - novo_visitados)
                    f = novo_g + h

                    heapq.heappush(fila, (f, novo_g, prox, novo_caminho, novo_visitados))

        fim = time.time()
        self.tempo_execucao = fim - inicio

    def exibir_resultado(self):
        """
        Imprime os dados relevantes da execução do algoritmo.
        """
        print("\n ---Resultado da Busca com A*---:")
        print(f" Caminho encontrado: {self.caminho}")
        print(f" Custo total: {self.custo_total}")
        print(f" Tempo de execução: {self.tempo_execucao:.4f} segundos")
        print("--------------------------------------\n")