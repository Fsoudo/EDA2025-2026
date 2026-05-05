import numpy as np
import matplotlib.pyplot as plt

# 1. Configurações
n = 100000
media_masc, sigma_masc = 178, 7
media_fem, sigma_fem = 168, 7

# 2. Gerar os dados
alturas_masc = np.random.normal(media_masc, sigma_masc, n)
alturas_fem = np.random.normal(media_fem, sigma_fem, n)

# 3. Impressão no Terminal (Linha a linha)
print(f"{'ID':<10} | {'Masculino (cm)':<15} | {'Feminino (cm)':<15}")
print("-" * 45)

for i in range(n):
    print(f"Pessoa {i+1:04d} | {alturas_masc[i]:.2f}          | {alturas_fem[i]:.2f}")

# Resumo estatístico
print("-" * 45)
print(f"Média Real Masc: {np.mean(alturas_masc):.2f}cm")
print(f"Média Real Fem:  {np.mean(alturas_fem):.2f}cm")

# 4. Gráfico Conjunto
plt.figure(figsize=(12, 7))

# Histograma Masculino (Azul)
plt.hist(alturas_masc, bins=40, alpha=0.5, label='Masculino (178cm)', color='skyblue', edgecolor='black')

# Histograma Feminino (Rosa)
plt.hist(alturas_fem, bins=40, alpha=0.5, label='Feminino (168cm)', color='pink', edgecolor='black')

# Linhas das médias
plt.axvline(media_masc, color='blue', linestyle='dashed', linewidth=2, label=f'Média Masc: {media_masc}')
plt.axvline(media_fem, color='red', linestyle='dashed', linewidth=2, label=f'Média Fem: {media_fem}')

# Formatação do Gráfico
plt.title('Comparação de Alturas: Masculino vs Feminino')
plt.xlabel('Altura (cm)')
plt.ylabel('Frequência')
plt.legend()
plt.grid(axis='y', alpha=0.3)

# Mostrar o gráfico
plt.tight_layout()
print("\nA abrir o gráfico comparativo...")
plt.show()