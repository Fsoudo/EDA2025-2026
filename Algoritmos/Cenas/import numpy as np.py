import numpy as np
import matplotlib.pyplot as plt

# 1. Definição dos parâmetros
media = 178
sigma = 10
quantidade = 1000

# 2. Gerar os 1000 números
numeros = np.random.normal(loc=media, scale=sigma, size=quantidade)

# 3. Imprimir os valores linha a linha no terminal
print(f"--- Listagem de {quantidade} alturas (média 178, sigma 10) ---")
for i, n in enumerate(numeros, 1):
    print(f"Número {i:04d}: {n:.2f} cm")

print("-" * 50)
print(f"Impressão concluída!")
print(f"Média real da amostra: {np.mean(numeros):.2f} cm")
print(f"Desvio padrão real: {np.std(numeros):.2f} cm")
print("-" * 50)

# 4. Criar e exibir o gráfico
plt.figure(figsize=(10, 6))
plt.hist(numeros, bins=40, color='skyblue', edgecolor='black', alpha=0.7)

# Adicionar detalhes ao gráfico
plt.title('Distribuição de Alturas Geradas (1000 amostras)')
plt.xlabel('Altura (cm)')
plt.ylabel('Frequência')
plt.axvline(media, color='red', linestyle='dashed', linewidth=2, label=f'Média Alvo ({media}cm)')
plt.legend()
plt.grid(axis='y', alpha=0.3)

# Mostrar o gráfico
print("A abrir o gráfico...")
plt.show()