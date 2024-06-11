import pandas as pd
import json

#carregando e normalizando json
with open('Pandas - Limpeza e tratamento de dados/dataset-telecon.json') as df:
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
for col in df_normalizado.columns:
    print(f'Coluna: {col}')
    print(df_normalizado[col].unique())
    print('-' * 30)

#criando uma cópia do df sem as linhas com string vazia em 'Churn'
df_sem_vazio = df_normalizado[df_normalizado['Churn'] != ''].copy()
df_sem_vazio.reset_index(drop=True, inplace=True)
print(df_sem_vazio.info())