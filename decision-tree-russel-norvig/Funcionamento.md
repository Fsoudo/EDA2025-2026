# Decision Tree Learning — Russell & Norvig
### Problema do Restaurante (Fig 18.3 / 18.6)

---

## O Problema

Dado um conjunto de exemplos de clientes num restaurante, o algoritmo aprende a prever se um cliente **vai esperar** (`WillWait = YES/NO`).

Cada exemplo tem **10 atributos**:

| Atributo | Valores possíveis |
|----------|-------------------|
| Alternate | yes / no |
| Bar | yes / no |
| Fri/Sat | yes / no |
| Hungry | yes / no |
| Patrons | None / Some / Full |
| Price | $ / $$ / $$$ |
| Raining | yes / no |
| Reservation | yes / no |
| Type | French / Thai / Burger / Italian |
| WaitEstimate | 0-10 / 10-30 / 30-60 / >60 |

O dataset tem **12 exemplos** (6 YES, 6 NO) — Fig 18.3 do livro.

---

## Algoritmo — DTL (Decision Tree Learning / ID3)

O algoritmo é **recursivo**. A cada chamada recebe um subconjunto de exemplos e decide o que fazer:

```
DTL(examples, attributes, parent_examples):

  1. SE examples está vazio
       → retorna PLURALITY(parent_examples)   [maioria dos exemplos do pai]

  2. SE todos os examples têm a mesma classe
       → retorna Leaf(classe)                 [puro → folha]

  3. SE attributes está vazio
       → retorna PLURALITY(examples)          [sem mais atributos para dividir]

  4. SENÃO:
       Para cada atributo A em attributes:
           Calcula Gain(A, examples)
       best ← atributo com maior Gain
       Cria nó de decisão em best
       Para cada valor v de best:
           subset ← exemplos onde best = v
           subtree ← DTL(subset, attributes \ {best}, examples)
           Adiciona ramo (v → subtree) ao nó
       Retorna nó
```

---

## Information Gain — Como escolher o melhor atributo

### Entropia

Mede a "impureza" de um conjunto de exemplos:

```
H(examples) = - (p/(p+n)) × log₂(p/(p+n))
              - (n/(p+n)) × log₂(n/(p+n))
```

- `p` = número de exemplos YES  
- `n` = número de exemplos NO  
- Se todos YES ou todos NO → `H = 0` (puro)  
- Se metade YES metade NO → `H = 1.0 bit` (máximo)

### Remainder

Entropia média ponderada após dividir por atributo A:

```
Remainder(A) = Σ (|subset_v| / |examples|) × H(subset_v)
               para cada valor v de A
```

### Gain

```
Gain(A, examples) = H(examples) − Remainder(A)
```

Escolhe-se o atributo com **maior Gain** → maior redução de incerteza.

---

## Estrutura do Código

```
decision-tree-russel-norvig/
│
├── src/
│   ├── Attribute.java      ← Enum com os 10 atributos e seus valores
│   ├── Example.java        ← Um exemplo de treino (linha do dataset)
│   ├── TreeNode.java       ← Classe abstrata base para nós da árvore
│   ├── LeafNode.java       ← Nó folha: guarda classificação final (YES/NO)
│   ├── DecisionNode.java   ← Nó interno: atributo + ramos por valor
│   ├── Dataset.java        ← 12 exemplos R&N hardcoded
│   ├── DTL.java            ← Algoritmo com trace visível de cada passo
│   └── Main.java           ← Entry point: corre DTL e verifica accuracy
│
├── out/                    ← Bytecode compilado (gerado automaticamente)
└── run.bat                 ← Script para compilar e correr (Windows)
```

### Responsabilidades por classe

#### `Attribute.java`
Enum com cada atributo e os seus valores possíveis.  
Usado para iterar valores ao fazer o split e calcular partições.

#### `Example.java`
Representa uma linha do dataset.  
Guarda os valores dos 10 atributos + label `willWait`.

#### `TreeNode.java` (abstract)
Interface comum a `LeafNode` e `DecisionNode`:
- `classify(Example)` → percorre a árvore e retorna YES/NO
- `display(indent)` → imprime a árvore em texto formatado

#### `LeafNode.java`
Nó terminal. Guarda `boolean classification`.  
`classify()` retorna sempre o mesmo valor.

#### `DecisionNode.java`
Nó interno. Guarda o atributo de split e um `Map<String, TreeNode>` (valor → subárvore).  
`classify()` lê o valor do atributo no exemplo e segue o ramo correspondente.

#### `Dataset.java`
Factory estático que retorna os 12 exemplos da Fig 18.3 de R&N.

#### `DTL.java`
O coração do programa. Implementa o algoritmo recursivo e **imprime o estado completo** a cada chamada:
- Número do step e profundidade
- Exemplos correntes (IDs) com contagem YES/NO
- Entropia do conjunto atual
- Tabela de Information Gain por atributo (◄ BEST marcado)
- Caso base ativado (se aplicável)
- Ramos criados e subsets passados recursivamente

#### `Main.java`
1. Carrega o dataset
2. Corre `DTL.learn()`
3. Imprime a árvore aprendida
4. Classifica todos os 12 exemplos e verifica accuracy

---

## Trace de Execução — Exemplo (Step 1)

```
┌─ STEP 1  depth=0
│  Examples [12] YES=6  NO=6  →  E1, E2, E3, ..., E12
│  Attributes: Alternate, Bar, Fri/Sat, Hungry, Patrons, ...
│
│  H(examples) = 1.0000 bits
│
│  Attribute         Gain     Partition sizes
│  Alternate         0.0207   yes=7  no=5
│  Bar               0.0207   yes=5  no=7
│  Fri/Sat           0.0000   yes=4  no=8
│  Hungry            0.1957   yes=7  no=5
│  Patrons           0.5409   None=2  Some=4  Full=6  ◄ BEST
│  Price             0.1957   $=7  $$=2  $$$=3
│  ...
│
│  → SPLIT on Patrons  (gain = 0.5409 bits)
│  Branch Patrons=None  size=2  E7, E11
│  Branch Patrons=Some  size=4  E1, E3, E6, E8
│  Branch Patrons=Full  size=6  E2, E4, E5, E9, E10, E12
└──────────────────────────────────────────────────
```

**Patrons** é escolhido no root porque tem o maior Gain (0.5409 bits).

---

## Árvore Final Aprendida

Coincide com a Fig 18.6 do livro:

```
[Patrons?]
  ├─ None:
  │   [Leaf: NO]
  ├─ Some:
  │   [Leaf: YES]
  └─ Full:
      [Fri/Sat?]
        ├─ yes:
        │   [Price?]
        │     ├─ $:   [Leaf: YES]
        │     ├─ $$:  [Leaf: YES]  ← plurality (sem exemplos $$+Full+Fri)
        │     └─ $$$: [Leaf: NO]
        └─ no:
            [Leaf: NO]
```

**Accuracy: 12/12** nos dados de treino.

---

## Como Correr

### Opção 1 — Script (Windows)
```
run.bat
```
Compila e executa automaticamente.

### Opção 2 — Terminal
```bash
# Compilar
javac -encoding UTF-8 -d out src/*.java

# Executar
java -cp out src.Main
```

> **Nota:** O `-encoding UTF-8` é necessário porque o `DTL.java` usa caracteres ANSI para colorir o output no terminal.

---

## Conceitos Chave (R&N Cap. 18)

| Conceito | Definição |
|----------|-----------|
| **Entropia** | Medida de impureza de um conjunto |
| **Information Gain** | Redução de entropia ao dividir por um atributo |
| **Plurality** | Classe maioritária num conjunto (desempate → YES) |
| **Overfitting** | Risco se o dataset for pequeno — esta árvore não faz pruning |
| **ID3** | Variante do DTL que usa Gain como heurística de escolha |
