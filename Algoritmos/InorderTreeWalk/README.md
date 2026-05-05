# Inorder Tree Walk - Documentação

Este projeto é uma visualização interativa do algoritmo **Inorder Tree Walk** (Percorrimento em Ordem) utilizando Python e a biblioteca gráfica Tkinter.

## 1. O que é o Inorder Tree Walk?

O percorrimento **Inorder** é um dos três tipos clássicos de percorrimento de árvores binárias (junto com Preorder e Postorder). Em uma Árvore Binária de Busca (BST), este percorrimento visita os nós de forma a resultar em uma sequência **ordenada** dos valores.

### A Ordem de Visita (Crescente):
1.  **Esquerda**: Percorre recursivamente a subárvore esquerda.
2.  **Raiz**: Visita o nó atual (imprime ou processa o valor).
3.  **Direita**: Percorre recursivamente a subárvore direita.

### Ordem Decrescente (Reverse Inorder):
Para obter os valores do **maior para o menor**, basta inverter a ordem das subárvores:
1.  **Direita**: Percorre recursivamente a subárvore direita (valores maiores).
2.  **Raiz**: Visita o nó atual.
3.  **Esquerda**: Percorre recursivamente a subárvore esquerda (valores menores).

**Pseudocódigo (Crescente):**
```python
def inorder_walk(node):
    if node is not None:
        inorder_walk(node.left)
        print(node.value)
        inorder_walk(node.right)
```

**Pseudocódigo (Decrescente):**
```python
def reverse_inorder_walk(node):
    if node is not None:
        reverse_inorder_walk(node.right)
        print(node.value)
        reverse_inorder_walk(node.left)
```

### Outros Tipos de Percorrimento:
*   **Preorder (Raiz → Esquerda → Direita)**: Útil para copiar a estrutura da árvore.
*   **Postorder (Esquerda → Direita → Raiz)**: Útil para apagar a árvore ou calcular o tamanho de subárvores.

---

## 2. Complexidade do Algoritmo

Este algoritmo é extremamente eficiente para visitar todos os elementos de uma árvore:

-   **Complexidade Temporal**: $O(n)$, onde $n$ é o número de nós na árvore, pois cada nó é visitado exatamente uma vez.
-   **Complexidade Espacial**: $O(h)$, onde $h$ é a altura da árvore, devido à pilha de chamadas da recursão. Em uma árvore equilibrada, isto é $O(\log n)$.

---

## 3. Como Funciona a Visualização

A aplicação foi desenhada para tornar o conceito abstrato da recursão algo visual e fácil de entender.

### Legenda de Cores:
-   **Nó Cinza**: Estado inicial (não visitado).
-   **Nó Azul**: O algoritmo está a "explorar" a subárvore deste nó (descendo na recursão).
-   **Nó Amarelo**: O algoritmo chegou ao passo de "visitar" a Raiz (o passo central do Inorder).
-   **Nó Verde**: O nó foi processado e adicionado à lista de resultados final.

### Controlos e Funcionalidades:
-   **Começar Inorder Walk**: Inicia a jornada recursiva. O botão fica desativado durante a execução para evitar conflitos.
-   **Reiniciar**: Interrompe qualquer animação em curso e reseta as cores para o estado original.
-   **Velocidade**: Um slider que permite ajustar o delay entre passos (de 0.1s a 2.0s).
-   **Resultado em Tempo Real**: Uma etiqueta na parte inferior mostra os valores à medida que são "visitados", permitindo confirmar a ordem crescente.
-   **Árvore Exemplo**: O programa gera automaticamente uma árvore equilibrada com 15 nós (valores de 15 a 85) para uma demonstração clara.

---

## 4. Detalhes Técnicos

### Estrutura do Código:
-   `Node`: Classe que representa um nó da árvore, contendo o valor, ponteiros para os filhos e coordenadas `(x, y)` para o desenho.
-   `BST`: Implementação da Árvore Binária de Busca com lógica de inserção automática.
-   `TreeVisualizer`: A classe principal que gere a interface gráfica (`Tkinter`), o desenho no `Canvas` e a animação através de *threading*.

### Requisitos:
-   Python 3.x
-   Biblioteca `tkinter` (incluída por padrão na maioria das instalações de Python).

---

## 5. Como Executar

Navegue até à pasta do projeto e execute:

```bash
python inorder_walk.py
```

---

*Desenvolvido como material de apoio para a unidade de Estruturas de Dados e Algoritmos.*
