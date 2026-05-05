import os
import time

def pausar(mensagem="\n[Pressione ENTER para continuar para o próximo passo...]"):
    input(mensagem)

def limpar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

# =========================================================
# 1. ÁRVORE BINÁRIA (Object-Oriented) + VISUALIZAÇÃO ASCII
# =========================================================
class NoBinario:
    def __init__(self, chave):
        self.key = chave
        self.p = None
        self.left = None
        self.right = None

class ArvoreBinaria:
    def __init__(self):
        self.root = None

    def inserir(self, chave):
        
        print(f"\n[ALGORITMO] A inserir a chave {chave}...")
        novo = NoBinario(chave)
        y = None
        x = self.root
        
        while x is not None:
            y = x
            if novo.key < x.key:
                print(f"  -> {novo.key} < {x.key}: A descer para a ESQUERDA.")
                x = x.left
            else:
                print(f"  -> {novo.key} >= {x.key}: A descer para a DIREITA.")
                x = x.right
            time.sleep(0.3)
        
        novo.p = y
        if y is None:
            print(f"  [CONCLUÍDO] Árvore vazia. {chave} torna-se a RAIZ.")
            self.root = novo
        elif novo.key < y.key:
            print(f"  [CONCLUÍDO] Ligado à ESQUERDA de {y.key}.")
            y.left = novo
        else:
            print(f"  [CONCLUÍDO] Ligado à DIREITA de {y.key}.")
            y.right = novo

    def imprimir_ascii(self, no, prefix="", is_left=True):
        """Desenha a árvore de forma visual na consola (Versão ASCII Segura)"""
        if no is not None:
            self.imprimir_ascii(no.right, prefix + ("|   " if is_left else "    "), False)
            print(prefix + ("+-- " if is_left else "+-- ") + str(no.key))
            self.imprimir_ascii(no.left, prefix + ("    " if is_left else "|   "), True)

# =========================================================
# 2. ÁRVORE BINÁRIA EM TABELAS (MEMÓRIA SIMULADA)
# =========================================================
class ArvoreBinariaTabelas:
    def __init__(self, capacidade=8):
        self.capacidade = capacidade
        self.key = [None] * capacidade
        self.p = [None] * capacidade
        self.left = [None] * capacidade
        self.right = [None] * capacidade
        
        # Free list (Pilha de índices livres)
        self.free = 0
        for i in range(capacidade - 1):
            self.right[i] = i + 1
        self.right[capacidade - 1] = None
        
        self.root = None

    def inserir_com_visualizacao(self, chave):
        limpar_consola()
        print(f"=== PASSO-A-PASSO: INSERIR {chave} NA MEMÓRIA ===")
        
        # 1. Alocação
        idx = self.free
        if idx is None: raise MemoryError("Sem memória!")
        self.free = self.right[idx]
        
        self.key[idx] = chave
        self.left[idx] = None
        self.right[idx] = None
        self.p[idx] = None
        
        print(f"\n[PASSO 1] Alocado o índice {idx} para a chave {chave}.")
        print(f"          A variável 'free' agora aponta para {self.free}.")
        self.imprimir_tabelas()
        pausar()

        # 2. Ligação lógica
        if self.root is None:
            self.root = idx
            print(f"\n[PASSO 2] Árvore vazia. root = {idx}.")
        else:
            print(f"\n[PASSO 2] A percorrer a árvore para posicionar o índice {idx}...")
            self._percorrer_e_ligar(self.root, idx)
        
        self.imprimir_tabelas()
        pausar()

    def _percorrer_e_ligar(self, atual, novo_idx):
        if self.key[novo_idx] < self.key[atual]:
            print(f"  -> {self.key[novo_idx]} < {self.key[atual]}: Olhar para left[{atual}] (índice {self.left[atual]})")
            if self.left[atual] is None:
                print(f"     [LIGAÇÃO] left[{atual}] recebe {novo_idx}. p[{novo_idx}] recebe {atual}.")
                self.left[atual] = novo_idx
                self.p[novo_idx] = atual
            else:
                self._percorrer_e_ligar(self.left[atual], novo_idx)
        else:
            print(f"  -> {self.key[novo_idx]} >= {self.key[atual]}: Olhar para right[{atual}] (índice {self.right[atual]})")
            if self.right[atual] is None:
                print(f"     [LIGAÇÃO] right[{atual}] recebe {novo_idx}. p[{novo_idx}] recebe {atual}.")
                self.right[atual] = novo_idx
                self.p[novo_idx] = atual
            else:
                self._percorrer_e_ligar(self.right[atual], novo_idx)

    def imprimir_tabelas(self):
        print("\n--- ESTADO DASHBOARD (TABELAS DE MEMÓRIA) ---")
        print(" ÍNDICE | P    | KEY  | LEFT | RIGHT")
        print(" -------+------+------+------+------")
        for i in range(self.capacidade):
            k = str(self.key[i]) if self.key[i] is not None else "."
            par = str(self.p[i]) if self.p[i] is not None else "/"
            l = str(self.left[i]) if self.left[i] is not None else "/"
            r = str(self.right[i]) if self.right[i] is not None else "/"
            
            marca = ""
            if i == self.root: marca = "<- ROOT"
            if i == self.free: marca = "<- FREE"
            
            print(f"  [{i}]   | {par:<4} | {k:<4} | {l:<4} | {r:<4} {marca}")

# =========================================================
# 3. DEMONSTRAÇÃO INTERATIVA
# =========================================================
def demo_interativa():
    # ENTRADA DE DADOS
    limpar_consola()
    print("=== CONFIGURAÇÃO DOS DADOS ===")
    try:
        entrada = input("Introduza os valores para a árvore (separados por espaço, ex: 15 6 18 3): ")
        valores = [int(v) for v in entrada.split()]
        if not valores:
            print("\nLista vazia. A usar valores padrão: [15, 6, 18, 3, 7, 17, 20]")
            valores = [15, 6, 18, 3, 7, 17, 20]
    except ValueError:
        print("\nErro: Entrada inválida. A usar valores padrão: [15, 6, 18, 3, 7, 17, 20]")
        valores = [15, 6, 18, 3, 7, 17, 20]
    
    pausar("\n--- [ENTER para iniciar Teste 1: Visualização ASCII] ---")

    # TESTE 1: ÁRVORE BINÁRIA ASCII
    limpar_consola()
    print("=== TESTE 1: VISUALIZAÇÃO LÓGICA (ASCII) ===")
    ab = ArvoreBinaria()
    for v in valores:
        ab.inserir(v)
    
    print("\nEstrutura Lógica Final:")
    ab.imprimir_ascii(ab.root)
    pausar("\n--- [PASSO SEGUINTE: Árvore em Memória/Tabelas] ---")

    # TESTE 2: ÁRVORE EM TABELAS PASSO-A-PASSO
    # Ajustamos a capacidade ao tamanho do array (mínimo 8)
    capacidade = max(len(valores), 8)
    abt = ArvoreBinariaTabelas(capacidade=capacidade)
    
    # Inserimos gradualmente até ao penúltimo
    for v in valores[:-1]:
        abt.inserir_com_visualizacao(v)
    
    # O último elemento é o "desafio final"
    if valores:
        limpar_consola()
        print("=== DESAFIO FINAL: Inserindo o último elemento ===")
        abt.inserir_com_visualizacao(valores[-1])
    
    print("\nPARABÉNS! Completaste a visualização do algoritmo.")
    print("Agora consegues ver como o computador guarda 'setas' usando apenas números/índices.")

if __name__ == "__main__":
    demo_interativa()
