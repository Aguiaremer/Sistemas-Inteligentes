import time
import random
import matplotlib.pyplot as plt
from Grafo import Grafo
from A_Estrela import AEstrela
from Tempera_Simulada import Tempera_Simulada, Tempera_Simulada_teste
from Algoritmo_Genetico import Algoritmo_Genetico, Algoritmo_Genetico_teste

"""
Definições dos parâmetros globais
"""

# Grafo
vertices = 15
peso_min = 1
peso_max = 100
semente = random.randint(0, 1000)

# Parâmetros para testar no Tempera Simulada
temperaturas_iniciais = [500, 1000, 1500, 2000]
temperaturas_finais = [0.1, 0.05, 0.01, 0.005]
alfas = [0.95, 0.98, 0.995, 0.999]

# Parâmetros para testar no algoritmo genetico
populacoes = [50, 100, 150, 200]
qnt_geracoes = [500, 1000, 1500, 2000]
taxas_mutacao = [0.05, 0.1, 0.15, 0.2]

if __name__ == '__main__':

    grafo = Grafo(vertices, peso_min, peso_max, semente)
    Tempera_Simulada_teste(grafo,temperaturas_iniciais,temperaturas_finais,alfas,"resultado_TS")
    Algoritmo_Genetico_teste(grafo,populacoes,qnt_geracoes,taxas_mutacao,"resultado_AG")

    # Teste A*
    aestrela = AEstrela(grafo)
    aestrela.executar()

    # Imprimir resultados
    print("\n--- Resultados dos Algoritmos ---")
    aestrela.exibir_resultado()
    
