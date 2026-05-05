#include <stdio.h>
#include <stdlib.h>

void imprimir_A(int*, int n)
{
    for (int j=1; j <n+1; j++)
    {
        printf("%d", A[j]);
    }
}
void insertion_sort(int* A, int n)
{
    int key;
    int i;
    int count =0;
    for(int j=2; j<=n;j++)
    {
        printf("j = %d", j);

        key= A [j];
        i=j-1;
        while( i >0 && A[i]>key)
        {
            printf("  i= %d", i);
            A[i+1] = A[i];
            i = i-1;
            count++;
        }
        A[i+1]= key;
    }
    printf("count = %d\n", count);
}

void main()
{
    const int N = 6;
    int* A = (int*) malloc(sizeof(int) * (N+1));
    A[0] = 0;
    A[1] = 5;
    A[2] = 2;
    A[3] = 4;
    A[4] = 6;
    A[5] = 1;
    A[6] = 3;
    imprimir_A(A,N);

    intsertion_sort(A,N);
    printf("\n");

    free( A );
}