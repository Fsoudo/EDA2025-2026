# Visualizações Interativas de Árvores Binárias de Busca (BST)

> Material pedagógico interativo para o estudo de algoritmos sobre **Árvores Binárias de Busca (BST)**.  
> Unidade Curricular: Estruturas de Dados e Algoritmos — Instituto Politécnico de Beja  
> Baseado no livro *Introduction to Algorithms* (CLRS, 4.ª edição).

---

## 📁 Scripts Disponíveis

| # | Ficheiro | Algoritmo | Referência CLRS |
|---|---|---|---|
| 1 | `inorder_walk.py` | Percorrimento Inorder (árvore equilibrada) | Cap. 12.1 |
| 2 | `inorder_walk_right.py` | Percorrimento Inorder (árvore degenerada à direita) | Cap. 12.1 |
| 3 | `bst_search.py` | Pesquisa Recursiva — `TREE-SEARCH(x, k)` | Cap. 12.2 |
| 4 | `bst_search_iterative.py` | Pesquisa Iterativa — `ITERATIVE-TREE-SEARCH(x, k)` | Cap. 12.2 |
| 5 | `bst_insert_iterative.py` | Inserção — `TREE-INSERT(T, z)` | Cap. 12.3 |
| 6 | `bst_delete.py` | Remoção — `TREE-DELETE(T, z)` + `TRANSPLANT(T, u, v)` | Cap. 12.3 |

---

## 1. Percorrimento Inorder — `inorder_walk.py` / `inorder_walk_right.py`

**Pseudocódigo:**
```
INORDER-TREE-WALK(x)
  if x != NIL
      INORDER-TREE-WALK(x.left)
      print x.key
      INORDER-TREE-WALK(x.right)
```

- **Ideia**: Visitar os nós na ordem **Esquerda → Raiz → Direita** produz os valores por ordem crescente.
- **`inorder_walk.py`**: Árvore equilibrada — mostra o fluxo recursivo completo com todas as subárvores.
- **`inorder_walk_right.py`**: Árvore degenerada (Right-Skewed) — cada nó só tem filho à direita. Demonstra o pior caso estrutural.
- **Extras**: Contador de iterações em tempo real e trace completo no terminal.
- **Complexidade**: Temporal $O(n)$ · Espacial $O(h)$ (pilha de recursão).

---

## 2. Pesquisa Recursiva — `bst_search.py`

**Pseudocódigo:**
```
TREE-SEARCH(x, k)
  if x == NIL or k == x.key
      return x
  if k < x.key
      return TREE-SEARCH(x.left, k)
  else
      return TREE-SEARCH(x.right, k)
```

- **Ideia**: Comparar o valor `k` com o nó atual e descer recursivamente para a subárvore correcta.
- **Painel de PASSOS**: Mostra o número de comparações efectuadas até ao resultado.
- **Legenda de cores**: Amarelo (a comparar) → Verde (encontrado) / Vermelho (não existe).
- **Complexidade**: $O(h)$.

---

## 3. Pesquisa Iterativa — `bst_search_iterative.py`

**Pseudocódigo:**
```
ITERATIVE-TREE-SEARCH(x, k)
  while x != NIL and k != x.key
      if k < x.key
          x = x.left
      else
          x = x.right
  return x
```

- **Ideia**: Equivalente à versão recursiva, mas sem consumir a pilha de chamadas.
- **Vantagem**: $O(1)$ de espaço adicional em vez de $O(h)$.
- **Visualização**: O ponteiro `curr` é destacado a cada iteração do ciclo `while`.
- **Complexidade**: Temporal $O(h)$ · Espacial $O(1)$.

---

## 4. Inserção Iterativa — `bst_insert_iterative.py`

**Pseudocódigo:**
```
TREE-INSERT(T, z)
  y = NIL
  x = T.root
  while x != NIL          ← usa dois ponteiros: x (atual) e y (pai)
      y = x
      if z.key < x.key
          x = x.left
      else
          x = x.right
  z.p = y
  if y == NIL
      T.root = z           ← árvore estava vazia
  elseif z.key < y.key
      y.left = z
  else
      y.right = z
```

- **Ponteiros**:
  - **`x`** (Azul) — desce pela árvore até encontrar `NIL`.
  - **`y`** (Amarelo) — segue `x` com um passo de atraso; é o pai onde o nó será anexado.
- **Funcionalidades**: Inserção de novos nós, reinício e ajuste de velocidade.
- **Complexidade**: $O(h)$.

---

## 5. Remoção — `bst_delete.py`

### Procedimento Auxiliar — `TRANSPLANT(T, u, v)`

```
TRANSPLANT(T, u, v)
  if u.p == NIL            ← u era a raiz
      T.root = v
  elseif u == u.p.left     ← u era filho esquerdo
      u.p.left = v
  else                     ← u era filho direito
      u.p.right = v
  if v != NIL
      v.p = u.p
```

> O `TRANSPLANT` substitui a subárvore enraizada em `u` pela subárvore enraizada em `v`, ajustando o ponteiro do pai.

### Algoritmo Principal — `TREE-DELETE(T, z)`

Existem **3 casos** possíveis:

| Caso | Condição | Ação |
|---|---|---|
| 1 | `z` não tem filho esquerdo | `TRANSPLANT(T, z, z.right)` |
| 2 | `z` não tem filho direito | `TRANSPLANT(T, z, z.left)` |
| 3 | `z` tem dois filhos | Encontrar o **sucessor mínimo** `y` de `z.right` e fazer transplante |

- **Legenda de cores**:
  - 🔴 Vermelho — nó a remover.
  - 🟣 Roxo — sucessor mínimo (caso 3).
  - 🔵 Azul — nó em análise durante o `TRANSPLANT`.
  - 🟡 Amarelo — passo do `TRANSPLANT` em execução.
  - 🟢 Verde — operação concluída.
- **Funcionalidades**: Remover, inserir novos nós, reiniciar e ajustar velocidade.
- **Complexidade**: $O(h)$.

---

## 6. Guia de Cores (todos os scripts)

| Cor | Hex | Significado |
|---|---|---|
| Cinzento escuro | `#313244` | Nó por visitar (estado inicial) |
| Azul | `#89b4fa` | Exploração / ponteiro `x` / em análise |
| Amarelo | `#f9e2af` | Comparação / visita da Raiz / TRANSPLANT |
| Laranja | `#fab387` | Ponteiro `y` (pai) / decisão → direita |
| Roxo | `#cba6f7` | Sucessor mínimo (remoção) |
| Verde | `#a6e3a1` | Sucesso — encontrado ou visitado |
| Vermelho | `#f38ba8` | Base da recursão (`NIL`) / nó a remover / falha |

---

## 7. Análise de Complexidade

| Algoritmo | Temporal | Espacial |
|---|---|---|
| Inorder Walk | $O(n)$ | $O(h)$ recursivo |
| Pesquisa Recursiva | $O(h)$ | $O(h)$ recursivo |
| Pesquisa Iterativa | $O(h)$ | $O(1)$ |
| Inserção Iterativa | $O(h)$ | $O(1)$ |
| Remoção (+ TRANSPLANT) | $O(h)$ | $O(1)$ |

> **Nota**: $h$ é a altura da árvore. Em árvores **equilibradas**, $h = O(\log n)$. Em árvores **degeneradas**, $h = O(n)$.

---

## 8. Como Executar

Navegue até esta pasta e execute o script pretendido:

```bash
python inorder_walk.py           # Percorrimento Inorder (equilibrado)
python inorder_walk_right.py     # Percorrimento Inorder (degenerado)
python bst_search.py             # Pesquisa Recursiva
python bst_search_iterative.py   # Pesquisa Iterativa
python bst_insert_iterative.py   # Inserção (TREE-INSERT)
python bst_delete.py             # Remoção (TREE-DELETE + TRANSPLANT)
```

**Requisitos**: Python 3.x com `tkinter` (incluído por defeito na maioria das instalações).

---

*Desenvolvido por Francisco Soudo — Estruturas de Dados e Algoritmos, 2024/2025.*
