import random
import numpy as np
import matplotlib.pyplot as plt

# Dados do problema: valores e pesos dos itens e capacidade da mochila
valores = [60, 100, 120, 90, 50, 70, 30, 80, 110, 40, 95, 85, 55, 65, 75]  # Valores dos itens
pesos = [10, 20, 30, 15, 25, 35, 10, 20, 40, 15, 25, 18, 28, 22, 12]  
capacidade = 100
num_itens = len(valores)
populacao_size = 1000
num_geracoes = 1000
taxa_mutacao = 0.1

# Função de aptidão
def fitness(individuo):
    valor_total = 0
    peso_total = 0
    for i in range(num_itens):
        if individuo[i] == 1:
            valor_total += valores[i]
            peso_total += pesos[i]
    if peso_total > capacidade:
        return 0
    else:
        return valor_total

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
populacao = [[random.randint(0, 1) for _ in range(num_itens)] for _ in range(populacao_size)]
melhores_valores = []
ciclos_melhores_valores = []
ultimos_valores = []

melhor_valor_global = 0
geracao_melhor_valor = 0

for geracao in range(num_geracoes):
    fitnesses = [fitness(individuo) for individuo in populacao]
    nova_populacao = []
    
    # Gerar nova população
    for _ in range(populacao_size):
        pai1 = selecao_roleta(populacao, fitnesses)
        pai2 = selecao_roleta(populacao, fitnesses)
        ponto_corte = random.randint(1, num_itens - 1)
        filho = pai1[:ponto_corte] + pai2[ponto_corte:]
        filho = mutacao(filho)
        nova_populacao.append(filho)
        
    populacao = nova_populacao
    
    # Capturar melhores valores e ciclos
    melhor_valor = max(fitnesses)
    ultimos_valores.append(fitnesses[-1])
    melhores_valores.append(melhor_valor)
    
    if melhor_valor > melhor_valor_global:
        melhor_valor_global = melhor_valor
        geracao_melhor_valor = geracao
    
    print(f'Geração {geracao+1}: Melhor valor = {melhor_valor}')

# Dados para os histogramas
ciclos_melhores_valores = [geracao_melhor_valor] * len(melhores_valores)

# Plot do histograma dos melhores valores
plt.figure(figsize=(18, 5))

# Histograma dos Melhores Valores
plt.subplot(1, 3, 1)
plt.hist(melhores_valores, bins=10, color='blue', alpha=0.75, edgecolor='black')
plt.xlabel('Melhor Valor')
plt.ylabel('Frequência')
plt.title('Histograma dos Melhores Valores')

# Histograma dos Ciclos do Melhor Valor
plt.subplot(1, 3, 2)
plt.hist(ciclos_melhores_valores, bins=10, color='green', alpha=0.75, edgecolor='black')
plt.xlabel('Ciclo do Melhor Valor')
plt.ylabel('Frequência')
plt.title('Histograma dos Ciclos do Melhor Valor')

# Histograma dos Últimos Valores
plt.subplot(1, 3, 3)
plt.hist(ultimos_valores, bins=10, color='red', alpha=0.75, edgecolor='black')
plt.xlabel('Último Valor')
plt.ylabel('Frequência')
plt.title('Histograma dos Últimos Valores')

plt.tight_layout()
plt.show()
