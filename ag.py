import random
import numpy as np
import matplotlib.pyplot as plt

# Definição do problema da mochila
valores = [60, 100, 120, 90, 50, 70, 30, 80, 110, 40, 95, 85, 55, 65, 75]
pesos = [10, 20, 30, 15, 25, 35, 10, 20, 40, 15, 25, 18, 28, 22, 12]
capacidade = 100
num_itens = len(valores)
populacao_size = 1000
num_geracoes = 1000
taxa_mutacao = 0.1
num_execucoes = 100  # Número de execuções para coleta de dados

# Função de aptidão
def fitness(individuo):
    valor_total = 0
    peso_total = 0
    for i in range(num_itens):
        if individuo[i] == 1:
            valor_total += valores[i]
            peso_total += pesos[i]
    return valor_total if peso_total <= capacidade else 0

# Seleção por roleta
def selecao_roleta(populacao, fitnesses):
    soma_fitness = sum(fitnesses)
    ponto_roleta = random.uniform(0, soma_fitness)
    atual = 0
    for i, fitness in enumerate(fitnesses):
        atual += fitness
        if atual >= ponto_roleta:
            return populacao[i]

# Mutação uniforme
def mutacao(individuo):
    for i in range(num_itens):
        if random.random() < taxa_mutacao:
            individuo[i] = 1 - individuo[i]
    return individuo

# Algoritmo genético
melhores_valores_finais = []  # Para armazenar os melhores valores finais de cada execução
melhores_valores_geracao = []  # Para armazenar os melhores valores de cada geração

for execucao in range(num_execucoes):
    populacao = [[random.randint(0, 1) for _ in range(num_itens)] for _ in range(populacao_size)]
    melhor_valor_execucao = 0  # Melhor valor da execução
    melhores_valores_geracao_execucao = []  # Melhores valores de cada geração da execução

    for geracao in range(num_geracoes):
        fitnesses = [fitness(individuo) for individuo in populacao]
        melhor_valor = max(fitnesses)
        melhores_valores_geracao_execucao.append(melhor_valor)
        
        if melhor_valor > melhor_valor_execucao:
            melhor_valor_execucao = melhor_valor

        nova_populacao = []
        for _ in range(populacao_size):
            pai1 = selecao_roleta(populacao, fitnesses)
            pai2 = selecao_roleta(populacao, fitnesses)
            ponto_corte = random.randint(1, num_itens - 1)
            filho = pai1[:ponto_corte] + pai2[ponto_corte:]
            filho = mutacao(filho)
            nova_populacao.append(filho)
        populacao = nova_populacao

    melhores_valores_finais.append(melhor_valor_execucao)
    melhores_valores_geracao.append(melhores_valores_geracao_execucao)

# Preparação dos dados para o gráfico
melhores_valores_geracao = np.array(melhores_valores_geracao)
melhores_valores_finais = np.array(melhores_valores_finais)

# Plot dos resultados
plt.figure(figsize=(18, 5))

# Gráfico dos melhores valores ao longo das gerações
plt.subplot(1, 2, 1)
for i in range(num_execucoes):
    plt.plot(melhores_valores_geracao[i], label=f'Execução {i+1}')
plt.xlabel('Geração')
plt.ylabel('Melhor Valor')
plt.title('Melhor Valor por Geração em Múltiplas Execuções')
plt.legend()
plt.grid()

# Gráfico dos melhores valores finais de cada execução
plt.subplot(1, 2, 2)
plt.bar(range(num_execucoes), melhores_valores_finais, color='blue', edgecolor='black')
plt.xlabel('Execução')
plt.ylabel('Melhor Valor Final')
plt.title('Melhor Valor Final de Cada Execução')
plt.xticks(range(num_execucoes))
plt.grid()

plt.tight_layout()
plt.show()