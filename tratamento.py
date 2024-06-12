import pandas as pd
import json, numpy as np

#carregando e normalizando json
with open('Pandas - Limpeza e tratamento de dados\limpeza-tratamento-dados\dataset-telecon.json') as df:
    df_json = json.load(df)

df_normalizado = pd.json_normalize(df_json)

#visualizando dados em branco
df_normalizado[df_normalizado['conta.cobranca.Total'] == ' '][['cliente.tempo_servico', 'conta.contrato', 'conta.cobranca.mensal', 'conta.cobranca.Total']]

#usando os índices para preencher os espaços em branco
idx = df_normalizado[df_normalizado['conta.cobranca.Total'] == ' '].index
df_normalizado.loc[idx, 'conta.cobranca.Total'] = df_normalizado.loc[idx, 'conta.cobranca.mensal'] * 24 #2 anos
df_normalizado.loc[idx, 'cliente.tempo_servico'] = 24

#modificando tipos de object para o tipo correto
df_normalizado['conta.cobranca.Total'] = df_normalizado['conta.cobranca.Total'].astype(float)

#identificando strings vazias
'''for col in df_normalizado.columns:
    print(f'Coluna: {col}')
    print(df_normalizado[col].unique())
    print('-' * 30)'''

#criando uma cópia do df sem as linhas com string vazia em 'Churn'
df_sem_vazio = df_normalizado[df_normalizado['Churn'] != ''].copy()
df_sem_vazio.reset_index(drop=True, inplace=True)

#identificando e tratando dados duplicados
valores_duplicados = df_sem_vazio.duplicated()
df_sem_vazio.drop_duplicates(inplace=True)

#identificando e substituindo dados nulos
filtro = df_sem_vazio['cliente.tempo_servico'].isna()

df_sem_vazio['cliente.tempo_servico'].fillna(
    np.ceil(df_sem_vazio['conta.cobranca.Total'] / df_sem_vazio['conta.cobranca.mensal']), inplace=True
) #preenchendo o tempo de serviço

'''print(df_sem_vazio[filtro][['cliente.tempo_servico', 'conta.cobranca.mensal', 'conta.cobranca.Total']])'''

#apagando os dados nulos
colunas_dados_vazios = ['conta.contrato', 'conta.faturamente_eletronico', 'conta.metodo_pagamento']
df_sem_nulos = df_sem_vazio.dropna(subset=colunas_dados_vazios)

#resetando o index do df
df_sem_nulos.reset_index(drop=True, inplace=True)

#print(df_sem_vazio.info())