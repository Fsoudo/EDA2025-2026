import os

def ler_inteiro(mensagem):
    while True:
        try:
            # Em Python, o input lê a linha toda como string, e int() tenta convertê-la
            return int(input(mensagem))
        except ValueError:
            print("Erro: tens de inserir um número inteiro.")

# =========================================================
# PILHA (Stack)
# =========================================================
class Pilha:
    def __init__(self, capacidade):
        self.capacidade = capacidade
        self.dados = [0] * capacidade
        self.topo = -1

    def esta_vazia(self):
        return self.topo == -1

    def esta_cheia(self):
        return self.topo == self.capacidade - 1

    def push(self, valor):
        if self.esta_cheia():
            print("Erro: overflow na pilha.")
            return
        self.topo += 1
        self.dados[self.topo] = valor
        print("Valor inserido na pilha.")

    def pop(self):
        if self.esta_vazia():
            print("Erro: underflow na pilha.")
            return None
        valor = self.dados[self.topo]
        self.topo -= 1
        return valor

    def mostrar(self):
        elementos = [str(self.dados[i]) for i in range(self.topo + 1)]
        print("Pilha: [" + ", ".join(elementos) + "]")

# =========================================================
# FILA (Queue Circular)
# =========================================================
class Fila:
    def __init__(self, capacidade):
        self.capacidade = capacidade
        self.dados = [0] * capacidade
        self.head = 0
        self.tail = 0
        self.tamanho = 0

    def esta_vazia(self):
        return self.tamanho == 0

    def esta_cheia(self):
        return self.tamanho == self.capacidade

    def enqueue(self, valor):
        if self.esta_cheia():
            print("Erro: overflow na fila.")
            return
        self.dados[self.tail] = valor
        self.tail = (self.tail + 1) % self.capacidade
        self.tamanho += 1
        print("Valor inserido na fila.")

    def dequeue(self):
        if self.esta_vazia():
            print("Erro: underflow na fila.")
            return None
        valor = self.dados[self.head]
        self.head = (self.head + 1) % self.capacidade
        self.tamanho -= 1
        return valor

    def mostrar(self):
        elementos = []
        for i in range(self.tamanho):
            indice = (self.head + i) % self.capacidade
            elementos.append(str(self.dados[indice]))
        print("Fila: [" + ", ".join(elementos) + "]")

# =========================================================
# LISTA LIGADA (Singly Linked List)
# =========================================================
class No:
    def __init__(self, valor):
        self.valor = valor
        self.next = None

class ListaLigada:
    def __init__(self):
        self.head = None

    def inserir_no_inicio(self, valor):
        novo = No(valor)
        novo.next = self.head
        self.head = novo
        print("Valor inserido na lista ligada.")

    def procurar(self, valor):
        atual = self.head
        while atual is not None:
            if atual.valor == valor:
                return True
            atual = atual.next
        return False

    def remover(self, valor):
        if self.head is None:
            return False

        if self.head.valor == valor:
            self.head = self.head.next
            return True

        atual = self.head
        while atual.next is not None:
            if atual.next.valor == valor:
                atual.next = atual.next.next
                return True
            atual = atual.next

        return False

    def mostrar(self):
        elementos = []
        atual = self.head
        
        if atual is None:
            print("Lista ligada: null")
            return
            
        while atual is not None:
            elementos.append(str(atual.valor))
            atual = atual.next
        print("Lista ligada: " + " -> ".join(elementos) + " -> null")

# =========================================================
# PROGRAMA PRINCIPAL
# =========================================================
def mostrar_menu():
    print("=== MENU ESTRUTURAS DINÂMICAS ===")
    print("1 - Push na pilha")
    print("2 - Pop da pilha")
    print("3 - Enqueue na fila")
    print("4 - Dequeue da fila")
    print("5 - Inserir na lista ligada")
    print("6 - Remover da lista ligada")
    print("7 - Procurar na lista ligada")
    print("8 - Mostrar todas as estruturas")
    print("0 - Sair")

def main():
    pilha = Pilha(5)
    fila = Fila(5)
    lista = ListaLigada()

    opcao = -1

    while opcao != 0:
        mostrar_menu()
        opcao = ler_inteiro("Escolhe uma opção: ")
        print()

        if opcao == 1:
            valor = ler_inteiro("Valor para inserir na pilha: ")
            pilha.push(valor)
            pilha.mostrar()
            
        elif opcao == 2:
            removido = pilha.pop()
            if removido is not None:
                print(f"Removido da pilha: {removido}")
            pilha.mostrar()
            
        elif opcao == 3:
            valor = ler_inteiro("Valor para inserir na fila: ")
            fila.enqueue(valor)
            fila.mostrar()
            
        elif opcao == 4:
            removido = fila.dequeue()
            if removido is not None:
                print(f"Removido da fila: {removido}")
            fila.mostrar()
            
        elif opcao == 5:
            valor = ler_inteiro("Valor para inserir na lista ligada: ")
            lista.inserir_no_inicio(valor)
            lista.mostrar()
            
        elif opcao == 6:
            valor = ler_inteiro("Valor para remover da lista ligada: ")
            removido = lista.remover(valor)
            if removido:
                print("Valor removido com sucesso.")
            else:
                print("Valor não encontrado.")
            lista.mostrar()
            
        elif opcao == 7:
            valor = ler_inteiro("Valor a procurar na lista ligada: ")
            existe = lista.procurar(valor)
            # Em Python True/False é com maiúscula, uso lower() para ficar = boolean Java (true/false)
            print(f"Existe {valor}? {str(existe).lower()}")
            
        elif opcao == 8:
            print("Estado atual das estruturas:")
            pilha.mostrar()
            fila.mostrar()
            lista.mostrar()
            
        elif opcao == 0:
            print("Programa terminado.")
            
        else:
            print("Opção inválida.")
        
        print()

if __name__ == "__main__":
    main()
