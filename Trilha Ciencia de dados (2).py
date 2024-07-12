import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress


# Carregar o arquivo CSV
nome_arquivo = 'C:/Users/PC/Desktop/arquivos/vendas_cursos.csv'
dados = pd.read_csv(nome_arquivo, encoding='latin1')

# Ajustar o tipo de dado para 'Quantidade de Vendas' se necessário
dados['Quantidade de Vendas'] = dados['Quantidade de Vendas'].astype('int64')

# Exibir as primeiras linhas do conjunto de dados
print("Primeiras linhas do conjunto de dados:")
print(dados.head())

# Agrupar os dados por 'Nome do Curso' e somar as quantidades de vendas
dados_agrupados = dados.groupby('Nome do Curso', as_index=False).agg({'Quantidade de Vendas': 'sum', 'Preço Unitário': 'first'})

# Calcular a receita total
dados_agrupados['Receita Total'] = dados_agrupados['Quantidade de Vendas'] * dados_agrupados['Preço Unitário']
receita_total = dados_agrupados['Receita Total'].sum()

# Estatísticas descritivas
descritivas = dados_agrupados.describe()

# Formatar os valores numéricos como decimais com vírgula
descritivas['Quantidade de Vendas'] = descritivas['Quantidade de Vendas'].apply(lambda x: f"{x:.2f}".replace('.', ','))
descritivas['Preço Unitário'] = descritivas['Preço Unitário'].apply(lambda x: f"{x:.2f}".replace('.', ','))
descritivas['Receita Total'] = f"R${receita_total:.2f}"  # Formatar a receita total com duas casas decimais e o símbolo de real

print("\nEstatísticas descritivas para colunas numéricas (formatadas):")
print(descritivas)

# Determinar os cursos com mais vendas
num_top_cursos = 1  # número de cursos a destacar
top_cursos = dados_agrupados.nlargest(num_top_cursos, 'Quantidade de Vendas')['Nome do Curso']

# Determinar o curso com o maior faturamento
curso_maior_faturamento = dados_agrupados.loc[dados_agrupados['Receita Total'].idxmax(), 'Nome do Curso']

# Função para definir cor baseada no curso e no maior faturamento
def define_cor(nome_curso):
    if nome_curso == curso_maior_faturamento:
        return '#FFD700'  # Cor dourada para o curso com maior faturamento
    elif nome_curso in top_cursos.values:
        return '#32CD32'  # Verde suave para o curso com mais vendas
    return '#87CEEB'  # Azul claro para os demais cursos

# Aplicar a função de cor às barras
dados_ordenados = dados_agrupados.sort_values('Quantidade de Vendas', ascending=True)
dados_ordenados['Cor'] = dados_ordenados['Nome do Curso'].apply(define_cor)

# Formatar valores de receita para exibição nas barras
def formata_receita(valor):
    """
    Função para formatar valores de receita com 'R$' e casas decimais.

    Args:
        valor (float): Valor da receita a ser formatado.

    Returns:
        str: Valor formatado como 'R$####,##'.
    """
    return f"R${valor:.2f}".replace('.', ',')

# Gráfico de barras horizontal para contar as categorias de cursos
plt.figure(figsize=(12, 6))
bars = plt.barh(dados_ordenados['Nome do Curso'], dados_ordenados['Quantidade de Vendas'], color=dados_ordenados['Cor'])
plt.title('Contagem de Vendas por Curso')
plt.xlabel('Quantidade de Vendas')

# Adicionar rótulos com valores de receita total nas barras
for bar, valor in zip(bars, dados_ordenados['Receita Total']):
    plt.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2, formata_receita(valor), va='center', ha='left')

# Definindo precisão nos ticks do eixo X
plt.xticks(rotation=45, ha='right')
plt.gca().xaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))  # Formato com uma casa decimal

# Adicionar legenda
legend_colors = {'Maior Faturamento': '#FFD700', 'Mais Vendas': '#32CD32'}
legend_handles = [plt.Rectangle((0,0), 1, 1, color=color) for color in legend_colors.values()]
receita_total_text = f'Receita Total: {formata_receita(receita_total)}'
plt.text(0.98, 0.20, receita_total_text, ha='right', va='bottom', transform=plt.gca().transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.5))
plt.legend(legend_handles, legend_colors.keys())
plt.tight_layout()
plt.show()

# Gráfico de dispersão para relação entre Quantidade de Vendas e Preço Unitário
plt.figure(figsize=(8, 6))
plt.scatter(dados_agrupados['Preço Unitário'], dados_agrupados['Quantidade de Vendas'], color='coral', alpha=0.7)
plt.title('Relação entre Preço Unitário e Quantidade de Vendas')
plt.xlabel('Preço Unitário')
plt.ylabel('Quantidade de Vendas')
plt.grid(True)

# Calcular a linha de tendência (regressão linear)
slope, intercept, r_value, p_value, std_err = linregress(dados_agrupados['Preço Unitário'], dados_agrupados['Quantidade de Vendas'])
line = slope * dados_agrupados['Preço Unitário'] + intercept
plt.plot(dados_agrupados['Preço Unitário'], line, color='blue', label='Linha de Tendência')

plt.legend()

plt.tight_layout()
plt.show()

# Gráficos de vendas ao longo do tempo (por dia)
# Converter a coluna de data para datetime, se necessário
dados['Data'] = pd.to_datetime(dados['Data'])

# Extrair o dia da data da venda
dados['Dia'] = dados['Data'].dt.day

# Agrupar os dados por dia
vendas_por_dia = dados.groupby('Dia')['Quantidade de Vendas'].sum()

# Determinar o limite para destacar os dias com mais vendas
limite_vendas = vendas_por_dia.max() * 0.8  # 80% do valor máximo

# Função para definir cor baseada na quantidade de vendas por dia
def define_cor_dia(dia):
    if vendas_por_dia[dia] > limite_vendas:
        return '#32CD32'  # Verde suave para os dias com mais vendas
    return '#87CEEB'  # Azul claro para os demais dias

# Aplicar a função de cor aos dias
cores_dias = [define_cor_dia(dia) for dia in vendas_por_dia.index]

# Gráfico de barras para vendas por dia
plt.figure(figsize=(12, 6))
plt.bar(vendas_por_dia.index, vendas_por_dia.values, color=cores_dias)
plt.title('Vendas por Dia')
plt.xlabel('Dia do Mês')
plt.ylabel('Quantidade de Vendas')
plt.xticks(range(1, 32))
plt.grid(True)

# Adicionar legenda para cores dos dias
legend_colors_dia = {'Mais Vendas': '#32CD32'}
legend_handles_dia = [plt.Rectangle((0,0), 1, 1, color=color) for color in legend_colors_dia.values()]
plt.legend(legend_handles_dia, legend_colors_dia.keys())

plt.tight_layout()
plt.show()

# Exibir a receita total
print(f"\nReceita Total Gerada: {descritivas['Receita Total']}")
