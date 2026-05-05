# ============================================================
#  Fibonacci - Solucao Rapida com Memorizacao (Memoization)
#  Estruturas de Dados e Algoritmos
# ============================================================
#
#  Problema da recursividade simples:
#    fibonacci(n) chama fibonacci(n-1) e fibonacci(n-2)
#    Isso causa recalculos repetidos -> O(2^n)
#
#  Solucao - Memorizacao:
#    Guardar os resultados ja calculados num dicionario.
#    Se o valor ja foi calculado, retorna diretamente -> O(n)
# ============================================================

import time

# Dicionario que serve de cache (memoria) dos resultados ja calculados
_cache = {}

def fibonacci_memo(n):
    """
    Calcula o n-esimo numero de Fibonacci usando memoization.

    Em vez de recalcular subproblemas repetidos, guarda cada
    resultado no dicionario _cache na primeira vez que e calculado.
    Nas chamadas seguintes, retorna imediatamente o valor guardado.

    Complexidade:
        Tempo : O(n)   <- cada valor e calculado apenas 1 vez
        Espaco: O(n)   <- cache com n entradas

    Parametro:
        n (int): posicao na sequencia de Fibonacci (>= 0)

    Retorna:
        int: o n-esimo numero de Fibonacci
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("O argumento deve ser um inteiro nao negativo.")

    # Casos base
    if n == 0:
        return 0
    if n == 1:
        return 1

    # Se ja foi calculado antes, retorna da cache diretamente
    if n in _cache:
        return _cache[n]

    # Calcula e guarda na cache antes de retornar
    _cache[n] = fibonacci_memo(n - 1) + fibonacci_memo(n - 2)
    return _cache[n]


# ---- Versao recursiva simples (para comparacao) ----------------
def fibonacci_recursivo(n):
    """Versao recursiva simples - O(2^n) - usada apenas para comparacao."""
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci_recursivo(n - 1) + fibonacci_recursivo(n - 2)


# ---- Mostrar sequencia com tempo por entrada -------------------
def mostrar_sequencia(limite):
    print(f"\nSequencia de Fibonacci com memoization (indice 0 ao {limite}):")
    print("-" * 55)
    print(f"  {'indice':^8} | {'valor':^10} | {'tempo (s)':^16}")
    print("-" * 55)
    for i in range(limite + 1):
        _cache.clear()           # limpa cache para medir tempo real de cada calculo
        inicio = time.perf_counter()
        valor = fibonacci_memo(i)
        tempo_calculo = time.perf_counter() - inicio
        print(f"  fibonacci({i:>2}) = {valor:<10} | {tempo_calculo:.8f} s")
    print("-" * 55)


# ---- Comparacao direta: recursivo vs memoization --------------
def comparar(n):
    print(f"\n  Comparacao de desempenho para fibonacci({n}):")
    print("  " + "-" * 50)

    # Recursivo simples
    inicio = time.perf_counter()
    resultado_rec = fibonacci_recursivo(n)
    tempo_rec = time.perf_counter() - inicio

    # Memoization (cache limpa para medicao justa)
    _cache.clear()
    inicio = time.perf_counter()
    resultado_memo = fibonacci_memo(n)
    tempo_memo = time.perf_counter() - inicio

    print(f"  Recursivo simples : {resultado_rec}  ({tempo_rec:.8f} s)")
    print(f"  Memoization       : {resultado_memo}  ({tempo_memo:.8f} s)")

    if tempo_memo > 0:
        aceleracao = tempo_rec / tempo_memo
        print(f"  Memoization foi {aceleracao:.1f}x mais rapida!")
    print("  " + "-" * 50)


# ---- Execucao principal ---------------------------------------
if __name__ == "__main__":
    tempo_inicio_total = time.perf_counter()  # inicia temporizador global

    print("=" * 55)
    print("   FIBONACCI RAPIDO - MEMOIZATION (cache)")
    print("=" * 55)

    # Sequencia de 0 a 10
    mostrar_sequencia(10)

    # Comparacao de desempenho para um valor mais alto
    comparar(30)

    # Input do utilizador
    print()
    try:
        entrada = int(input("  Introduza um indice para calcular: "))
        _cache.clear()
        inicio = time.perf_counter()
        resultado = fibonacci_memo(entrada)
        tempo_calculo = time.perf_counter() - inicio
        print(f"  fibonacci({entrada}) = {resultado}")
        print(f"  Tempo de calculo  : {tempo_calculo:.8f} segundos")
    except ValueError as e:
        print(f"  Erro: {e}")

    # Tempo total do programa
    tempo_total = time.perf_counter() - tempo_inicio_total
    print()
    print("=" * 55)
    print(f"  Tempo total de execucao: {tempo_total:.6f} segundos")
    print("=" * 55)
