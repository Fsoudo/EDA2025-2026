import os

class ListaSentinelaTabelas:
    def __init__(self, capacidade=7):
        self.capacidade = capacidade
        
        # As três tabelas (Arrays) com os nomes exatos sugeridos na imagem:
        # prev, key, next
        self.key = [None] * capacidade
        self.next = [None] * capacidade
        self.prev = [None] * capacidade
        
        # A Sentinela ficará fixamente no índice 0
        self.key[0] = "SENTINELA"
        self.next[0] = 0  # Aponta para si própria
        self.prev[0] = 0
        self.sentinela = 0
        
        # Gestão da Lista Livre (Free List) - Comportamento de Pilha
        self.free = 1
        for i in range(1, capacidade - 1):
            self.next[i] = i + 1
            self.prev[i] = None # Não precisamos do prev na Free List
        self.next[capacidade - 1] = None # Fim da lista livre
        
        print("[EXPLICAÇÃO] Memória e Tabelas Inicializadas.")
        print(f"             A Sentinela ocupa o índice {self.sentinela}.")
        print("             A variável global 'free' aponta para o índice 1.")
        self._mostrar_tabelas()
        self.pausar()

    def _allocate_object(self):
        """Retira e devolve o índice do próximo bloco livre."""
        if self.free is None:
            raise MemoryError("Out of memory: Não há mais espaço nas tabelas!")
        x = self.free
        self.free = self.next[x]
        return x

    def _free_object(self, x):
        """Devolve o índice x à lista livre (Stack / Pilha LIFO)."""
        self.key[x] = None
        self.prev[x] = None
        self.next[x] = self.free
        self.free = x

    def insert(self, chave):
        """List-Insert(L, x): Reserva memória e coloca na frente da lista"""
        print(f"\n[AÇÃO] A pedir memória para inserir '{chave}'...")
        self.pausar()
        
        x = self._allocate_object()
        self.key[x] = chave
        print(f"  [Detalhe 0] Foi alocado o índice (apontador) {x}. A variável 'free' avançou.")
        self._mostrar_tabelas("Alocação Inicial")
        self.pausar()
        
        print(f"\n  [AÇÃO] Vamos alterar os apontadores para colocar o índice {x} logo após a Sentinela...")
        # 1. O next do novo nó
        self.next[x] = self.next[self.sentinela]
        print(f"  [Detalhe 1] next[{x}] = {self.next[x]}")
        self._mostrar_tabelas("Passo 1: Ligar x ao nó seguinte")
        self.pausar()
        
        # 2. O prev do atual primeiro elemento
        elemento_seguinte = self.next[self.sentinela]
        self.prev[elemento_seguinte] = x
        print(f"  [Detalhe 2] prev[{elemento_seguinte}] = {x}")
        self._mostrar_tabelas("Passo 2: O vizinho da direita aponta para trás (para x)")
        self.pausar()
        
        # 3. O next da Sentinela
        self.next[self.sentinela] = x
        print(f"  [Detalhe 3] next[0] (Sentinela) = {x}")
        self._mostrar_tabelas("Passo 3: Sentinela aponta para o novo nó")
        self.pausar()
        
        # 4. O prev do novo nó
        self.prev[x] = self.sentinela
        print(f"  [Detalhe 4] prev[{x}] = 0 (Sentinela)")
        self._mostrar_tabelas(f"Lista Após Inserção Completa do {chave}")
        self.pausar()

    def search(self, k):
        """List-Search(L, k): Procura percorrendo índices em vez de objetos"""
        print(f"\n[AÇÃO] A iniciar a PESQUISA pela chave '{k}'...")
        self.pausar()
        
        x = self.next[self.sentinela]
        passo = 1
        
        while x != self.sentinela and self.key[x] != k:
            print(f"  -> Passo {passo}: Apontador (Índice) = {x} | Chave Atual = {self.key[x]}. Não é ({k}). Avançando nas tabelas (x = next[{x}])...")
            self._mostrar_tabelas(f"Pesquisa: Passando pelo índice {x}")
            self.pausar()
            x = self.next[x]
            passo += 1
            
        if x == self.sentinela:
            print(f"  [Concluído] O ciclo chegou novamente ao índice 0 (SENTINELA). A chave {k} NÃO existe.")
        else:
            print(f"  [Concluído] FOI ENCONTRADA a chave {k} no índice {x} das tabelas!")
        self.pausar()
        return x if x != self.sentinela else None

    def delete_by_index(self, x):
        """Remove o elemento no índice x"""
        if x == self.sentinela or x is None:
            return
            
        print(f"\n[AÇÃO] A REMOVER o elemento no índice {x} (chave = '{self.key[x]}')...")
        self.pausar()
        
        vizinho_esq = self.prev[x]
        vizinho_dir = self.next[x]
        
        # O vizinho da ESQUERDA liga ao da direita
        self.next[vizinho_esq] = vizinho_dir
        print(f"  [Detalhe 1] next[{vizinho_esq}] passa a ser {vizinho_dir} (passou por cima do índice {x})")
        self._mostrar_tabelas("Passo 1 da Remoção")
        self.pausar()
        
        # O vizinho da DIREITA liga ao da esquerda
        self.prev[vizinho_dir] = vizinho_esq
        print(f"  [Detalhe 2] prev[{vizinho_dir}] passa a ser {vizinho_esq}")
        self._mostrar_tabelas("Passo 2 da Remoção (O nó está isolado da lista)")
        self.pausar()
        
        # Liberta o nó para voltar a ser usado
        self._free_object(x)
        print(f"  [Detalhe 3] A Memória do índice {x} foi Devolvida à Free List!")
        self._mostrar_tabelas("Resultado Final após limpeza da memória")
        self.pausar()

    def _mostrar_tabelas(self, titulo="ESTADO DAS TABELAS (MEMÓRIA)"):
        """Exibe as 3 tabelas na exata ordem visual da imagem (prev -> key -> next)."""
        print(f"\n   --- {titulo} ---")
        print("   ÍNDICE | PREV | KEY          | NEXT ")
        print("   -------+------+--------------+------")
        for i in range(self.capacidade):
            k_val = str(self.key[i]) if self.key[i] is not None else "(Livre)"
            # A imagem usa "/" para simbolizar nil/None. Vamos usar " / " ou o índice
            p_val = str(self.prev[i]) if self.prev[i] is not None else "/"
            n_val = str(self.next[i]) if self.next[i] is not None else "/"
            
            marca = " "
            if i == self.free: marca = "F" # Apontador de Free List
            if i == 0: k_val = "SENTINELA"
            
            print(f" {marca} [{i}]  | {p_val:<4} | {k_val:<12} | {n_val:<4} ")
        
        print("\n   Legenda: F = Apontado pela variável 'free' | / = nil/NULL")
        self._mostrar_ordem_visual()

    def _mostrar_ordem_visual(self):
        elementos = []
        curr = self.next[self.sentinela]
        
        count = 0
        while curr != self.sentinela and count < self.capacidade:
            # Mostra no formato visual igual ao da imagem: [ prev | key | next ]
            p_v = self.prev[curr]
            n_v = self.next[curr]
            elementos.append(f"[{p_v} | {self.key[curr]} | {n_v}]")
            curr = self.next[curr]
            count += 1
            
        if not elementos:
            print("   Estrutura Lógica: (Sentinela)🔄")
        else:
            print(f"   Estrutura Lógica: [SENTINELA] <-> {' <-> '.join(elementos)} <-> [SENTINELA]")

    def pausar(self):
        input("\n    (Pressione [ENTER] para avançar...)")


# --- TESTE DO ALGORITMO COM ESTADOS VISÍVEIS (TABELAS) ---
if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("="*80)
    print(" IMPLEMENTAÇÃO COM 3 TABELAS (prev, key, next) E SENTINELA ".center(80))
    print("="*80)
    
    lista = ListaSentinelaTabelas(capacidade=6)
    
    # Vamos usar os números exatamente como na imagem (a), (b) e (c)!
    # Originalmente a imagem tem 9, 16, 4, 1. Vamos testar inserir o 25!
    lista.insert(9)
    lista.insert(16)
    lista.insert(4)
    lista.insert(1)
    
    # a) O estado original da primeira alínea da imagem está focado na inserção do 25
    # b) Inserção do 25
    lista.insert(25)
    
    # c) Remoção do elemento 4
    n_encontrado_4 = lista.search(4)
    if n_encontrado_4 is not None:
        lista.delete_by_index(n_encontrado_4)
        
    print("\n" + "="*80)
    print(" FIM DA DEMONSTRAÇÃO ".center(80))
    print("="*80)
