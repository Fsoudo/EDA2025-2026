# ============================================================
#  Fibonacci - Solucoes Otimizadas
#  Estruturas de Dados e Algoritmos
#
#  Comparacao de 4 abordagens:
#   1. Recursivo simples    -> O(2^n)
#   2. Memoization          -> O(n)   tempo, O(n) espaco
#   3. Iterativo            -> O(n)   tempo, O(1) espaco
#   4. Fast Doubling        -> O(log n) tempo  <- o mais rapido
# ============================================================

import time


# ── 1. Recursivo simples (apenas para comparacao) ──────────────
def fibonacci_recursivo(n):
    if n <= 1:
        return n
    return fibonacci_recursivo(n - 1) + fibonacci_recursivo(n - 2)


# ── 2. Memoization ─────────────────────────────────────────────
_cache = {}
def fibonacci_memo(n):
    if n <= 1:
        return n
    if n in _cache:
        return _cache[n]
    _cache[n] = fibonacci_memo(n - 1) + fibonacci_memo(n - 2)
    return _cache[n]


# ── 3. Iterativo ───────────────────────────────────────────────
def fibonacci_iterativo(n):
    """
    Percorre a sequencia de forma iterativa, guardando apenas
    os dois valores anteriores. Sem recursao, sem cache.

    Complexidade:
        Tempo : O(n)
        Espaco: O(1)  <- apenas 2 variaveis em memoria
    """
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b   # desloca a janela de 2 valores
    return b


# ── 4. Fast Doubling ───────────────────────────────────────────
def fibonacci_fast_doubling(n):
    """
    Calcula fibonacci(n) usando a identidade matematica:
        F(2k)   = F(k) * (2*F(k+1) - F(k))
        F(2k+1) = F(k)^2 + F(k+1)^2

    Divide o problema a metade a cada passo -> O(log n).
    E o algoritmo mais rapido para calcular um unico F(n).

    Complexidade:
        Tempo : O(log n)
        Espaco: O(log n)  <- profundidade da recursao
    """
    if n < 0:
        raise ValueError("O argumento deve ser um inteiro nao negativo.")
    return _fast_doubling_helper(n)[0]

def _fast_doubling_helper(n):
    """Retorna o par (F(n), F(n+1))."""
    if n == 0:
        return (0, 1)
    fk, fk1 = _fast_doubling_helper(n >> 1)   # divide n a metade
    f2k   = fk * (2 * fk1 - fk)               # F(2k)
    f2k1  = fk * fk + fk1 * fk1               # F(2k+1)
    if n & 1:                                  # se n e impar
        return (f2k1, f2k + f2k1)
    else:
        return (f2k, f2k1)


# ── Comparacao de todas as abordagens ──────────────────────────
def comparar_todos(n, incluir_recursivo=True):
    print(f"\n  Comparacao para fibonacci({n}):")
    print("  " + "-" * 58)
    print(f"  {'Metodo':<22} | {'Resultado':>10} | {'Tempo (s)':>16}")
    print("  " + "-" * 58)

    resultados = {}

    if incluir_recursivo:
        t = time.perf_counter()
        resultados['Recursivo simples'] = fibonacci_recursivo(n)
        print(f"  {'Recursivo simples':<22} | {resultados['Recursivo simples']:>10} | {time.perf_counter()-t:>16.8f}")

    _cache.clear()
    t = time.perf_counter()
    resultados['Memoization'] = fibonacci_memo(n)
    print(f"  {'Memoization':<22} | {resultados['Memoization']:>10} | {time.perf_counter()-t:>16.8f}")

    t = time.perf_counter()
    resultados['Iterativo'] = fibonacci_iterativo(n)
    print(f"  {'Iterativo':<22} | {resultados['Iterativo']:>10} | {time.perf_counter()-t:>16.8f}")

    t = time.perf_counter()
    resultados['Fast Doubling'] = fibonacci_fast_doubling(n)
    print(f"  {'Fast Doubling O(log n)':<22} | {resultados['Fast Doubling']:>10} | {time.perf_counter()-t:>16.8f}")

    print("  " + "-" * 58)


# ── Sequencia com Fast Doubling ─────────────────────────────────
def mostrar_sequencia(limite):
    print(f"\nSequencia de Fibonacci - Fast Doubling (0 ao {limite}):")
    print("-" * 55)
    print(f"  {'indice':^8} | {'valor':^10} | {'tempo (s)':^16}")
    print("-" * 55)
    for i in range(limite + 1):
        inicio = time.perf_counter()
        valor = fibonacci_fast_doubling(i)
        tempo = time.perf_counter() - inicio
        print(f"  fibonacci({i:>2}) = {valor:<10} | {tempo:.8f} s")
    print("-" * 55)


# ── Execucao principal ─────────────────────────────────────────
if __name__ == "__main__":
    tempo_inicio_total = time.perf_counter()

    print("=" * 58)
    print("   FIBONACCI OTIMIZADO - FAST DOUBLING O(log n)")
    print("=" * 58)

    # Sequencia ate 10
    mostrar_sequencia(10)

    # Comparacao com n=30 (inclui recursivo)
    comparar_todos(30, incluir_recursivo=True)

    # Comparacao com n=100 (sem recursivo - seria demasiado lento)
    comparar_todos(100, incluir_recursivo=False)

    # Input do utilizador
    print()
    try:
        entrada = int(input("  Introduza um indice para calcular: "))
        inicio = time.perf_counter()
        resultado = fibonacci_fast_doubling(entrada)
        tempo_calculo = time.perf_counter() - inicio
        print(f"  fibonacci({entrada}) = {resultado}")
        print(f"  Tempo de calculo (Fast Doubling): {tempo_calculo:.8f} segundos")
    except ValueError as e:
        print(f"  Erro: {e}")

    # Tempo total
    tempo_total = time.perf_counter() - tempo_inicio_total
    print()
    print("=" * 58)
    print(f"  Tempo total de execucao: {tempo_total:.6f} segundos")
    print("=" * 58)
