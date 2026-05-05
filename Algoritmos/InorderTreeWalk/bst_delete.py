import tkinter as tk
from tkinter import ttk
import time
import threading

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.x = 0
        self.y = 0
        self.canvas_id = None
        self.text_id = None

class BST:
    def __init__(self):
        self.root = None

    # TRANSPLANT(T, u, v) - Fiel ao pseudocódigo do manual
    def transplant(self, u, v, vis):
        vis.log(f"TRANSPLANT({u.value}, {v.value if v else 'NIL'})", "#fab387")
        time.sleep(vis.speed)

        # Linha 1: if u.p == NIL
        if u.parent is None:
            self.root = v                                           # Linha 2: T.root = v
            vis.log("L2: u era raiz → T.root = v", "#f9e2af")
        elif u == u.parent.left:                                   # Linha 3: elseif u == u.p.left
            u.parent.left = v                                      # Linha 4: u.p.left = v
            vis.log("L4: u era filho esquerdo → u.p.left = v", "#f9e2af")
        else:
            u.parent.right = v                                     # Linha 5: u.p.right = v
            vis.log("L5: u era filho direito → u.p.right = v", "#f9e2af")

        if v is not None:                                          # Linha 6: if v != NIL
            v.parent = u.parent                                    # Linha 7: v.p = u.p
            vis.log("L7: v.p = u.p", "#f9e2af")

        time.sleep(vis.speed)
        vis.draw_tree()

    def tree_delete(self, z, vis):
        vis.log(f"Iniciando TREE-DELETE({z.value})", "#f38ba8")
        vis.highlight_node(z, "#f38ba8")
        time.sleep(vis.speed)

        if z.left is None:
            vis.log(f"Sem filho esquerdo → TRANSPLANT({z.value}, {z.right.value if z.right else 'NIL'})", "#89b4fa")
            self.transplant(z, z.right, vis)
        elif z.right is None:
            vis.log(f"Sem filho direito → TRANSPLANT({z.value}, {z.left.value})", "#89b4fa")
            self.transplant(z, z.left, vis)
        else:
            # Dois filhos → encontrar sucessor mínimo
            y = self.minimum(z.right)
            vis.log(f"Dois filhos → sucessor mínimo: {y.value}", "#cba6f7")
            vis.highlight_node(y, "#cba6f7")
            time.sleep(vis.speed)

            if y.parent != z:
                vis.log(f"Sucessor não é filho direto → TRANSPLANT({y.value}, {y.right.value if y.right else 'NIL'})", "#89b4fa")
                self.transplant(y, y.right, vis)
                y.right = z.right
                y.right.parent = y

            self.transplant(z, y, vis)
            y.left = z.left
            y.left.parent = y

        vis.draw_tree()
        vis.log(f"✓ Remoção de {z.value} concluída!", "#a6e3a1")

    def minimum(self, node):
        while node.left:
            node = node.left
        return node

    def search(self, value):
        curr = self.root
        while curr and curr.value != value:
            curr = curr.left if value < curr.value else curr.right
        return curr

    def insert(self, value):
        z = Node(value)
        y = None
        x = self.root
        while x:
            y = x
            x = x.left if z.value < x.value else x.right
        z.parent = y
        if not y:
            self.root = z
        elif z.value < y.value:
            y.left = z
        else:
            y.right = z


INITIAL_VALUES = [50, 30, 70, 20, 40, 60, 80, 35, 45]

class DeleteVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Remoção em BST — TRANSPLANT Visualization")
        self.root.geometry("1100x820")
        self.root.configure(bg="#1e1e2e")

        self.tree = BST()
        self.is_animating = False
        self._speed_val = 1.0
        self.selected_node = None  # Nó clicado pelo utilizador

        self._setup_ui()
        # Forçar Tkinter a calcular o layout antes de desenhar
        self.root.update_idletasks()
        self._reset_tree()
        # Redesenhar quando a janela for redimensionada
        self.canvas.bind("<Configure>", lambda e: self.draw_tree())

    @property
    def speed(self):
        return self._speed_val

    # ─── UI ──────────────────────────────────────────────────────────────────
    def _setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#1e1e2e", pady=14)
        header.pack(fill=tk.X)
        tk.Label(header, text="Remoção em BST  ·  Procedimento TRANSPLANT",
                 font=("Helvetica", 22, "bold"), fg="#cdd6f4", bg="#1e1e2e").pack()
        self.status_label = tk.Label(header, text="Clique num nó para o selecionar e depois prima Remover",
                                     font=("Helvetica", 13, "italic"), fg="#94e2d5", bg="#1e1e2e")
        self.status_label.pack(pady=4)

        # Canvas
        self.canvas = tk.Canvas(self.root, bg="#181825", highlightthickness=0, cursor="hand2")
        self.canvas.pack(expand=True, fill=tk.BOTH, padx=30, pady=(0, 6))
        self.canvas.bind("<Button-1>", self._on_canvas_click)

        # ── Controlo principal ────────────────────────────────────────────────
        ctrl = tk.Frame(self.root, bg="#1e1e2e", pady=12)
        ctrl.pack(fill=tk.X, padx=30)

        # Remover
        tk.Label(ctrl, text="Remover:", fg="#cdd6f4", bg="#1e1e2e",
                 font=("Helvetica", 12)).grid(row=0, column=0, padx=(0, 6), sticky="w")
        self.entry_del = tk.Entry(ctrl, font=("Helvetica", 14), width=7,
                                  bg="#313244", fg="#cdd6f4", insertbackground="white")
        self.entry_del.grid(row=0, column=1, padx=4)
        self.entry_del.bind("<Return>", lambda e: self.start_delete())
        tk.Button(ctrl, text="Remover Nó", command=self.start_delete,
                  bg="#f38ba8", fg="#11111b", font=("Helvetica", 11, "bold"),
                  relief=tk.FLAT, padx=14, cursor="hand2").grid(row=0, column=2, padx=6)
        # Etiqueta do nó selecionado
        self.selected_label = tk.Label(ctrl, text="Nenhum nó selecionado",
                                       fg="#cba6f7", bg="#1e1e2e", font=("Helvetica", 11, "italic"))
        self.selected_label.grid(row=0, column=3, padx=(10, 4))

        # Separador
        tk.Label(ctrl, text="│", fg="#45475a", bg="#1e1e2e",
                 font=("Helvetica", 16)).grid(row=0, column=4, padx=10)

        # Inserir
        tk.Label(ctrl, text="Inserir:", fg="#cdd6f4", bg="#1e1e2e",
                 font=("Helvetica", 12)).grid(row=0, column=4, padx=(0, 6), sticky="w")
        self.entry_ins = tk.Entry(ctrl, font=("Helvetica", 14), width=7,
                                  bg="#313244", fg="#cdd6f4", insertbackground="white")
        self.entry_ins.grid(row=0, column=6, padx=4)
        self.entry_ins.bind("<Return>", lambda e: self.insert_node())
        tk.Button(ctrl, text="Inserir Nó", command=self.insert_node,
                  bg="#a6e3a1", fg="#11111b", font=("Helvetica", 11, "bold"),
                  relief=tk.FLAT, padx=14, cursor="hand2").grid(row=0, column=7, padx=6)

        # Separador
        tk.Label(ctrl, text="│", fg="#45475a", bg="#1e1e2e",
                 font=("Helvetica", 16)).grid(row=0, column=8, padx=10)

        # Reiniciar
        tk.Button(ctrl, text="⟳ Reiniciar", command=self._reset_tree,
                  bg="#313244", fg="#cdd6f4", font=("Helvetica", 11, "bold"),
                  relief=tk.FLAT, padx=14, cursor="hand2").grid(row=0, column=9, padx=6)

        # ── Velocidade e legenda ──────────────────────────────────────────────
        bottom = tk.Frame(self.root, bg="#1e1e2e", pady=8)
        bottom.pack(fill=tk.X, padx=30)

        # Slider velocidade
        tk.Label(bottom, text="Velocidade:", fg="#bac2de", bg="#1e1e2e",
                 font=("Helvetica", 10)).pack(side=tk.LEFT)
        self.speed_slider = ttk.Scale(bottom, from_=0.1, to=2.0, orient=tk.HORIZONTAL,
                                      length=140, command=self._on_speed)
        self.speed_slider.set(1.0)
        self.speed_slider.pack(side=tk.LEFT, padx=(6, 20))

        # Legenda de cores
        legend = [
            ("#f38ba8", "A remover"),
            ("#cba6f7", "Sucessor"),
            ("#89b4fa", "Em análise"),
            ("#f9e2af", "TRANSPLANT"),
            ("#a6e3a1", "Concluído"),
        ]
        for color, label in legend:
            dot = tk.Canvas(bottom, width=12, height=12, bg="#1e1e2e", highlightthickness=0)
            dot.create_oval(1, 1, 11, 11, fill=color, outline="")
            dot.pack(side=tk.LEFT, padx=(10, 2))
            tk.Label(bottom, text=label, fg=color, bg="#1e1e2e",
                     font=("Helvetica", 9)).pack(side=tk.LEFT, padx=(0, 4))

        # Complexidade
        info = tk.Frame(bottom, bg="#313244", padx=12, pady=3)
        info.pack(side=tk.RIGHT)
        tk.Label(info, text="Complexidade:", fg="#bac2de", bg="#313244",
                 font=("Helvetica", 9, "bold")).pack(side=tk.LEFT)
        tk.Label(info, text=" O(h)", fg="#fab387", bg="#313244",
                 font=("Helvetica", 13, "bold")).pack(side=tk.LEFT)

    # ─── Helpers ─────────────────────────────────────────────────────────────
    def _on_speed(self, val):
        self._speed_val = float(val)

    def _reset_tree(self):
        if self.is_animating: return
        self.tree = BST()
        self.selected_node = None
        for v in INITIAL_VALUES:
            self.tree.insert(v)
        self.draw_tree()
        self.log("Árvore reposta.", "#94e2d5")
        self.selected_label.config(text="Nenhum nó selecionado")

    def log(self, msg, color="#cdd6f4"):
        self.status_label.config(text=msg, fg=color)
        self.root.update()

    def draw_tree(self):
        self.canvas.delete("all")
        if not self.tree.root: return

        # Inorder Layout: X pelo rank, Y pela profundidade
        order = []
        def inorder(n):
            if n:
                inorder(n.left)
                order.append(n)
                inorder(n.right)
        inorder(self.tree.root)

        self.root.update_idletasks()
        w = self.canvas.winfo_width()
        if w < 200: w = 1040  # fallback mais seguro
        sx = (w - 80) / max(len(order) - 1, 1)
        for i, n in enumerate(order):
            n.x = 40 + i * sx

        def set_y(n, d):
            if n:
                n.y = 60 + d * 75
                set_y(n.left, d + 1)
                set_y(n.right, d + 1)
        set_y(self.tree.root, 0)

        self._draw_recursive(self.tree.root)

    def _draw_recursive(self, node):
        if not node: return
        for child in (node.left, node.right):
            if child:
                self.canvas.create_line(node.x, node.y, child.x, child.y,
                                        fill="#585b70", width=2)
                self._draw_recursive(child)
        r = 20
        node.canvas_id = self.canvas.create_oval(
            node.x-r, node.y-r, node.x+r, node.y+r,
            fill="#313244", outline="#cdd6f4", width=2)
        node.text_id = self.canvas.create_text(
            node.x, node.y, text=str(node.value),
            fill="#cdd6f4", font=("Helvetica", 10, "bold"))
        # Se este nó está selecionado, destacar com borda colorida
        if node is self.selected_node:
            self.canvas.itemconfig(node.canvas_id, outline="#cba6f7", width=3, fill="#45475a")

    def highlight_node(self, node, color):
        if not node: return
        self.canvas.itemconfig(node.canvas_id, fill=color, outline="#11111b")
        self.canvas.itemconfig(node.text_id, fill="#11111b")
        self.root.update()

    def _on_canvas_click(self, event):
        """Seleciona o nó mais próximo do clique."""
        if self.is_animating: return
        R = 22  # raio de deteção
        clicked = None

        def find_node(node):
            nonlocal clicked
            if not node: return
            if abs(node.x - event.x) <= R and abs(node.y - event.y) <= R:
                clicked = node
                return
            find_node(node.left)
            find_node(node.right)

        find_node(self.tree.root)

        if clicked:
            self.selected_node = clicked
            self.selected_label.config(text=f"Selecionado: Nó({clicked.value})")
            self.log(f"Nó {clicked.value} selecionado. Prima 'Remover Nó' para apagar.", "#cba6f7")
            self.draw_tree()  # Redesenhar para mostrar a seleção
        else:
            self.selected_node = None
            self.selected_label.config(text="Nenhum nó selecionado")
            self.draw_tree()

    # ─── Acções ──────────────────────────────────────────────────────────────
    def start_delete(self):
        if self.is_animating: return

        # Prioridade: nó clicado na tela > valor no campo de texto
        node = self.selected_node
        if node is None:
            try:
                val = int(self.entry_del.get())
                node = self.tree.search(val)
            except ValueError:
                pass

        if not node:
            self.log("Clique num nó ou escreva um valor válido.", "#f38ba8")
            return

        self.selected_node = None
        self.selected_label.config(text="Nenhum nó selecionado")
        self.entry_del.delete(0, tk.END)
        self.is_animating = True

        def run():
            self.tree.tree_delete(node, self)
            self.is_animating = False

        threading.Thread(target=run, daemon=True).start()

    def insert_node(self):
        if self.is_animating: return
        try:
            val = int(self.entry_ins.get())
        except ValueError:
            self.log("Introduza um número válido.", "#f38ba8"); return
        self.tree.insert(val)
        self.entry_ins.delete(0, tk.END)
        self.draw_tree()
        self.log(f"Nó {val} inserido.", "#a6e3a1")


if __name__ == "__main__":
    root = tk.Tk()
    app = DeleteVisualizer(root)
    root.mainloop()
