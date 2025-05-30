import pandas as pd
import numpy as np
from collections import Counter

class Node:
    def __init__(self, gini, num_samples, num_samples_per_class, predicted_class):
        self.gini = gini
        self.num_samples = num_samples
        self.num_samples_per_class = num_samples_per_class
        self.predicted_class = predicted_class
        self.feature_index = None
        self.threshold = None
        self.left = None
        self.right = None


class DecisionTree:
    def __init__(self, max_depth=5):
        self.max_depth = max_depth
        self.tree = None

    def gini_impurity(self, y):
        classes = np.unique(y)
        impurity = 1.0
        for c in classes:
            p = np.sum(y == c) / len(y)
            impurity -= p ** 2
        return impurity

    def gini_gain(self, y, y_left, y_right):
        p_left = len(y_left) / len(y)
        p_right = len(y_right) / len(y)
        gain = self.gini_impurity(y) - (p_left * self.gini_impurity(y_left) + p_right * self.gini_impurity(y_right))
        return gain

    def best_split(self, X, y):
        best_gain = 0
        best_col = None
        best_thresh = None
        for col in X.columns:
            values = np.unique(X[col])
            for val in values:
                left_mask = X[col] <= val
                y_left, y_right = y[left_mask], y[~left_mask]
                if len(y_left) == 0 or len(y_right) == 0:
                    continue
                gain = self.gini_gain(y, y_left, y_right)
                if gain > best_gain:
                    best_gain = gain
                    best_col = col
                    best_thresh = val
        return best_col, best_thresh

    def build_tree(self, X, y, depth=0):
        num_samples_per_class = [np.sum(y == c) for c in np.unique(y)]
        predicted_class = np.unique(y)[np.argmax(num_samples_per_class)]
        node = Node(
            gini=self.gini_impurity(y),
            num_samples=len(y),
            num_samples_per_class=num_samples_per_class,
            predicted_class=predicted_class
        )
        if depth < self.max_depth:
            col, thresh = self.best_split(X, y)
            if col is not None:
                node.feature_index = col
                node.threshold = thresh
                left_mask = X[col] <= thresh
                node.left = self.build_tree(X[left_mask], y[left_mask], depth + 1)
                node.right = self.build_tree(X[~left_mask], y[~left_mask], depth + 1)
        return node

    def fit(self, dados):
        X=dados.drop(columns=['ID','gravidade','classe'])
        y=dados['classe'].values
        self.tree = self.build_tree(X, y)

    def print_tree(self, node=None, depth=0):
        if node is None:
            node = self.tree
        prefix = "  " * depth
        if node.feature_index is None:
            print(f"{prefix}Predict: {node.predicted_class}")
        else:
            print(f"{prefix}If {node.feature_index} <= {node.threshold}:")
            self.print_tree(node.left, depth + 1)
            print(f"{prefix}Else:")
            self.print_tree(node.right, depth + 1)

    def predict(self, row, node):
        if node.feature_index is None:
            return node.predicted_class
        if row[node.feature_index] <= node.threshold:
            return self.predict(row, node.left)
        else:
            return self.predict(row, node.right)

class Random_florest:
    def __init__(self,dados,atributos,alvo,n_features,tam_arvore,qntd_arvore):
        self.dados=dados
        self.atributos=atributos
        self.alvo=alvo
        self.n_features=n_features
        self.tam_arvore=tam_arvore
        self.qntd_arvore=qntd_arvore
        self.forest=self.make_florest()

    def bootstrap(self):
        n_samples=len(self.dados['ID'])
        samples = np.random.choice(n_samples, n_samples, replace=True)
        features = np.random.choice(np.arange(1, len(self.atributos) + 1),self.n_features, replace=False)
        colunas_pra_dropar = [i for i in self.atributos if i not in map(str, features)]
        aux = self.dados.drop(colunas_pra_dropar, axis=1)
        bootstrap=pd.DataFrame({'ID': samples})
        return bootstrap.merge(aux,how='left')
    
    def make_florest(self):
        forest=[]
        for i in range(self.qntd_arvore):
            dataset=self.bootstrap()
            arvore=DecisionTree(self.tam_arvore)
            arvore.fit(dataset)
            forest.append(arvore)
        return forest
    
    def agregacao(self,lista):
        contador = Counter(lista)
        return contador.most_common(1)[0][0]
    
    def prever(self,linha):
        previsoes=[]
        for arvore in self.forest:
            previsoes.append(arvore.predict(linha,arvore.tree))
        return self.agregacao(previsoes)
        
    
    def resultado(self,dados):
        ids=dados['ID']
        resultado={}
        for id_value in ids:
            linha = dados[dados['ID'] == id_value].iloc[0]
            resultado[id_value]=self.prever(linha)
        dados['resultado']=dados['ID'].map(resultado)
        return dados