import pandas as pd
from ID3 import ID3
import matplotlib.pyplot as plt

cut = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]

def discretization(df, colunas, num_faixas):
    df_discretizado = df.copy()
    
    for coluna in colunas:
        # Cria os faixas
        df_discretizado[coluna] = pd.qcut(df[coluna],num_faixas,labels=False,duplicates='drop')
    
    return df_discretizado

def run_tests(cut):
    acuracias = []

    for i in cut:
        print(f'\n🔥 Testando com  faixas 🔥')

        df = pd.read_csv('treino_sinais_vitais_com_label.txt')
        df = discretization(df, ['1', '2', '3', '4', '5'], 10)
        df_shuffled = df.sample(frac=1, random_state=42)
        metade=int(len(df)*i)
        treino=df_shuffled.iloc[:metade]
        dataset=df_shuffled.iloc[metade:]
        teste=dataset.drop(columns='classe')

        indtree = ID3(treino, ['1', '2', '3', '4', '5'], 'classe')
        resultado = indtree.resultado(teste)

        df_comparacao = pd.merge(resultado, dataset[['ID', 'classe']], on='ID', how='left')
        df_comparacao['acerto'] = df_comparacao['resultado'] == df_comparacao['classe']
        acuracia = df_comparacao['acerto'].mean() * 100

        print(f'Acurácia com {i} faixas: {acuracia:.2f}%')
        acuracias.append(acuracia)

    return acuracias

acuracias = run_tests(cut)

plt.figure(figsize=(10, 6))
plt.plot(cut, acuracias, marker='o', linestyle='-', color='green')
plt.title('Acurácia x porcetagem do dataset')
plt.xlabel('porcentagem do dataset')
plt.ylabel('Acurácia (%)')
plt.grid(True)
plt.show()