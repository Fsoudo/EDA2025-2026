# -*- coding: utf-8 -*-
# ============================================================
#  Merge Sort -- Visualizacao de Todos os Estagios
#  Disciplina: Estruturas de Dados e Algoritmos
#  Técnica: Divisão e Conquista  |  Complexidade: Θ(n log n)
# ============================================================

# Cores ANSI para terminal (funciona no Windows 10+ e qualquer terminal moderno)
RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
RED    = "\033[91m"
MAGENTA= "\033[95m"
DIM    = "\033[2m"

# Contador de estagio global
_stage = [0]


def _print_array(A: list, p: int, r: int, highlight: list = None, label: str = "") -> None:  # noqa: E501
    """Imprime o array completo, destacando a sub-lista A[p..r]."""
    out = []
    for idx, val in enumerate(A):
        s = str(val).rjust(4)
        if p <= idx <= r:3
            if highlight and idx in highlight:
                out.append(f"{GREEN}{BOLD}{s}{RESET}")
            else:
                out.append(f"{YELLOW}{s}{RESET}")
        else:
            out.append(f"{DIM}{s}{RESET}")
    print(f"  {''.join(out)}   {DIM}{label}{RESET}")


def _divider(depth: int) -> str:
    return "  " * depth


# ──────────────────────────────────────────────
#  MERGE com visualização
# ──────────────────────────────────────────────
def merge_visual(A: list, p: int, q: int, r: int, depth: int) -> None:
    """Funde duas sub-listas ordenadas e mostra o processo."""
    _stage[0] += 1
    indent = _divider(depth)

    L = A[p : q + 1]
    R = A[q + 1 : r + 1]

    print(f"\n{indent}{CYAN}{BOLD}>> Estagio {_stage[0]} -- FUSAO{RESET}  "
          f"A[{p}..{r}]")
    print(f"{indent}  Esquerda : {YELLOW}{L}{RESET}")
    print(f"{indent}  Direita  : {YELLOW}{R}{RESET}")

    SENTINELA = float('inf')
    L.append(SENTINELA)
    R.append(SENTINELA)

    i = j = 0
    merged_indices = []

    for k in range(p, r + 1):
        if L[i] <= R[j]:
            A[k] = L[i]
            src = f"L[{i}]={L[i]}"
            i += 1
        else:
            A[k] = R[j]
            src = f"R[{j}]={R[j]}"
            j += 1
        merged_indices.append(k)
        print(f"{indent}  k={k}: coloca {GREEN}{A[k]}{RESET} (de {src})", end="  ->  ")
        _print_array(A, p, r, highlight=merged_indices)

    print(f"{indent}  {GREEN}OK Resultado A[{p}..{r}] = {A[p:r+1]}{RESET}")


# ──────────────────────────────────────────────
#  MERGE SORT com visualização
# ──────────────────────────────────────────────
def merge_sort_visual(A: list, p: int, r: int, depth: int = 0) -> None:
    """Ordena A[p..r] mostrando cada fase de divisão e fusão."""
    indent = _divider(depth)

    if p < r:
        q = (p + r) // 2

        # -- Divisao --
        print(f"\n{indent}{MAGENTA}{BOLD}** DIVISAO{RESET}  "
              f"A[{p}..{r}]  ->  A[{p}..{q}] + A[{q+1}..{r}]")
        print(f"{indent}  q = floor(({p}+{r})/2) = {q}")
        _print_array(A, p, r, label=f"sub-lista actual A[{p}..{r}]")

        # -- Recursao esquerda --
        merge_sort_visual(A, p, q,     depth + 1)

        # -- Recursao direita --
        merge_sort_visual(A, q + 1, r, depth + 1)

        # -- Fusao --
        merge_visual(A, p, q, r, depth)

    else:
        # Caso base: sub-lista de 1 elemento
        print(f"\n{indent}{DIM}* Base: A[{p}] = [{A[p]}]  (ja ordenado){RESET}")


# ──────────────────────────────────────────────
#  Programa Principal
# ──────────────────────────────────────────────
if __name__ == "__main__":
    import os, sys
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    # Activar cores ANSI no Windows
    os.system("")

    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}  MERGE SORT -- Visualizacao de Todos os Estagios{RESET}")
    print(f"{BOLD}{'='*60}{RESET}")

    # -- Escolha do array --
    print(f"\n{CYAN}Opcoes:{RESET}")
    print("  1 - Usar array de exemplo  [38, 27, 43, 3, 9, 82, 10]")
    print("  2 - Introduzir array manualmente")
    print("  3 - Usar array aleatorio")
    opcao = input(f"\n{YELLOW}Escolha (1/2/3): {RESET}").strip()

    if opcao == "2":
        entrada = input(f"{YELLOW}Introduza os numeros separados por espacos: {RESET}")
        try:
            A = list(map(int, entrada.split()))
        except ValueError:
            print(f"{RED}Entrada invalida. A usar array de exemplo.{RESET}")
            A = [38, 27, 43, 3, 9, 82, 10]
    elif opcao == "3":
        import random
        n = int(input(f"{YELLOW}Quantos elementos? {RESET}") or "8")
        A = random.sample(range(1, 100), min(n, 99))
        print(f"{CYAN}Array gerado: {A}{RESET}")
    else:
        A = [38, 27, 43, 3, 9, 82, 10]

    print(f"\n{BOLD}Array inicial:{RESET} {A}")
    print(f"{BOLD}{'-'*60}{RESET}")

    merge_sort_visual(A, 0, len(A) - 1)

    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{GREEN}{BOLD}  OK Array ordenado: {A}{RESET}")
    print(f"{BOLD}{'='*60}{RESET}\n")
