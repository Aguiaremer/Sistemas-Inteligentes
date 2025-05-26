import pandas as pd
from ID3 import ID3
from discretizacao import *
import matplotlib.pyplot as plt

def rodar_testes(num_bins_lista):
    acuracias = []

    for num_bins in num_bins_lista:
        print(f'\n🔥 Testando com {num_bins} bins 🔥')

        df = pd.read_csv('treino_sinais_vitais_com_label.txt')
        treino = equalfreq_discr(df, ['1', '2', '3', '4', '5'], num_bins)
        teste = treino.drop('classe', axis=1)

        indtree = ID3(treino, ['1', '2', '3', '4', '5'], 'classe')
        resultado = indtree.resultado(teste)

        df_comparacao = pd.merge(resultado, treino[['ID', 'classe']], on='ID', how='left')
        df_comparacao['acerto'] = df_comparacao['resultado'] == df_comparacao['classe']
        acuracia = df_comparacao['acerto'].mean() * 100

        print(f'Acurácia com {num_bins} bins: {acuracia:.2f}%')
        acuracias.append(acuracia)

    return acuracias

num_bins_lista = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]

acuracias = rodar_testes(num_bins_lista)

plt.figure(figsize=(10, 6))
plt.plot(num_bins_lista, acuracias, marker='o', linestyle='-', color='green')
plt.title('Acurácia x Número de faixas')
plt.xlabel('Número de faixas')
plt.ylabel('Acurácia (%)')
plt.grid(True)
plt.show()