/* ============================================================
   Merge Sort — Implementação em C
   Disciplina: Estruturas de Dados e Algoritmos
   Técnica: Divisão e Conquista
   Complexidade: Θ(n log n)
   ============================================================ */

#include <stdio.h>
#include <stdlib.h>
#include <limits.h>  /* INT_MAX — usado como sentinela */

/* ------------------------------------------------------------
   merge: funde A[p..q] e A[q+1..r] (ambas já ordenadas)
          em A[p..r] ordenada.
   ------------------------------------------------------------ */
void merge(int A[], int p, int q, int r) {
    int n1 = q - p + 1;  /* tamanho da sub-tabela esquerda */
    int n2 = r - q;       /* tamanho da sub-tabela direita  */

    /* Alocar listas auxiliares com espaço para a sentinela */
    int *L = (int *)malloc((n1 + 1) * sizeof(int));
    int *R = (int *)malloc((n2 + 1) * sizeof(int));

    /* Copiar dados para L e R */
    for (int i = 0; i < n1; i++) L[i] = A[p + i];
    for (int j = 0; j < n2; j++) R[j] = A[q + j + 1];

    /* Colocar sentinelas no fim */
    L[n1] = INT_MAX;
    R[n2] = INT_MAX;

    int i = 0, j = 0;

    /* Preencher A[p..r] com os elementos ordenados */
    for (int k = p; k <= r; k++) {
        if (L[i] <= R[j]) {
            A[k] = L[i];
            i++;
        } else {
            A[k] = R[j];
            j++;
        }
    }

    free(L);
    free(R);
}

/* ------------------------------------------------------------
   merge_sort: ordena A[p..r] por divisão e conquista
   ------------------------------------------------------------ */
void merge_sort(int A[], int p, int r) {
    if (p < r) {
        int q = (p + r) / 2;      /* ponto de divisão ⌊(p+r)/2⌋ */
        merge_sort(A, p, q);       /* conquistar — lado esquerdo  */
        merge_sort(A, q + 1, r);   /* conquistar — lado direito   */
        merge(A, p, q, r);         /* combinar                    */
    }
}

/* ------------------------------------------------------------
   Utilitário: imprimir array
   ------------------------------------------------------------ */
void print_array(int A[], int n) {
    printf("[");
    for (int i = 0; i < n; i++) {
        printf("%d", A[i]);
        if (i < n - 1) printf(", ");
    }
    printf("]\n");
}

/* ------------------------------------------------------------
   Programa Principal
   ------------------------------------------------------------ */
int main(void) {
    int A[] = {38, 27, 43, 3, 9, 82, 10};
    int n = sizeof(A) / sizeof(A[0]);

    printf("Antes:  ");
    print_array(A, n);

    merge_sort(A, 0, n - 1);

    printf("Depois: ");
    print_array(A, n);
    /* Resultado esperado: [3, 9, 10, 27, 38, 43, 82] */

    return 0;
}
