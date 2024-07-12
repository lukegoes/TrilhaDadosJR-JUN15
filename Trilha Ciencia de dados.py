import pandas as pd
import matplotlib.pyplot as plt

# Carregar o arquivo CSV
nome_arquivo = 'C:/Users/PC/Desktop/vendas_cursos.csv'
dados = pd.read_csv(nome_arquivo, encoding='latin1')

# Ajustar o tipo de dado para 'Quantidade de Vendas' se necessário
dados['Quantidade de Vendas'] = dados['Quantidade de Vendas'].astype('int64')

# Exibir as primeiras linhas do conjunto de dados
print("Primeiras linhas do conjunto de dados:")
print(dados.head())

# Informações básicas do conjunto de dados
print("\nInformações básicas do conjunto de dados:")
print(dados.info())

# Estatísticas descritivas
descritivas = dados.describe()

# Formatar os valores numéricos como decimais com vírgula
descritivas['Quantidade de Vendas'] = descritivas['Quantidade de Vendas'].apply(lambda x: f"{x:.2f}".replace('.', ','))
descritivas['Preço Unitário'] = descritivas['Preço Unitário'].apply(lambda x: f"{x:.2f}".replace('.', ','))

print("\nEstatísticas descritivas para colunas numéricas (formatadas):")
print(descritivas)

# Determinar os cursos com mais vendas
num_top_cursos = 3  # número de cursos a destacar
top_cursos = dados.nlargest(num_top_cursos, 'Quantidade de Vendas')['Nome do Curso']

# Função para definir cor baseada na quantidade de vendas
def define_cor(nome_curso):
    if nome_curso in top_cursos.values:
        return 'green'
    return 'skyblue'

# Aplicar a função de cor às barras
dados['Cor'] = dados['Nome do Curso'].apply(define_cor)

# Ordenar os dados pelo nome do curso antes de plotar
dados_ordenados = dados.sort_values('Quantidade de Vendas', ascending=True)

# Gráfico de barras horizontal para contar as categorias de cursos
plt.figure(figsize=(12, 8))
plt.barh(dados_ordenados['Nome do Curso'], dados_ordenados['Quantidade de Vendas'], color=dados_ordenados['Cor'])
plt.title('Contagem de Vendas por Curso')
plt.xlabel('Quantidade de Vendas')
plt.ylabel('Nome do Curso')
plt.tight_layout()
plt.show()

# Gráfico de dispersão para relação entre Quantidade de Vendas e Preço Unitário
plt.figure(figsize=(8, 6))
plt.scatter(dados['Preço Unitário'], dados['Quantidade de Vendas'], color='coral', alpha=0.7)
plt.title('Relação entre Preço Unitário e Quantidade de Vendas')
plt.xlabel('Preço Unitário')
plt.ylabel('Quantidade de Vendas')
plt.grid(True)
plt.tight_layout()
plt.show()