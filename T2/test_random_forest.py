import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Criando o dataframe
data = pd.read_csv('treino_sinais_vitais_com_label.txt')

df = pd.DataFrame(data)

# Separando features e target
X = df.drop(['ID', 'classe'], axis=1)
y = df['classe']

# Dividindo em treino e teste (aqui é só exemplo, com poucos dados)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

# Criando e treinando o modelo
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Fazendo previsões
y_pred = model.predict(X_test)

# Avaliando
acc = accuracy_score(y_test, y_pred)
print(f'Acurácia: {acc:.2f}')

# Previsão de novos dados (exemplo)
# novos_dados = [[13, 12, 8, 70, 20, 40]]
# pred = model.predict(novos_dados)
# print(f'Classe prevista: {pred}')