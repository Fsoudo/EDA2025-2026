# -*- coding: utf-8 -*-
# ============================================================
#  Merge Sort -- Visualizacao Grafica com Controlos
#  Botoes: Play/Pause | Anterior | Proximo | Reiniciar
#  Slider: navegar para qualquer frame
#  Disciplina: Estruturas de Dados e Algoritmos
# ============================================================

import matplotlib
matplotlib.use("TkAgg")          # backend com suporte a botoes interactivos
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.widgets as widgets
import random

# ── Paleta de cores ──────────────────────────────────────────
C_DEFAULT  = "#3a3f58"
C_ACTIVE   = "#f0a500"
C_LEFT     = "#5b8dee"
C_RIGHT    = "#e05c97"
C_MERGE    = "#26de81"
C_SORTED   = "#a29bfe"
C_DONE_TXT = "#a29bfe"
BG_COLOR   = "#1e2130"
PANEL_BG   = "#13161f"
TEXT_COLOR = "#f0f0f0"
BTN_COLOR  = "#2a2f45"
BTN_HOVER  = "#3d4466"
BTN_PLAY   = "#26de81"
BTN_PAUSE  = "#f0a500"

# ── Captura de frames ─────────────────────────────────────────
frames = []

def _snap(A, state, p, r, q=None, highlight=None, desc="", etapa=""):
    frames.append({
        "arr"      : A[:],
        "state"    : state,
        "p"        : p,
        "r"        : r,
        "q"        : q,
        "highlight": highlight[:] if highlight else [],
        "desc"     : desc,
        "etapa"    : etapa,
    })

def merge_capture(A, p, q, r, num_fusao):
    L = A[p : q + 1]
    R = A[q + 1 : r + 1]
    base = f"Fusao #{num_fusao}  A[{p}..{r}]   L={L}   R={R}"
    _snap(A, "fusao", p, r, q, [], base,
          f"Fusao #{num_fusao}: inicio A[{p}..{r}]")

    SENT = float('inf')
    L.append(SENT); R.append(SENT)
    i = j = 0
    merged = []
    for k in range(p, r + 1):
        if L[i] <= R[j]:
            A[k] = L[i]; src = "Esq"; i += 1
        else:
            A[k] = R[j]; src = "Dir"; j += 1
        merged.append(k)
        _snap(A, "fusao", p, r, q, merged[:],
              f"{base}\n   k={k}: coloca {A[k]} (de {src})",
              f"Fusao #{num_fusao}: k={k}, valor={A[k]}")

    _snap(A, "fusao_ok", p, r, q, list(range(p, r + 1)),
          f"Fusao #{num_fusao} concluida:  A[{p}..{r}] = {A[p:r+1]}",
          f"Fusao #{num_fusao}: A[{p}..{r}] OK")

_fusao_cnt = [0]

def merge_sort_capture(A, p, r):
    if p < r:
        q = (p + r) // 2
        _snap(A, "divisao", p, r, q, [],
              f"Divisao  A[{p}..{r}]  ->  A[{p}..{q}] + A[{q+1}..{r}]   (q={q})",
              f"Divisao: A[{p}..{r}]")
        merge_sort_capture(A, p, q)
        merge_sort_capture(A, q + 1, r)
        _fusao_cnt[0] += 1
        merge_capture(A, p, q, r, _fusao_cnt[0])
    else:
        _snap(A, "base", p, r, None, [],
              f"Caso base: A[{p}] = [{A[p]}]  (ja ordenado)",
              f"Base: A[{p}]")


# ── Construtor do grafico ─────────────────────────────────────
def build_chart(A_orig):
    global frames
    frames = []
    _fusao_cnt[0] = 0

    A = A_orig[:]
    n = len(A)

    _snap(A, "inicio", 0, n - 1, None, [],
          f"Array inicial: {A}", "Inicio")
    merge_sort_capture(A, 0, n - 1)
    _snap(A, "done", 0, n - 1, None, list(range(n)),
          f"Array ordenado: {A}", "Concluido!")

    total   = len(frames)
    max_val = max(A_orig)

    # ── Estado de reproducao ─────────────────────────────────
    state = {
        "fi"      : 0,
        "playing" : False,
        "timer"   : None,
    }

    # ── Layout da figura ─────────────────────────────────────
    fig = plt.figure(figsize=(max(11, n), 8), facecolor=BG_COLOR)
    fig.suptitle("Merge Sort — Visualizacao por Estagios",
                 color=TEXT_COLOR, fontsize=13, fontweight="bold", y=0.99)

    # Eixo principal das barras
    ax = fig.add_axes([0.05, 0.30, 0.90, 0.62], facecolor=BG_COLOR)

    # Painel de texto informativo
    ax_info = fig.add_axes([0.05, 0.185, 0.90, 0.09], facecolor=PANEL_BG)
    ax_info.axis("off")

    # Eixos dos botoes e slider
    ax_prev   = fig.add_axes([0.05,  0.07, 0.10, 0.075])
    ax_play   = fig.add_axes([0.175, 0.07, 0.13, 0.075])
    ax_next   = fig.add_axes([0.325, 0.07, 0.10, 0.075])
    ax_reset  = fig.add_axes([0.435, 0.07, 0.10, 0.075])
    ax_slider = fig.add_axes([0.58,  0.085, 0.36, 0.04])

    # ── Barras ───────────────────────────────────────────────
    bars = ax.bar(range(n), A_orig,
                  color=C_DEFAULT, edgecolor="#111", linewidth=0.6, width=0.7)

    val_labels = [
        ax.text(i, A_orig[i] + max_val * 0.01, str(A_orig[i]),
                ha="center", va="bottom",
                color=TEXT_COLOR, fontsize=9, fontweight="bold")
        for i in range(n)
    ]

    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(0, max_val * 1.20)
    ax.set_xticks(range(n))
    ax.set_xticklabels([f"[{i}]" for i in range(n)],
                        color="#888", fontsize=8)
    ax.tick_params(axis="y", colors="#555")
    ax.spines[:].set_visible(False)
    ax.yaxis.set_visible(False)

    # Legenda
    leg_items = [
        mpatches.Patch(color=C_DEFAULT, label="Normal"),
        mpatches.Patch(color=C_ACTIVE,  label="Sub-lista activa"),
        mpatches.Patch(color=C_LEFT,    label="Esquerda (L)"),
        mpatches.Patch(color=C_RIGHT,   label="Direita (R)"),
        mpatches.Patch(color=C_MERGE,   label="Ja fundido"),
        mpatches.Patch(color=C_SORTED,  label="Ordenado"),
    ]
    ax.legend(handles=leg_items, loc="upper right",
              facecolor="#2a2f45", edgecolor="#444",
              labelcolor=TEXT_COLOR, fontsize=7.5, framealpha=0.9)

    # Contador frame / total
    frame_lbl = ax.text(0.01, 0.97, f"Frame 1 / {total}",
                        transform=ax.transAxes,
                        color="#aaaaaa", fontsize=8, va="top")

    # Texto descritivo
    info_text = ax_info.text(
        0.5, 0.5, frames[0]["desc"],
        transform=ax_info.transAxes,
        color=TEXT_COLOR, fontsize=8.5, ha="center", va="center",
        fontfamily="monospace",
        bbox=dict(boxstyle="round,pad=0.3", facecolor=PANEL_BG, edgecolor="#333")
    )

    # ── Botoes ───────────────────────────────────────────────
    btn_style = dict(color=BTN_COLOR, hovercolor=BTN_HOVER)

    btn_prev  = widgets.Button(ax_prev,  "< Anterior", **btn_style)
    btn_play  = widgets.Button(ax_play,  "  Play  ",   color=BTN_PLAY, hovercolor="#1fc96a")
    btn_next  = widgets.Button(ax_next,  "Proximo >",  **btn_style)
    btn_reset = widgets.Button(ax_reset, "Reiniciar",  **btn_style)

    for btn in (btn_prev, btn_play, btn_next, btn_reset):
        btn.label.set_color(TEXT_COLOR)
        btn.label.set_fontsize(9)
        btn.label.set_fontweight("bold")

    # Slider
    slider = widgets.Slider(
        ax_slider, "Frame", 1, total,
        valinit=1, valstep=1,
        color="#5b8dee",
    )
    ax_slider.set_facecolor("#1a1f33")
    slider.label.set_color(TEXT_COLOR)
    slider.valtext.set_color(TEXT_COLOR)

    # ── Render de um frame ───────────────────────────────────
    def render(fi):
        fi = max(0, min(fi, total - 1))
        state["fi"] = fi

        f      = frames[fi]
        arr    = f["arr"]
        fstate = f["state"]
        p      = f["p"]
        r      = f["r"]
        q      = f["q"]
        hl     = set(f["highlight"])

        for i, (bar, lbl) in enumerate(zip(bars, val_labels)):
            v = arr[i]
            bar.set_height(v)
            lbl.set_y(v + max_val * 0.01)
            lbl.set_text(str(v))

            if fstate == "done":
                bar.set_color(C_SORTED);  lbl.set_color(C_SORTED)
            elif fstate == "base":
                if i == p:
                    bar.set_color(C_ACTIVE);  lbl.set_color(C_ACTIVE)
                else:
                    bar.set_color(C_DEFAULT); lbl.set_color(TEXT_COLOR)
            elif fstate in ("fusao", "fusao_ok"):
                if i in hl:
                    bar.set_color(C_MERGE);   lbl.set_color(C_MERGE)
                elif q is not None and p <= i <= q:
                    bar.set_color(C_LEFT);    lbl.set_color(C_LEFT)
                elif q is not None and q < i <= r:
                    bar.set_color(C_RIGHT);   lbl.set_color(C_RIGHT)
                else:
                    bar.set_color(C_DEFAULT); lbl.set_color(TEXT_COLOR)
            elif fstate == "divisao":
                if p <= i <= r:
                    bar.set_color(C_ACTIVE);  lbl.set_color(C_ACTIVE)
                else:
                    bar.set_color(C_DEFAULT); lbl.set_color(TEXT_COLOR)
            else:
                bar.set_color(C_DEFAULT); lbl.set_color(TEXT_COLOR)

        frame_lbl.set_text(f"Frame {fi + 1} / {total}   |   {f['etapa']}")
        info_text.set_text(f["desc"])

        # Sincronizar slider sem disparar callback
        slider.eventson = False
        slider.set_val(fi + 1)
        slider.eventson = True

        # Cor do botao play/pause
        if state["playing"]:
            btn_play.label.set_text("  Pause  ")
            btn_play.ax.set_facecolor(BTN_PAUSE)
        else:
            btn_play.label.set_text("  Play   ")
            btn_play.ax.set_facecolor(BTN_PLAY)

        fig.canvas.draw_idle()

    # ── Timer de reproducao automatica ───────────────────────
    interval_ms = max(250, 1600 // max(total, 1))

    def tick(_):
        if state["playing"]:
            nxt = state["fi"] + 1
            if nxt >= total:
                state["playing"] = False
                render(state["fi"])
            else:
                render(nxt)

    state["timer"] = fig.canvas.new_timer(interval=interval_ms)
    state["timer"].add_callback(tick, None)
    state["timer"].start()

    # ── Callbacks dos botoes ─────────────────────────────────
    def on_prev(_):
        state["playing"] = False
        render(state["fi"] - 1)

    def on_next(_):
        state["playing"] = False
        render(state["fi"] + 1)

    def on_play(_):
        state["playing"] = not state["playing"]
        if state["playing"] and state["fi"] >= total - 1:
            state["fi"] = 0        # reinicia do principio
        render(state["fi"])

    def on_reset(_):
        state["playing"] = False
        render(0)

    def on_slider(val):
        state["playing"] = False
        render(int(val) - 1)

    btn_prev.on_clicked(on_prev)
    btn_play.on_clicked(on_play)
    btn_next.on_clicked(on_next)
    btn_reset.on_clicked(on_reset)
    slider.on_changed(on_slider)

    # ── Teclas de atalho ─────────────────────────────────────
    def on_key(event):
        if event.key == "right":
            on_next(None)
        elif event.key == "left":
            on_prev(None)
        elif event.key == " ":
            on_play(None)
        elif event.key == "r":
            on_reset(None)

    fig.canvas.mpl_connect("key_press_event", on_key)

    # Render inicial
    render(0)

    # Rodape com atalhos
    fig.text(0.5, 0.01,
             "Teclas: [Espaco] Play/Pause   [<-] Anterior   [->] Proximo   [R] Reiniciar",
             ha="center", color="#666", fontsize=7.5)

    plt.show()


# ── Programa Principal ────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  MERGE SORT -- Visualizacao Grafica com Controlos")
    print("=" * 55)
    print("\nOpcoes:")
    print("  1 - Array de exemplo  [38, 27, 43, 3, 9, 82, 10]")
    print("  2 - Introduzir array manualmente")
    print("  3 - Array aleatorio")
    opcao = input("\nEscolha (1/2/3): ").strip()

    if opcao == "2":
        entrada = input("Introduza os numeros separados por espacos: ")
        try:
            A = list(map(int, entrada.split()))
            if not A:
                raise ValueError
        except ValueError:
            print("Entrada invalida. A usar array de exemplo.")
            A = [38, 27, 43, 3, 9, 82, 10]
    elif opcao == "3":
        n = input("Quantos elementos? (2-20, padrao 8): ").strip()
        n = int(n) if n.isdigit() and 2 <= int(n) <= 20 else 8
        A = random.sample(range(1, 100), n)
        print(f"Array gerado: {A}")
    else:
        A = [38, 27, 43, 3, 9, 82, 10]

    print(f"\nArray: {A}")
    print("A abrir grafico... (fecha a janela para terminar)\n")
    build_chart(A)
