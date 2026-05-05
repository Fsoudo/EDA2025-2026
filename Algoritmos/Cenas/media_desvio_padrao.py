import numpy as np
import matplotlib.pyplot as plt
import math

# ============================================================
#  Cálculo de Média e Desvio Padrão — Alturas Masculino/Feminino
#  Estruturas de Dados e Algoritmos
# ============================================================

# 1. Configurações
n = 100000
media_masc, sigma_masc = 178, 7
media_fem, sigma_fem = 168, 7

# 2. Gerar os dados
alturas_masc = np.random.normal(media_masc, sigma_masc, n)
alturas_fem  = np.random.normal(media_fem,  sigma_fem,  n)


# ------------------------------------------------------------
# 3. Funções manuais de média e desvio padrão
# ------------------------------------------------------------

def calcular_media(valores: list[float]) -> float:
    """Calcula a média aritmética de uma lista de valores."""
    if len(valores) == 0:
        raise ValueError("A lista não pode estar vazia.")
    return sum(valores) / len(valores)


def calcular_desvio_padrao(valores: list[float], populacional: bool = True) -> float:
    """
    Calcula o desvio padrão de uma lista de valores.

    Parâmetros:
        valores      – lista de números
        populacional – True  → divide por N   (desvio padrão populacional)
                       False → divide por N-1 (desvio padrão amostral)
    """
    if len(valores) == 0:
        raise ValueError("A lista não pode estar vazia.")
    if not populacional and len(valores) < 2:
        raise ValueError("São necessários pelo menos 2 valores para o desvio padrão amostral.")

    media = calcular_media(valores)
    n_val = len(valores)
    divisor = n_val if populacional else (n_val - 1)
    variancia = sum((x - media) ** 2 for x in valores) / divisor
    return math.sqrt(variancia)


# ------------------------------------------------------------
# 4. Resumo estatístico no terminal
# ------------------------------------------------------------

print(f"{'Estatística':<30} | {'Masculino':>12} | {'Feminino':>12}")
print("-" * 62)

# Média
print(f"{'Média (NumPy)':<30} | {np.mean(alturas_masc):>11.4f} | {np.mean(alturas_fem):>11.4f}")
print(f"{'Média (Manual)':<30} | {calcular_media(list(alturas_masc)):>11.4f} | {calcular_media(list(alturas_fem)):>11.4f}")

# Desvio Padrão
print(f"{'Desvio Padrão Pop. (NumPy)':<30} | {np.std(alturas_masc):>11.4f} | {np.std(alturas_fem):>11.4f}")
print(f"{'Desvio Padrão Pop. (Manual)':<30} | {calcular_desvio_padrao(list(alturas_masc), True):>11.4f} | {calcular_desvio_padrao(list(alturas_fem), True):>11.4f}")
print(f"{'Desvio Padrão Amostral (NumPy)':<30} | {np.std(alturas_masc, ddof=1):>11.4f} | {np.std(alturas_fem, ddof=1):>11.4f}")

print("-" * 62)
print(f"  Total de amostras por grupo: {n}")


# ------------------------------------------------------------
# 5. Gráfico Conjunto
# ------------------------------------------------------------

plt.figure(figsize=(12, 7))

# Histogramas
plt.hist(alturas_masc, bins=40, alpha=0.5, label='Masculino (178cm)', color='skyblue', edgecolor='black')
plt.hist(alturas_fem,  bins=40, alpha=0.5, label='Feminino (168cm)',  color='pink',    edgecolor='black')

# Linhas das médias
plt.axvline(media_masc, color='blue', linestyle='dashed', linewidth=2, label=f'Média Masc: {media_masc}cm')
plt.axvline(media_fem,  color='red',  linestyle='dashed', linewidth=2, label=f'Média Fem: {media_fem}cm')

# Desvio padrão — barras horizontais (±1σ)
plt.axvline(media_masc - sigma_masc, color='blue', linestyle='dotted', linewidth=1.2, label=f'±1σ Masc ({sigma_masc}cm)')
plt.axvline(media_masc + sigma_masc, color='blue', linestyle='dotted', linewidth=1.2)
plt.axvline(media_fem  - sigma_fem,  color='red',  linestyle='dotted', linewidth=1.2, label=f'±1σ Fem ({sigma_fem}cm)')
plt.axvline(media_fem  + sigma_fem,  color='red',  linestyle='dotted', linewidth=1.2)

# Formatação do Gráfico
plt.title('Comparação de Alturas: Masculino vs Feminino\nMédia e Desvio Padrão')
plt.xlabel('Altura (cm)')
plt.ylabel('Frequência')
plt.legend()
plt.grid(axis='y', alpha=0.3)

plt.tight_layout()
print("\nA abrir o gráfico comparativo...")
plt.show()
