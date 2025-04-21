import random
import math
import time
import itertools
import csv

class Tempera_Simulada:
    def __init__(self, grafo, temp_inicial, temp_final, alfa):
        """
        Inicializa os parâmetros da têmpera simulada.
        
        :param grafo: Objeto do tipo Grafo (vindo de Grafo.py)
        :param temp_inicial: Temperatura inicial do sistema
        :param temp_final: Temperatura final (critério de parada)
        :param alfa: Fator de resfriamento (quanto menor, mais devagar esfria)
        """
        self.grafo = grafo
        self.temp_inicial = temp_inicial
        self.temp_final = temp_final
        self.alfa = alfa
        self.melhor_rota = []
        self.melhor_custo = float('inf')
        self.tempo_execucao = 0

    def _vizinho(self, rota):
        """
        Gera uma nova rota trocando duas cidades de lugar aleatoriamente.
        """
        a, b = random.sample(range(len(rota)), 2)
        nova_rota = rota[:]
        nova_rota[a], nova_rota[b] = nova_rota[b], nova_rota[a]
        return nova_rota

    def executar(self):
        """
        Executa o algoritmo da têmpera simulada.
        """
        n = self.grafo.n
        atual = list(range(n))
        random.shuffle(atual)  # Começa com uma rota aleatória
        melhor = atual[:]
        custo_atual = self.grafo.calcular_distancia(atual)
        custo_melhor = custo_atual
        temperatura = self.temp_inicial

        inicio = time.time()

        while temperatura > self.temp_final:
            candidato = self._vizinho(atual)
            custo_candidato = self.grafo.calcular_distancia(candidato)
            delta = custo_candidato - custo_atual

            # Aceita se for melhor ou com probabilidade baseada na temperatura
            if delta < 0 or random.random() < math.exp(-delta / temperatura):
                atual = candidato
                custo_atual = custo_candidato
                if custo_atual < custo_melhor:
                    melhor = atual
                    custo_melhor = custo_atual

            temperatura *= self.alfa  # Resfriamento gradual

        fim = time.time()

        self.melhor_rota = melhor
        self.melhor_custo = custo_melhor
        self.tempo_execucao = fim - inicio

    def exibir_resultado(self):
        """
        Mostra os dados importantes depois de rodar a têmpera simulada.
        """
        print("\n--- Resultado da Têmpera Simulada ---")
        print(f"Melhor rota encontrada: {self.melhor_rota + [self.melhor_rota[0]]}")
        print(f"Custo total da rota: {self.melhor_custo}")
        print(f"Tempo de execução: {self.tempo_execucao:.4f} segundos")
        print("--------------------------------------\n")


def Tempera_Simulada_teste(grafo, temperaturas_iniciais, temperaturas_finais, alfas, arquivo_saida):
    # Combinações de todos os parâmetros
    combinacoes = list(itertools.product(temperaturas_iniciais, temperaturas_finais, alfas))

    melhor_custo_global = float('inf')
    tempo_melhor_custo = float('inf')
    melhor_combinacao = None

    # Criando o arquivo CSV e escrevendo o cabeçalho
    with open(arquivo_saida, mode='w', newline='') as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        writer.writerow(["Temperatura Inicial", "Temperatura Final", "Alfa", "Custo", "Tempo Execucao"])

        print("\nTestando combinações de parâmetros para a têmpera simulada...\n")

        for temp_ini, temp_fim, alfa in combinacoes:
            print(f"🔧 Testando: T_inicial={temp_ini}, T_final={temp_fim}, alfa={alfa}")

            ts = Tempera_Simulada(
                grafo=grafo,
                temp_inicial=temp_ini,
                temp_final=temp_fim,
                alfa=alfa
            )

            ts.executar()
            print(f"   ➤ Custo: {ts.melhor_custo} | Tempo: {ts.tempo_execucao:.3f}s")

            # Escreve os resultados no arquivo CSV
            writer.writerow([temp_ini, temp_fim, alfa, ts.melhor_custo, round(ts.tempo_execucao, 3)])

            if ts.melhor_custo < melhor_custo_global:
                melhor_custo_global = ts.melhor_custo
                tempo_melhor_custo = ts.tempo_execucao
                melhor_combinacao = (temp_ini, temp_fim, alfa)

    print("\n✅ MELHOR COMBINAÇÃO PARA A TEMPERA SIMULADA ENCONTRADA:")
    print(f"T_inicial={melhor_combinacao[0]}, T_final={melhor_combinacao[1]}, alfa={melhor_combinacao[2]}")
    print(f"Custo total: {melhor_custo_global}, Tempo de Execução: {tempo_melhor_custo:.3f}")
