import os
import sys

# Forçar encoding UTF-8 para o terminal Windows poder ver os caracteres acentuados
sys.stdout.reconfigure(encoding='utf-8')

def pausar():
    input("\n  [ENTER para continuar...]\n")

def linha(char="=", n=60):
    print(char * n)

# ============================================================
#  CLASSE NÓ  (left-child / right-sibling — Slide 39)
# ============================================================
class NoNaria:
    """
    Cada nó guarda APENAS dois apontadores além da chave:
      - left_child    : aponta para o PRIMEIRO filho
                        (cabeça de uma lista ligada de filhos)
      - right_sibling : aponta para o PRÓXIMO irmão
                        (próximo nó da mesma lista ligada)

    Isto permite representar qualquer número de filhos usando
    apenas O(n) de memória, tal como descrito no Slide 39.
    """
    def __init__(self, chave):
        self.key           = chave
        self.parent        = None   # p  — progenitor
        self.left_child    = None   # left-child
        self.right_sibling = None   # right-sibling


# ============================================================
#  ÁRVORE N-ÁRIA
# ============================================================
class ArvoreNariaLista:
    def __init__(self):
        self.root = None

    # -----------------------------------------------------------
    # INSERÇÃO com explicação passo-a-passo
    # -----------------------------------------------------------
    def inserir_filho(self, pai_chave, nova_chave):
        """
        Insere nova_chave como filho de pai_chave.
        Se pai_chave=None, cria a raiz.
        """
        linha("-")
        print(f"  INSERIR  '{nova_chave}'  como filho de  '{pai_chave}'")
        linha("-")

        if self.root is None:
            self.root = NoNaria(nova_chave)
            print(f"  >> Arvore vazia. '{nova_chave}' torna-se a RAIZ.")
            print(f"     root.left_child    = None")
            print(f"     root.right_sibling = None")
            return self.root

        pai = self._buscar(self.root, pai_chave)
        if pai is None:
            print(f"  >> ERRO: no pai '{pai_chave}' nao encontrado!")
            return None

        novo       = NoNaria(nova_chave)
        novo.parent = pai

        # Caso 1: pai ainda não tem filhos → left_child aponta para o novo
        if pai.left_child is None:
            pai.left_child = novo
            print(f"  >> '{pai_chave}' nao tinha filhos.")
            print(f"     LIGACAO: {pai_chave}.left_child  -->  '{nova_chave}'")

        # Caso 2: pai já tem filhos → percorre lista ligada de irmãos até ao fim
        else:
            print(f"  >> '{pai_chave}' ja tem filhos.")
            print(f"     A percorrer a lista ligada de irmaos:")
            atual = pai.left_child
            passo = 1
            while atual.right_sibling is not None:
                print(f"     passo {passo}: '{atual.key}'.right_sibling = '{atual.right_sibling.key}' → avançar")
                atual = atual.right_sibling
                passo += 1
            print(f"     passo {passo}: '{atual.key}'.right_sibling = None → FIM da lista")
            print(f"     LIGACAO: {atual.key}.right_sibling  -->  '{nova_chave}'")
            atual.right_sibling = novo

        return novo

    # -----------------------------------------------------------
    # BUSCA recursiva (for-each filho via lista de irmãos)
    # -----------------------------------------------------------
    def _buscar(self, no, chave):
        if no is None:     return None
        if no.key == chave: return no
        res = self._buscar(no.left_child, chave)    # desce para filhos
        if res: return res
        return self._buscar(no.right_sibling, chave) # avança para irmão

    # -----------------------------------------------------------
    # VISTA LÓGICA da árvore (indentação hierárquica)
    # -----------------------------------------------------------
    def imprimir_logica(self, no=None, nivel=0, _primeiro_call=True):
        """Vista lógica — mostra a hierarquia real (pai → filhos)"""
        if _primeiro_call:
            linha()
            print("  VISTA LOGICA  (hierarquia real)")
            linha()
        if no is None:
            return
        prefixo = "   " * nivel
        label   = "RAIZ" if nivel == 0 else "+---"
        print(f"{prefixo}{label} [ {no.key} ]")

        # Percorrer a lista ligada de filhos
        filho = no.left_child
        while filho is not None:
            self.imprimir_logica(filho, nivel + 1, _primeiro_call=False)
            filho = filho.right_sibling

    # -----------------------------------------------------------
    # VISTA FÍSICA dos ponteiros de cada nó
    # -----------------------------------------------------------
    def imprimir_fisica(self):
        """Vista física — mostra os dois apontadores de cada nó"""
        linha()
        print("  VISTA FISICA  (apontadores left_child / right_sibling)")
        linha()
        print(f"  {'NO':<12} | {'PARENT':<12} | {'LEFT_CHILD':<12} | {'RIGHT_SIBLING':<14}")
        print(f"  {'-'*12}-+-{'-'*12}-+-{'-'*12}-+-{'-'*14}")
        self._imprimir_fisica_rec(self.root)

    def _imprimir_fisica_rec(self, no):
        if no is None:
            return
        p  = no.parent.key        if no.parent        else "None"
        lc = no.left_child.key    if no.left_child    else "None"
        rs = no.right_sibling.key if no.right_sibling else "None"
        print(f"  {str(no.key):<12} | {p:<12} | {lc:<12} | {rs:<14}")
        self._imprimir_fisica_rec(no.left_child)
        self._imprimir_fisica_rec(no.right_sibling)


# ============================================================
#  DEMONSTRAÇÃO PASSO-A-PASSO
# ============================================================
def demo():
    os.system("cls" if os.name == "nt" else "clear")
    linha()
    print("  ARVORE N-ARIA COM LISTA LIGADA DE IRMAOS")
    print("  (Slide 39 de eda-5.pdf  —  Conjuntos Dinamicos)")
    linha()
    print("""
  IDEIA CHAVE
  -----------
  Qualquer arvore pode ter um numero variavel de filhos.
  Se guardarmos um apontador por filho, precisamos de saber
  antecipadamente quantos filhos cada no pode ter — ineficiente!

  Solucao 'left-child / right-sibling':
    - left_child    --> 1.o filho (inicio de uma lista ligada)
    - right_sibling --> proximo irmao (proximo da mesma lista)

  Com apenas DOIS apontadores por no representamos QUALQUER arvore
  usando apenas O(n) de memoria total.
    """)
    pausar()

    # ----------------------------------------------------------
    # CONSTRUÇÃO DA ÁRVORE
    # ----------------------------------------------------------
    arvore = ArvoreNariaLista()
    passos = [
        (None, 1),
        (1,    2),
        (1,    3),
        (1,    4),
        (2,    5),
        (2,    6),
        (4,    7),
    ]

    for pai, filho in passos:
        arvore.inserir_filho(pai, filho)
        arvore.imprimir_logica(arvore.root)
        pausar()

    # ----------------------------------------------------------
    # VISTA FÍSICA
    # ----------------------------------------------------------
    arvore.imprimir_fisica()
    pausar()

    # ----------------------------------------------------------
    # RESUMO FINAL
    # ----------------------------------------------------------
    linha()
    print("  RESUMO")
    linha()
    print("""
  Ao inserir um filho:
    1. Se left_child == None  -->  first child:
         pai.left_child = novo_no

    2. Se left_child != None  -->  percorrer lista de irmaos:
         atual = pai.left_child
         while atual.right_sibling != None:
             atual = atual.right_sibling
         atual.right_sibling = novo_no

  O NO NOVO nunca altera a estrutura dos nos existentes —
  apenas se adiciona ao FIM da lista ligada de irmaos.
    """)

if __name__ == "__main__":
    demo()
