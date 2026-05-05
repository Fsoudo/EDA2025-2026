"""
RESUMO: Conjuntos Dinâmicos (eda-5.pdf)
Este arquivo serve como um guia rápido para as principais estruturas 
mencionadas no PDF da Aula 5.
"""

# ---------------------------------------------------------
# 1. PILHA (Stack) - LIFO (Last-In, First-Out)
# ---------------------------------------------------------
class PilhaSimples:
    def __init__(self, n):
        self.S = [0] * n
        self.top = -1  # No PDF é S.top, indexado de 1 a n
    
    def empty(self):
        return self.top == -1
    
    def push(self, x):
        self.top += 1
        self.S[self.top] = x
        
    def pop(self):
        if self.empty(): raise IndexError("Underflow")
        x = self.S[self.top]
        self.top -= 1
        return x

# ---------------------------------------------------------
# 2. FILA (Queue) - FIFO (First-In, First-Out) - Circular
# ---------------------------------------------------------
class FilaCircular:
    def __init__(self, n):
        self.Q = [0] * n
        self.head = 0
        self.tail = 0
        self.length = n
        
    def enqueue(self, x):
        self.Q[self.tail] = x
        if self.tail == self.length - 1: self.tail = 0
        else: self.tail += 1
        
    def dequeue(self):
        x = self.Q[self.head]
        if self.head == self.length - 1: self.head = 0
        else: self.head += 1
        return x

# ---------------------------------------------------------
# 3. LISTA LIGADA (Linked List) - Dupla com Sentinela
# ---------------------------------------------------------
class NoLista:
    def __init__(self, k=None):
        self.key = k
        self.next = None
        self.prev = None

class ListaSentinela:
    def __init__(self):
        self.nil = NoLista()  # O objeto sentinela
        self.nil.next = self.nil
        self.nil.prev = self.nil
        
    def insert(self, x):
        """Insere x no início da lista (logo após a sentinela)"""
        x.next = self.nil.next
        self.nil.next.prev = x
        self.nil.next = x
        x.prev = self.nil
        
    def search(self, k):
        x = self.nil.next
        while x != self.nil and x.key != k:
            x = x.next
        return x

# ---------------------------------------------------------
# 4. ÁRVORES (Trees)
# ---------------------------------------------------------
class NoArvore:
    def __init__(self, k):
        self.key = k
        self.p = None      # Parent
        self.left = None   # Left child
        self.right = None  # Right child (ou sibling em n-árias)

# ---------------------------------------------------------
# FUNÇÃO DE DEMONSTRAÇÃO RÁPIDA
# ---------------------------------------------------------
def demo():
    print("--- DEMO PILHA ---")
    p = PilhaSimples(5)
    p.push(10); p.push(20)
    print("Pop:", p.pop()) # 20
    
    print("\n--- DEMO FILA CIRCULAR ---")
    f = FilaCircular(5)
    f.enqueue(1); f.enqueue(2)
    print("Dequeue:", f.dequeue()) # 1
    
    print("\n--- DEMO LISTA COM SENTINELA ---")
    l = ListaSentinela()
    no1 = NoLista(50)
    l.insert(no1)
    print("Search 50:", "Encontrado" if l.search(50) != l.nil else "Não encontrado")

if __name__ == "__main__":
    demo()
