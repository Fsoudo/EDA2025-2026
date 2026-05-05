import numpy as np
import matplotlib.pyplot as plt

# 1. Definição dos parâmetros para o género feminino
media = 168       # Nova média: 168cm
sigma = 10        # Desvio padrão: 10cm
quantidade = 1000

# 2. Gerar os 1000 números seguindo a distribuição normal
# O parâmetro 'loc' define a média e 'scale' o desvio padrão
numeros = np.random.normal(loc=media, scale=sigma, size=quantidade)

# 3. Imprimir os valores linha a linha no terminal
print(f"--- Listagem de {quantidade} alturas femininas (Média: {media}cm) ---")
for i, valor in enumerate(numeros, 1):
    print(f"Mulher {i:04d}: {valor:.2f} cm")

# Resumo estatístico rápido no terminal
print("-" * 50)
print("Cálculos da amostra gerada:")
print(f"Média real: {np.mean(numeros):.2f} cm")
print(f"Desvio padrão real: {np.std(numeros):.2f} cm")
print("-" * 50)

# 4. Criar o gráfico (Histograma)
plt.figure(figsize=(10, 6))
plt.hist(numeros, bins=40, color='pink', edgecolor='black', alpha=0.7)

# Detalhes visuais do gráfico
plt.title(f'Distribuição de Alturas Femininas ($n=1000, \mu=168, \sigma=10$)')
plt.xlabel('Altura (cm)')
plt.ylabel('Frequência (Quantidade de pessoas)')
plt.axvline(media, color='purple', linestyle='dashed', linewidth=2, label=f'Média: {media}cm')
plt.legend()
plt.grid(axis='y', alpha=0.3)

# Exibir o gráfico
print("A abrir a janela do gráfico...")
plt.show()