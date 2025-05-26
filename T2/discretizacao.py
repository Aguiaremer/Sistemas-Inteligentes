import pandas as pd
from sklearn.preprocessing import KBinsDiscretizer

def avg_discr(df, folga):
    df_discreto = df.copy()

    for coluna in df.columns:
        if pd.api.types.is_numeric_dtype(df[coluna]) and coluna != 'ID' and coluna !='gravidade' and coluna !='classe':
            media = df[coluna].mean()
            inferior = media - folga
            superior = media + folga
            df_discreto[coluna] = df[coluna].apply(lambda x: 1 if inferior <= x <= superior else 0)

    return df_discreto

def boa_discr(df):
    id = df['ID']
    X = df[['1', '2', '3', '4', '5']]
    y = df['classe']


    # Cria discretizador
    discretizador = KBinsDiscretizer(n_bins=4, encode='ordinal', strategy='kmeans') # Entropy = parecido com MDLP

    # Aplica
    X_discretizado = discretizador.fit_transform(X, y)

    df_discretizado['id'] = id
    df_discretizado = pd.DataFrame(X_discretizado, columns=['1', '2', '3', '4', '5'])
    df_discretizado['classe'] = y

    return df_discretizado

def equalfreq_discr(df, colunas, num_bins):
    df_discretizado = df.copy()
    
    for coluna in colunas:
        # Cria os bins
        df_discretizado[coluna] = pd.qcut(
            df[coluna],
            q=num_bins,
            labels=False,
            duplicates='drop'  # Evita erro se tiver valores repetidos demais
        )
    
    return df_discretizado

