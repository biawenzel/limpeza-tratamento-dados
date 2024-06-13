import pandas as pd
import json, numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

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

#procurando por outliers
'''sns.boxplot(x=df_sem_nulos['cliente.tempo_servico'])
plt.show()'''

#selecionando o 1º quartil de valores (25%) e o 3º (75%) - lembrando que a marca de 50% é a mediana
Q1 = df_sem_nulos['cliente.tempo_servico'].quantile(.25)
Q3 = df_sem_nulos['cliente.tempo_servico'].quantile(.75)
IQR = Q3 - Q1
lim_inf = Q1 - 1.5*IQR
lim_sup = Q3 + 1.5*IQR

#para achar os outliers, vamos encontrar os índices desses valores
outliers_index = (df_sem_nulos['cliente.tempo_servico'] < lim_inf) | (df_sem_nulos['cliente.tempo_servico'] > lim_sup)

#mudando os valores errados de tempo de serviço dividindo o total pelo mensal
df_sem_nulos.loc[outliers_index, 'cliente.tempo_servico'] = np.ceil(
    df_sem_nulos.loc[outliers_index, 'conta.cobranca.Total'] / df_sem_nulos.loc[outliers_index, 'conta.cobranca.mensal']
)
'''sns.boxplot(x=df_sem_nulos['cliente.tempo_servico'])
plt.show()'''

#refazendo o filtro de outliers para filtrar apenas os valores que ainda são outliers
Q1 = df_sem_nulos['cliente.tempo_servico'].quantile(.25)
Q3 = df_sem_nulos['cliente.tempo_servico'].quantile(.75)
IQR = Q3 - Q1
limite_inf = Q1 - 1.5*IQR
limite_sup = Q3 + 1.5*IQR

outliers_index2 = (df_sem_nulos['cliente.tempo_servico'] < limite_inf) | (df_sem_nulos['cliente.tempo_servico'] > limite_sup)

#criando um novo dataframe sem os outliers
df_sem_out = df_sem_nulos[~outliers_index2]
df_sem_out.reset_index(drop=True, inplace=True)

#checando se os outliers realmente não existem mais
'''sns.boxplot(x=df_sem_out['cliente.tempo_servico'])
plt.show()'''

#substituindo strings por valores numéricos para o modelo de ML funcionar melhor
df_sem_id = df_sem_out.drop('id_cliente', axis=1)
mapeamento = {'nao': 0, 'sim': 1,'masculino': 0, 'feminino': 1}

#achando as colunas que contém só respostas com as chaves do mapeamento
'''for col in df_sem_id.columns:
  print(f'Coluna: {col}') #nome da coluna
  print(df_sem_id[col].unique()) #traz os valores únicos dessa coluna
  print('-' * 30)'''

colunas = ['Churn', 'cliente.genero', 'cliente.parceiro', 'cliente.dependentes', 'telefone.servico_telefone', 'conta.faturamente_eletronico']
df_sem_id[colunas] = df_sem_id[colunas].replace(mapeamento)

#transformando o resto das variáveis qualitativas em valores numéricos
df_dummies = pd.get_dummies(df_sem_id, dtype=int)

#print(df_dummies.info())