import pandas as pd
from ID3 import ID3
import matplotlib.pyplot as plt

num_faixas_lista = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]

def discretization(df, colunas, num_faixas):
    df_discretizado = df.copy()
    
    for coluna in colunas:
        # Cria os faixas
        df_discretizado[coluna] = pd.qcut(df[coluna],num_faixas,labels=False,duplicates='drop')
    
    return df_discretizado

def run_tests(num_faixas_lista):
    acuracias = []

    for num_faixas in num_faixas_lista:
        print(f'\n🔥 Testando com {num_faixas} faixas 🔥')

        df = pd.read_csv('treino_sinais_vitais_com_label.txt')
        treino = discretization(df, ['1', '2', '3', '4', '5'], num_faixas)
        teste = treino.drop('classe', axis=1)

        indtree = ID3(treino, ['1', '2', '3', '4', '5'], 'classe')
        resultado = indtree.resultado(teste)

        df_comparacao = pd.merge(resultado, treino[['ID', 'classe']], on='ID', how='left')
        df_comparacao['acerto'] = df_comparacao['resultado'] == df_comparacao['classe']
        acuracia = df_comparacao['acerto'].mean() * 100

        print(f'Acurácia com {num_faixas} faixas: {acuracia:.2f}%')
        acuracias.append(acuracia)

    return acuracias

acuracias = run_tests(num_faixas_lista)

plt.figure(figsize=(10, 6))
plt.plot(num_faixas_lista, acuracias, marker='o', linestyle='-', color='green')
plt.title('Acurácia x Número de faixas')
plt.xlabel('Número de faixas')
plt.ylabel('Acurácia (%)')
plt.grid(True)
plt.show()