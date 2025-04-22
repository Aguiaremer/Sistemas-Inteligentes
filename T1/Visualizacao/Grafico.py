import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


#df = pd.read_csv('TS_1.csv')
#df = pd.read_csv('TS_2.csv')
#df = pd.read_csv('TS_3.csv')
#df = pd.read_csv('AG_1.csv')
#df = pd.read_csv('AG_2.csv')
df = pd.read_csv('AG_3.csv')



"""
x = df['Temperatura Inicial']
y = df['Temperatura Final']
z = df['Alfa']

"""
x = df['Populacao']
y = df['Geracoes']
z = df['Taxa Mutacao']


cor = df['Custo']

# Criando figura 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot
sc = ax.scatter(x, y, z, c=cor, cmap='viridis')

# Eixos

""" 
ax.set_xlabel('Temperatura Inicial')
ax.set_ylabel('Temperatura Final')
ax.set_zlabel('Alfa')
"""
ax.set_xlabel('Populacao')
ax.set_ylabel('Geracoes')
ax.set_zlabel('Taxa Mutacao')

# Barra de cor
cbar = plt.colorbar(sc, pad=0.1, shrink=0.8, aspect=20)
cbar.set_label('Custo')

plt.title('Algoritmo Genetico com 15 vertices')
plt.show()