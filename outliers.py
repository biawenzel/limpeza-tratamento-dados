'''Foi informado que nessa base de dados há possíveis fraudes que podem ser identificadas através dos outliers no “valor da transação”. Basicamente a fraude seria um outlier.

Sua missão é construir uma função que recebe dois parâmetros, a coluna que você quer analisar se tem outlier e o DataFrame em questão. A intenção de fazer isso é aproveitar novamente essa função tanto para outras colunas quanto para outros DataFrames futuramente em outras análises. O método que deve ser implementado para identificação do outlier é do intervalo interquartil.'''

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# criando um DataFrame com 30 transações aleatórias
df = pd.DataFrame({
    'ID da transação': range(1, 31),
    'Valor da transação': [100, 200, 150, 500, 300, 913, 250, 400, 200, 150, 
                           200, 200, 400, 300, 150, 301, 805, 300, 400, 250, 
                           150, 100, 500, 600, 200, 350, 100, 250, 800, 250],
    'Data da transação': pd.date_range(start='2022-01-01', end='2022-01-30', freq='D'),
    'Local da transação': ['São Paulo, Brasil', 'Rio de Janeiro, Brasil', 'Belo Horizonte, Brasil', 'São Paulo, Brasil', 
                           'São Paulo, Brasil', 'Nova Iorque, EUA', 'São Paulo, Brasil', 'São Paulo, Brasil', 'São Paulo, Brasil',
                           'Rio de Janeiro, Brasil', 'São Paulo, Brasil', 'São Paulo, Brasil', 'São Paulo, Brasil', 'São Paulo, Brasil',
                           'São Paulo, Brasil', 'São Paulo, Brasil', 'Los Angeles, EUA', 'São Paulo, Brasil', 'São Paulo, Brasil', 'São Paulo, Brasil',
                           'São Paulo, Brasil', 'São Paulo, Brasil', 'São Paulo, Brasil', 'São Paulo, Brasil', 'São Paulo, Brasil', 'São Paulo, Brasil',
                           'São Paulo, Brasil', 'São Paulo, Brasil', 'Miami, EUA', 'São Paulo, Brasil']
})

'''#usando boxplot para ver os candidatos a outliers
sns.boxplot(x=df['Valor da transação'])
#plt.show()

#achando os quartis
Q1 = df['Valor da transação'].quantile(.25)
Q3 = df['Valor da transação'].quantile(.75)
IQR = Q3 - Q1 #intervalo interquartil
limite_inferior = Q1 - 1.5*IQR
limite_superior = Q3 + 1.5*IQR

#para achar os outliers, vamos encontrar os valores < limite inferior OU > limite superior
outliers_index = (df['Valor da transação'] < limite_inferior) | (df['Valor da transação'] > limite_superior)
print(df[outliers_index]['Valor da transação'])'''

#função que responde à questão:
def acha_outliers(dataframe, coluna):
    Q1 = dataframe[coluna].quantile(.25)
    Q3 = dataframe[coluna].quantile(.75)
    IQR = Q3 - Q1 #intervalo interquartil
    limite_inferior = Q1 - 1.5*IQR
    limite_superior = Q3 + 1.5*IQR
    outliers = dataframe[(dataframe[coluna] < limite_inferior) | (dataframe[coluna] > limite_superior)]
    return outliers

print(acha_outliers(df, 'Valor da transação'))