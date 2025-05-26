import pandas as pd
import numpy as np

class ID3:
    def __init__(self, dados, atributos, alvo):
        self.dados = dados
        self.atributos = atributos
        self.alvo = alvo
        self.arvore = self.id3_algorithm(dados, atributos, alvo)

    def id3_algorithm(self, dados, atributos, alvo):
        alvo_valores = dados[alvo]
        
        # Se todos são da mesma classe
        if len(np.unique(alvo_valores)) == 1:
            return np.unique(alvo_valores)[0]
        
        # Se não há mais atributos
        if len(atributos) == 0:
            return alvo_valores.mode()[0]  # Classe mais comum

        # Atributo com menor ganho
        melhor_atributo = atributos[self.maior_ganho(dados,atributos,alvo)]
        
        # Criar nó da árvore
        arvore = {melhor_atributo: {}}
        
        for valor in np.unique(dados[melhor_atributo]):
            subset = dados[dados[melhor_atributo] == valor]
            
            if subset.shape[0] == 0:
                arvore[melhor_atributo][valor] = alvo_valores.mode()[0]
            else:
                novos_atributos = [a for a in atributos if a != melhor_atributo]
                arvore[melhor_atributo][valor] = self.id3_algorithm(subset, novos_atributos, alvo)
    
        return arvore

    def maior_ganho(self,dados,atributos,alvo):
        entr_alvo=self.entropia_alvo(dados,alvo)
        ganhos=[]
        maior_ganho=0
        for i in range(len(atributos)):
            ganho=entr_alvo-self.entropia_atributo(dados,atributos[i],alvo)
            ganhos.append(ganho)
            if(ganho>ganhos[maior_ganho]):
                maior_ganho=i
        return maior_ganho
    
    def entropia_atributo(self,dados,_atributo,_alvo):
        alvo=dados[_alvo]
        atributo=dados[_atributo]
        total=len(alvo)
        resultado= pd.crosstab(atributo,alvo)
        entropia_lista=[]
        for valor_atrib in resultado.index:
            entropia=0
            qntd=0
            for valor_alvo in resultado.columns:
                qntd+=resultado.loc[valor_atrib, valor_alvo]
            for valor_alvo in resultado.columns:
                if(resultado.loc[valor_atrib, valor_alvo]==0):
                    entropia-=0
                else:
                    prob= resultado.loc[valor_atrib, valor_alvo]/qntd
                    entropia-=prob*np.log2(prob)
            entropia_lista.append(entropia*qntd/total)
        entropia_total=0
        while (entropia_lista):
            entropia_total+=entropia_lista.pop(0)
        return entropia_total

    def entropia_alvo(self,dados,alvo):
        coluna=dados[alvo]
        total=len(coluna)
        contagem=coluna.value_counts()
        entropia=0
        for qntd in contagem:
            prob= qntd/total
            entropia-=prob*np.log2(prob)
        return entropia 
    
    def prever(self,instancia,arvore):
        if not isinstance(arvore, dict):
            return arvore  # Nó folha, retorna a classe

        atributo = next(iter(arvore))  # Pega a raiz (atributo atual)
        valor = instancia.get(atributo)

        if valor in arvore[atributo]:
            return self.prever(instancia, arvore[atributo][valor])
        else:
            return None  # Valor não visto na árvore
    
    def resultado(self, dados):
        #dados tem que ter o campo ID
        ids=dados['ID']
        resultado={}
        for id_value in ids:
            instancia = dados[dados['ID'] == id_value].iloc[0].to_dict()
            resultado[id_value] = self.prever(instancia, self.arvore)
        dados['resultado']=dados['ID'].map(resultado)
        return dados
