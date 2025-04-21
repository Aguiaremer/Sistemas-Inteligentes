import random
import time
import itertools
import csv

class Algoritmo_Genetico:
    def __init__(self, grafo, populacao_size, geracoes, taxa_mutacao):
        """
        grafo: instância da classe Grafo (do grafo.py)
        populacao_size: número de rotas em cada geração
        geracoes: número total de gerações
        taxa_mutacao: chance de uma mutação ocorrer em um indivíduo
        """
        self.grafo = grafo
        self.populacao_size = populacao_size
        self.geracoes = geracoes
        self.taxa_mutacao = taxa_mutacao

        self.melhor_rota = None
        self.melhor_distancia = float('inf')
        self.tempo_execucao = 0

    def _cruzamento(self, pai1, pai2):
        """Faz o cruzamento entre dois pais usando (OX)"""
        tamanho = len(pai1)
        filho = [-1] * tamanho
        inicio, fim = sorted([random.randint(0, tamanho-1), random.randint(0, tamanho-1)])

        for i in range(inicio, fim + 1):
            filho[i] = pai1[i]

        indice = 0
        for i in range(tamanho):
            if filho[i] == -1:
                while pai2[indice] in filho:
                    indice += 1
                filho[i] = pai2[indice]

        return filho

    def _mutacao(self, rota):
        """Aplica mutação trocando duas cidades de lugar na rota"""
        i, j = random.sample(range(len(rota)), 2)
        rota[i], rota[j] = rota[j], rota[i]
        return rota

    def executar(self):
        """Executa o algoritmo genético para resolver o TSP"""
        inicio = time.time()

        n = self.grafo.n
        populacao = [random.sample(range(n), n) for _ in range(self.populacao_size)]

        for geracao in range(self.geracoes):
            # Ordena pela distância (menor é melhor)
            populacao.sort(key=lambda x: self.grafo.calcular_distancia(x))

            # Atualiza o melhor da geração
            if self.grafo.calcular_distancia(populacao[0]) < self.melhor_distancia:
                self.melhor_rota = populacao[0][:]
                self.melhor_distancia = self.grafo.calcular_distancia(self.melhor_rota)

            nova_populacao = []
            for i in range(0, self.populacao_size, 2):
                pai1, pai2 = populacao[i], populacao[i+1]
                filho1 = self._cruzamento(pai1, pai2)
                filho2 = self._cruzamento(pai2, pai1)

                if random.random() < self.taxa_mutacao:
                    filho1 = self._mutacao(filho1)
                if random.random() < self.taxa_mutacao:
                    filho2 = self._mutacao(filho2)

                nova_populacao.append(filho1)
                nova_populacao.append(filho2)

            populacao = nova_populacao


        self.melhor_rota = self.melhor_rota + [self.melhor_rota[0]] 
        fim = time.time()
        self.tempo_execucao = fim - inicio

    def exibir_resultado(self):
        """Mostra as informações mais importantes da execução"""
        print("--- Resultado do Algoritmo Genético ---")
        print(f"Melhor rota encontrada: {self.melhor_rota}")
        print(f"Distância total: {self.melhor_distancia}")
        print(f"Tempo de execução: {self.tempo_execucao:.4f} segundos")
        print("--------------------------------------\n")

def Algoritmo_Genetico_teste(grafo, populacoes, qnt_geracoes, taxas_mutacao, arquivo_saida):
    # Combinações de todos os parâmetros do Algoritmo Genético
    combinacoes = list(itertools.product(populacoes, qnt_geracoes, taxas_mutacao))

    melhor_custo_global = float('inf')
    tempo_melhor_custo = float('inf')
    melhor_combinacao = None

    # Criando o arquivo CSV e escrevendo o cabeçalho
    with open(arquivo_saida, mode='w', newline='') as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        writer.writerow(["Populacao", "Geracoes", "Taxa Mutacao", "Custo", "Tempo Execucao"])

        print("\nTestando combinações de parâmetros para o Algoritmo Genético...\n")

        for populacao_size, geracoes, taxa_mutacao in combinacoes:
            print(f"🔧 Testando: População={populacao_size}, Gerações={geracoes}, Taxa Mutação={taxa_mutacao}")

            # Instancia o Algoritmo Genético
            ag = Algoritmo_Genetico(
                grafo=grafo,
                populacao_size=populacao_size,
                geracoes=geracoes,
                taxa_mutacao=taxa_mutacao
            )

            ag.executar()
            print(f"   ➤ Custo: {ag.melhor_distancia} | Tempo: {ag.tempo_execucao:.3f}s")

            # Escreve os resultados no arquivo CSV
            writer.writerow([populacao_size, geracoes, taxa_mutacao, ag.melhor_distancia, round(ag.tempo_execucao, 3)])

            if ag.melhor_distancia < melhor_custo_global:
                melhor_custo_global = ag.melhor_distancia
                tempo_melhor_custo = ag.tempo_execucao
                melhor_combinacao = (populacao_size, geracoes, taxa_mutacao)

    print("\n✅ MELHOR COMBINAÇÃO PARA O ALGORITMO GENETICO ENCONTRADA:")
    print(f"População={melhor_combinacao[0]}, Gerações={melhor_combinacao[1]}, Taxa Mutação={melhor_combinacao[2]}")
    print(f"Custo total: {melhor_custo_global}, Tempo de Execução: {tempo_melhor_custo:.3f}")
