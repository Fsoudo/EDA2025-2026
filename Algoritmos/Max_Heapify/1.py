import math

def max_heapify(A, i, heap_size):
    """Mantém a propriedade de Max-Heap (descida do nó)."""
    l = 2 * i + 1
    r = 2 * i + 2
    
    if l < heap_size and A[l] > A[i]:
        largest = l
    else:
        largest = i
        
    if r < heap_size and A[r] > A[largest]:
        largest = r
        
    if largest != i:
        A[i], A[largest] = A[largest], A[i]
        max_heapify(A, largest, heap_size)

def build_max_heap(A):
    """Transforma um array desordenado num Max-Heap."""
    heap_size = len(A)
    # Começa do último nó que possui filhos e vai até a raiz
    for i in range(len(A) // 2 - 1, -1, -1):
        max_heapify(A, i, heap_size)

def display_heap(A):
    """Visualização básica da estrutura da árvore no terminal."""
    if not A:
        print("Heap vazio.")
        return

    n = len(A)
    height = int(math.log2(n)) + 1
    
    print("\n--- Estrutura do Max-Heap ---")
    i = 0
    for level in range(height):
        # Espaçamento para centralizar os níveis
        spaces = " " * (2**(height - level + 1))
        between = " " * (2**(height - level + 2) - 2)
        
        level_nodes = A[i : i + 2**level]
        row = spaces + between.join(str(node).zfill(2) for node in level_nodes)
        print(row)
        i += 2**level
    print("-" * 30 + "\n")

# --- Teste do Código ---
if __name__ == "__main__":
    # Exemplo: Array totalmente desordenado
    data = [4, 1, 3, 2, 16, 9, 10, 14, 8, 7]
    
    print("Array original:", data)
    
    # 1. Transformar em Heap
    build_max_heap(data)
    
    print("Array após Build-Max-Heap:", data)
    
    # 2. Visualizar a árvore
    display_heap(data)