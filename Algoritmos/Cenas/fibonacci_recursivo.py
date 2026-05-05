# ============================================================
#  Fibonacci - Solução Recursiva
#  Estruturas de Dados e Algoritmos
# ============================================================
import time

def fibonacci(n):
    """
    Calcula o n-ésimo número de Fibonacci usando recursividade.

    Casos base:
        fibonacci(0) = 0
        fibonacci(1) = 1

    Caso recursivo:
        fibonacci(n) = fibonacci(n-1) + fibonacci(n-2)

    Parâmetro:
        n (int): posição na sequência de Fibonacci (>= 0)

    Retorna:
        int: o n-ésimo número de Fibonacci
    """
    # Validação da entrada
    if not isinstance(n, int) or n < 0:
        raise ValueError("O argumento deve ser um inteiro não negativo.")

    # Casos base
    if n == 0:
        return 0
    if n == 1:
        return 1

    # Caso recursivo
    return fibonacci(n - 1) + fibonacci(n - 2)


def mostrar_sequencia(limite):
    """
    Mostra a sequência de Fibonacci do índice 0 até 'limite' (inclusive).

    Parâmetro:
        limite (int): último índice a apresentar
    """
    print(f"\nSequencia de Fibonacci (do indice 0 ao {limite}):")
    print("-" * 55)
    print(f"  {'indice':^8} | {'valor':^10} | {'tempo (s)':^16}")
    print("-" * 55)
    for i in range(limite + 1):
        inicio = time.perf_counter()
        valor = fibonacci(i)
        tempo_calculo = time.perf_counter() - inicio
        print(f"  fibonacci({i:>2}) = {valor:<10} | {tempo_calculo:.8f} s")
    print("-" * 55)


# ─── Execução principal ───────────────────────────────────────
if __name__ == "__main__":
    tempo_inicio_total = time.perf_counter()  # inicia temporizador global

    print("=" * 45)
    print("   FIBONACCI RECURSIVO - RECURSIVIDADE")
    print("=" * 45)

    # Mostrar a sequência até ao índice 10
    mostrar_sequencia(10)

    # Exemplo isolado com medicao de tempo
    print()
    n = 7
    inicio = time.perf_counter()
    resultado = fibonacci(n)
    tempo_calculo = time.perf_counter() - inicio
    print(f"  fibonacci({n}) = {resultado}")
    print(f"  Tempo de calculo: {tempo_calculo:.8f} segundos")

    # Permitir ao utilizador introduzir um valor
    print()
    try:
        entrada = int(input("  Introduza um indice para calcular: "))
        inicio = time.perf_counter()
        resultado_entrada = fibonacci(entrada)
        tempo_calculo = time.perf_counter() - inicio
        print(f"  fibonacci({entrada}) = {resultado_entrada}")
        print(f"  Tempo de calculo: {tempo_calculo:.8f} segundos")
    except ValueError as e:
        print(f"  Erro: {e}")

    # Tempo total do programa
    tempo_total = time.perf_counter() - tempo_inicio_total
    print()
    print("=" * 45)
    print(f"  Tempo total de execucao: {tempo_total:.6f} segundos")
    print("=" * 45)
