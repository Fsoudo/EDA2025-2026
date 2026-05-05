import tkinter as tk
from tkinter import ttk
import time
import threading

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None # z.p no pseudocódigo
        self.x = 0
        self.y = 0
        self.canvas_id = None
        self.text_id = None

class BST:
    def __init__(self):
        self.root = None

    # TREE-INSERT(T, z) - Fiel ao pseudocódigo da imagem
    def insert_iterative(self, z_val, visualizer):
        z = Node(z_val) # O nó a ser inserido
        
        # Linha 1: y = NIL
        y = None 
        
        # Linha 2: x = T.root
        x = self.root 
        
        if visualizer.status_label:
            visualizer.status_label.config(text=f"Pesquisando local para {z.value}...", fg="#cdd6f4")
        
        # Linha 3: while x != NIL
        while x is not None:
            # Linha 4: y = x
            y = x 
            visualizer.highlight_node(y, "#f9e2af", "y") # Highlight y (trailing pointer)
            time.sleep(visualizer.animation_speed)

            # Linha 5: if z.key < x.key
            if z.value < x.value:
                # Linha 6: x = x.left
                visualizer.status_label.config(text=f"{z.value} < {x.value} -> x = x.left", fg="#89b4fa")
                x = x.left
            else:
                # Linha 7: else x = x.right
                visualizer.status_label.config(text=f"{z.value} >= {x.value} -> x = x.right", fg="#fab387")
                x = x.right
            
            if x:
                visualizer.highlight_node(x, "#89b4fa", "x") # Highlight x
                time.sleep(visualizer.animation_speed)
            
            visualizer.draw_tree() # Limpa destaques para a próxima iteração

        # Linha 8: z.p = y
        z.parent = y 

        # Linha 9: if y == NIL
        if y is None:
            # Linha 10: T.root = z
            self.root = z
            visualizer.status_label.config(text="Árvore vazia: T.root = z", fg="#a6e3a1")
        # Linha 11: elseif z.key < y.key
        elif z.value < y.value:
            # Linha 12: y.left = z
            y.left = z
            visualizer.status_label.config(text=f"{z.value} < {y.value} -> y.left = z", fg="#a6e3a1")
        # Linha 13: else y.right = z
        else:
            y.right = z
            visualizer.status_label.config(text=f"{z.value} >= {y.value} -> y.right = z", fg="#a6e3a1")
        
        visualizer.draw_tree()
        visualizer.highlight_node(z, "#a6e3a1") # Destaca o nó inserido

class InsertVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Iterative BST Insert (TREE-INSERT)")
        self.root.geometry("1000x750")
        self.root.configure(bg="#1e1e2e")

        self.tree = BST()
        self.animation_speed = 0.8
        self.is_animating = False
        self.status_label = None # Inicializa como None para evitar erros

        self._setup_ui()
        
        # Agora que a UI existe, podemos inserir os nós iniciais (sem animação longa)
        self.animation_speed = 0.1 # Velocidade rápida para o setup
        for val in [6,5,7,2,5,8]:
            self.tree.insert_iterative(val, self)
        self.animation_speed = 0.8 # Velocidade normal para o utilizador

        self.draw_tree()

    def _setup_ui(self):
        header = tk.Frame(self.root, bg="#1e1e2e", pady=20)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="Algoritmo TREE-INSERT (Iterativo)", 
                 font=("Helvetica", 22, "bold"), fg="#cdd6f4", bg="#1e1e2e").pack()

        self.status_label = tk.Label(header, text="Introduza um valor para inserir", 
                                     font=("Helvetica", 13, "italic"), fg="#94e2d5", bg="#1e1e2e")
        self.status_label.pack(pady=5)

        self.canvas = tk.Canvas(self.root, bg="#181825", highlightthickness=0)
        self.canvas.pack(expand=True, fill=tk.BOTH, padx=40, pady=10)

        controls = tk.Frame(self.root, bg="#1e1e2e", pady=20)
        controls.pack(fill=tk.X)

        tk.Label(controls, text="Valor z:", fg="#cdd6f4", bg="#1e1e2e", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=(40, 10))
        
        self.entry_val = tk.Entry(controls, font=("Helvetica", 14), width=10, bg="#313244", fg="#cdd6f4", insertbackground="white")
        self.entry_val.pack(side=tk.LEFT, padx=10)

        self.btn_insert = tk.Button(controls, text="Executar TREE-INSERT", command=self.start_insert,
                                    bg="#a6e3a1", fg="#11111b", font=("Helvetica", 12, "bold"),
                                    activebackground="#94e2d5", relief=tk.FLAT, padx=20)
        self.btn_insert.pack(side=tk.LEFT, padx=10)

        self.btn_reset = tk.Button(controls, text="Limpar Tudo", command=self.clear_tree,
                                   bg="#f38ba8", fg="#11111b", font=("Helvetica", 12, "bold"),
                                   activebackground="#eba0ac", relief=tk.FLAT, padx=20)
        self.btn_reset.pack(side=tk.LEFT, padx=10)

        # Nota de Complexidade
        self.info_frame = tk.Frame(controls, bg="#313244", padx=15, pady=5)
        self.info_frame.pack(side=tk.RIGHT, padx=40)
        tk.Label(self.info_frame, text="COMPLEXIDADE:", fg="#bac2de", bg="#313244", font=("Helvetica", 10, "bold")).pack()
        tk.Label(self.info_frame, text="O(h)", fg="#fab387", bg="#313244", font=("Helvetica", 20, "bold")).pack()

    def draw_tree(self):
        self.canvas.delete("all")
        if not self.tree.root: return
        
        # Novo algoritmo de posicionamento (Inorder Layout)
        # 1. Obter a ordem dos nós para o eixo X
        nodes_in_order = []
        def get_inorder(node):
            if node:
                get_inorder(node.left)
                nodes_in_order.append(node)
                get_inorder(node.right)
        get_inorder(self.tree.root)
        
        # 2. Definir coordenadas X baseadas no rank e Y baseadas na profundidade
        canvas_width = self.canvas.winfo_width()
        if canvas_width < 100: canvas_width = 1000 # Fallback
        
        spacing_x = (canvas_width - 100) / (len(nodes_in_order) if len(nodes_in_order) > 1 else 1)
        
        for i, node in enumerate(nodes_in_order):
            node.x = 50 + i * spacing_x
            
        def set_y(node, depth):
            if node:
                node.y = 80 + depth * 80
                set_y(node.left, depth + 1)
                set_y(node.right, depth + 1)
        
        set_y(self.tree.root, 0)
        
        # 3. Desenhar
        self._draw_node_recursive(self.tree.root)

    def _draw_node_recursive(self, node):
        if not node: return
        if node.left:
            self.canvas.create_line(node.x, node.y, node.left.x, node.left.y, fill="#585b70", width=2)
            self._draw_node_recursive(node.left)
        if node.right:
            self.canvas.create_line(node.x, node.y, node.right.x, node.right.y, fill="#585b70", width=2)
            self._draw_node_recursive(node.right)

        r = 20
        node.canvas_id = self.canvas.create_oval(node.x-r, node.y-r, node.x+r, node.y+r, 
                                               fill="#313244", outline="#cdd6f4", width=2)
        node.text_id = self.canvas.create_text(node.x, node.y, text=str(node.value), 
                                              fill="#cdd6f4", font=("Helvetica", 10, "bold"))

    def highlight_node(self, node, color, label=""):
        if not node: return
        self.canvas.itemconfig(node.canvas_id, fill=color, outline="#11111b")
        self.canvas.itemconfig(node.text_id, fill="#11111b")
        if label:
            self.canvas.create_text(node.x, node.y - 35, text=label, fill=color, font=("Helvetica", 12, "bold"), tags="label")
        self.root.update()

    def start_insert(self):
        if self.is_animating: return
        try:
            val = int(self.entry_val.get())
        except ValueError: return

        self.is_animating = True
        self.entry_val.delete(0, tk.END)
        
        def run():
            self.draw_tree()
            self.tree.insert_iterative(val, self)
            self.is_animating = False

        threading.Thread(target=run, daemon=True).start()

    def clear_tree(self):
        if self.is_animating: return
        self.tree.root = None
        self.draw_tree()
        self.status_label.config(text="Árvore limpa.", fg="#94e2d5")

if __name__ == "__main__":
    root = tk.Tk()
    app = InsertVisualizer(root)
    root.mainloop()
