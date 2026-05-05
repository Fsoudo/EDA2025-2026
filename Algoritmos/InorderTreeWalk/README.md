# Visualizações de Algoritmos de Árvores (EDA)

Este diretório contém ferramentas interativas em Python para o estudo de **Árvores Binárias de Busca (BST)**. As visualizações foram desenhadas para tornar conceitos abstratos em experiências visuais claras.

---

## 1. Algoritmos Disponíveis

### 🌳 Inorder Tree Walk (Equilibrado)
-   **Ficheiro**: `inorder_walk.py`
-   **Conceito**: Percorre a árvore na ordem **Esquerda -> Raiz -> Direita**.
-   **Destaque**: Mostra como uma árvore equilibrada permite um percorrimento eficiente que resulta em valores ordenados.
-   **Funcionalidade Extra**: Inclui um rasto (trace) no terminal e contador de iterações.

### 📉 Inorder Tree Walk (Degenerada à Direita)
-   **Ficheiro**: `inorder_walk_right.py`
-   **Conceito**: Demonstra uma árvore onde cada nó só tem filhos à direita (Right-Skewed).
-   **Destaque**: Útil para observar como o algoritmo se comporta quando a árvore perde a sua forma ideal e se assemelha a uma lista ligada.
-   **Análise**: Notará que a recursão para a esquerda é quase instantânea (nó é sempre `None`), focando-se na descida diagonal.

### 🔍 BST Search (Pesquisa Binária)
-   **Ficheiro**: `bst_search.py`
-   **Conceito**: Procura um valor específico na árvore.
-   **Destaque**: Em vez de visitar todos os nós, o algoritmo decide o caminho (`Esquerda` ou `Direita`) com base em comparações.
-   **Painel de Passos**: Inclui um mostrador grande de **PASSOS** que indica quão eficiente foi a procura. Se a árvore tiver altura $h$, a pesquisa levará no máximo $h+1$ passos.

---

## 2. Guia Visual (Cores e Status)

Todas as visualizações utilizam o mesmo sistema de cores para facilitar a aprendizagem:

| Cor | Significado | Fase do Algoritmo |
|---|---|---|
| **Cinzento (`#313244`)** | Por visitar | Estado inicial do nó. |
| **Azul (`#89b4fa`)** | Exploração | O algoritmo está a descer para uma subárvore. |
| **Amarelo (`#f9e2af`)** | Comparação / Raiz | O nó está a ser "processado" ou comparado com o alvo. |
| **Verde (`#a6e3a1`)** | Sucesso / Visitado | O nó foi visitado (Inorder) ou encontrado (Search). |
| **Vermelho (`#f38ba8`)** | Base / Falha | Chegou a um nó nulo ou o valor não existe. |

---

## 3. Análise de Complexidade

Todos os algoritmos de manipulação direta (Pesquisa e Inserção) dependem da altura da árvore:

-   **Tempo de Execução**: $O(h)$, onde $h$ é a altura da árvore.
    -   Numa árvore **equilibrada**: $h \approx \log_2 n \implies O(\log n)$.
    -   Numa árvore **degenerada** (como a `inorder_walk_right.py`): $h = n \implies O(n)$.
-   **Espaço**:
    -   Versões **Iterativas**: $O(1)$ (apenas ponteiros).
    -   Versões **Recursivas**: $O(h)$ (devido à pilha de chamadas).

---

## 4. Informação de Iterações e Argumentos

Adicionámos funcionalidades de "debug" pedagógico em todos os scripts:

1.  **Etiqueta de Status**: No topo de cada janela, poderá ler o **Argumento Atual** que a função recebeu (ex: `Nó(50)` ou `None`).
2.  **Contador de Iterações**: Indica quantas chamadas recursivas foram feitas no total. Isto ajuda a visualizar a complexidade espacial e temporal.
3.  **Trace no Terminal**: Para quem gosta de analisar código, o terminal imprime o fluxo completo:
    ```text
    --> Chamada #1 | Processando Nó: 6
      [6] Indo para a ESQUERDA...
    --> Chamada #2 | Processando Nó: 5
    ```

---

## 4. Como Executar

Certifique-se de que tem o Python instalado e execute o script pretendido:

```bash
# Para o percorrimento padrão
python inorder_walk.py

# Para a árvore degenerada
python inorder_walk_right.py

# Para a pesquisa interativa
python bst_search.py

# Para a pesquisa iterativa
4.  **Pesquisa Iterativa (BST Search Iterative)**:
    Demonstra como procurar um valor usando um ciclo `while`, sem recorrer a funções recursivas. É a versão mais eficiente em termos de memória.
5.  **Inserção Iterativa (BST Insert Iterative)**:
    Implementação fiel ao pseudocódigo `TREE-INSERT(T, z)` do livro CLRS. Mostra os ponteiros `x` e `y` a navegar na árvore até encontrar a posição correta.
    ```bash
    python bst_insert_iterative.py
    ```

---

*Material desenvolvido para a unidade de Estruturas de Dados e Algoritmos — Francisco Soudo.*
