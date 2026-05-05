// ============================================================
//  Merge Sort — Implementação em Java
//  Disciplina: Estruturas de Dados e Algoritmos
//  Técnica: Divisão e Conquista
//  Complexidade: Θ(n log n)
// ============================================================

import java.util.Arrays;

public class MergeSort {

    // ----------------------------------------------------------
    // merge: funde A[p..q] e A[q+1..r] (ambas já ordenadas)
    //        em A[p..r] ordenada.
    // ----------------------------------------------------------
    private static void merge(int[] A, int p, int q, int r) {
        int n1 = q - p + 1;  // tamanho da sub-tabela esquerda
        int n2 = r - q;       // tamanho da sub-tabela direita

        // Criar arrays auxiliares (com espaço para a sentinela)
        int[] L = new int[n1 + 1];
        int[] R = new int[n2 + 1];

        // Copiar dados para L e R
        for (int i = 0; i < n1; i++) L[i] = A[p + i];
        for (int j = 0; j < n2; j++) R[j] = A[q + j + 1];

        // Colocar sentinelas no fim
        L[n1] = Integer.MAX_VALUE;
        R[n2] = Integer.MAX_VALUE;

        int i = 0, j = 0;

        // Preencher A[p..r] com os elementos ordenados
        for (int k = p; k <= r; k++) {
            if (L[i] <= R[j]) {
                A[k] = L[i];
                i++;
            } else {
                A[k] = R[j];
                j++;
            }
        }
    }

    // ----------------------------------------------------------
    // mergeSort: ordena A[p..r] por divisão e conquista
    // ----------------------------------------------------------
    public static void mergeSort(int[] A, int p, int r) {
        if (p < r) {
            int q = (p + r) / 2;       // ponto de divisão ⌊(p+r)/2⌋
            mergeSort(A, p, q);         // conquistar — lado esquerdo
            mergeSort(A, q + 1, r);     // conquistar — lado direito
            merge(A, p, q, r);          // combinar
        }
    }

    // ----------------------------------------------------------
    // Programa Principal
    // ----------------------------------------------------------
    public static void main(String[] args) {
        int[] A = {38, 27, 43, 3, 9, 82, 10};

        System.out.println("Antes:  " + Arrays.toString(A));

        mergeSort(A, 0, A.length - 1);

        System.out.println("Depois: " + Arrays.toString(A));
        // Resultado esperado: [3, 9, 10, 27, 38, 43, 82]
    }
}
