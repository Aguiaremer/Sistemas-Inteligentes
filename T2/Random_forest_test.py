from Random_forest import *
import matplotlib.pyplot as plt

num_arvores= [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
num_testes=5

def run_tests(num_arvores,num_testes):
    acuracias = []

    for num_arvores in num_arvores:
        acuracia_med=0
        for i in range(num_testes):
            print(f'\n🔥 Testando com {num_arvores} arvores 🔥')

            df = pd.read_csv('treino_sinais_vitais_com_label.txt')
            df_shuffled = df.sample(frac=1, random_state=42)
            metade=len(df)//2
            treino=df_shuffled.iloc[:metade]
            dataset=df_shuffled.iloc[metade:]
            treino = Random_florest(treino, ['1', '2', '3', '4', '5'],'classe',3,10,num_arvores)
            
            teste = dataset.drop(columns=['classe'])

            resultado = treino.resultado(teste)

            df_comparacao = pd.merge(resultado, dataset[['ID', 'classe']], on='ID', how='left')
            df_comparacao['acerto'] = df_comparacao['resultado'] == df_comparacao['classe']
            acuracia = df_comparacao['acerto'].mean() * 100

            print(f'Acurácia com {num_arvores} arvores: {acuracia:.2f}%')
            acuracia_med+=acuracia
        acuracias.append(acuracia_med/num_testes)
        print(f"acutacia media :{acuracia_med/num_testes}")
            

    return acuracias

acuracias = run_tests(num_arvores,num_testes)

plt.figure(figsize=(10, 6))
plt.plot(num_arvores, acuracias, marker='o', linestyle='-', color='green')
plt.title('Acurácia média x Número de árvores')
plt.xlabel('Número de arvores')
plt.ylabel('Acurácia media(%)')
plt.grid(True)
plt.show()