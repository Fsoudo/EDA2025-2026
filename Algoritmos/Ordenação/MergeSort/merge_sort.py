# ============================================================
#  Merge Sort — Implementação em Python
#  Disciplina: Estruturas de Dados e Algoritmos
#  Técnica: Divisão e Conquista
#  Complexidade: Θ(n log n)
# ============================================================


def merge(A: list, p: int, q: int, r: int) -> None:
    """
    Funde duas sub-listas ordenadas em uma só.
      A[p..q]   — sub-lista esquerda (já ordenada)
      A[q+1..r] — sub-lista direita  (já ordenada)
    Resultado: A[p..r] fica ordenada.
    """
    n1 = q - p + 1   # tamanho da sub-lista esquerda
    n2 = r - q        # tamanho da sub-lista direita

    # Copiar para listas auxiliares
    L = A[p : q + 1]          # A[p..q]
    R = A[q + 1 : r + 1]      # A[q+1..r]

    # Sentinelas (valor infinito no fim de cada lista auxiliar)
    SENTINELA = float('inf')
    L.append(SENTINELA)
    R.append(SENTINELA)

    i = 0  # índice para L
    j = 0  # índice para R

    # Preencher A[p..r] com os elementos ordenados
    for k in range(p, r + 1):
        if L[i] <= R[j]:
            A[k] = L[i]
            i += 1
        else:
            A[k] = R[j]
            j += 1


def merge_sort(A: list, p: int, r: int) -> None:
    """
    Ordena A[p..r] usando a técnica de divisão e conquista.
      p — índice inicial (inclusive)
      r — índice final   (inclusive)
    """
    if p < r:
        q = (p + r) // 2          # ponto de divisão ⌊(p+r)/2⌋
        merge_sort(A, p, q)        # conquistar — lado esquerdo
        merge_sort(A, q + 1, r)    # conquistar — lado direito
        merge(A, p, q, r)          # combinar


# ============================================================
#  Programa Principal
# ============================================================
if __name__ == "__main__":
    # Exemplo de uso
    A = [38, 27, 43, 3, 9, 82, 10]
    print("Antes:", A)

    merge_sort(A, 0, len(A) - 1)

    print("Depois:", A)
    # Resultado esperado: [3, 9, 10, 27, 38, 43, 82]
