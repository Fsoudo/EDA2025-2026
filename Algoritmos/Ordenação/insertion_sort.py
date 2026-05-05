def imprimir_A(A, n):
    elementos = " | ".join(str(A[j]) for j in range(1, n + 1))
    print(f"  Array: [ {elementos} ]")


def insertion_sort(A, n):
    count = 0
    print("\n--- Inicio do Insertion Sort ---")
    for j in range(2, n + 1):
        key = A[j]
        i = j - 1

        print(f"\n  Iteracao j={j}  =>  key={key}")

        while i > 0 and A[i] > key:
            print(f"    Mover A[{i}]={A[i]} para A[{i+1}]  (i={i})")
            A[i + 1] = A[i]
            i = i - 1
            count += 1

        A[i + 1] = key
        imprimir_A(A, n)

    print(f"\n--- Fim do Insertion Sort ---")
    print(f"  Total de movimentos: {count}")


def main():
    N = 6
    # Índice 0 não é usado (como no código C original)
    A = [0, 5, 2, 4, 6, 1, 3]  # A[0]=0, A[1]=5, ... A[6]=3

    print("=== Insertion Sort ===")
    print("\nArray inicial:")
    imprimir_A(A, N)

    insertion_sort(A, N)

    print("\nArray ordenado:")
    imprimir_A(A, N)


if __name__ == "__main__":
    main()
