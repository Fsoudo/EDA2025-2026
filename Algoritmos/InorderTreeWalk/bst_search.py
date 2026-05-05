import tkinter as tk
from tkinter import ttk
import time
import threading

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.x = 0
        self.y = 0
        self.canvas_id = None
        self.text_id = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if not self.root:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left:
                self._insert_recursive(node.left, value)
            else:
                node.left = Node(value)
        else:
            if node.right:
                self._insert_recursive(node.right, value)
            else:
                node.right = Node(value)

class SearchVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("BST Search Visualization")
        self.root.geometry("1000x750")
        self.root.configure(bg="#1e1e2e")

        self.tree = BST()
        # Árvore equilibrada para exemplo
        for val in [6,5,7,2,5,8]:
            self.tree.insert(val)

        self.animation_speed = 0.8
        self.is_searching = False
        self.iteration_count = 0

        self._setup_ui()
        self.draw_tree()

    def _setup_ui(self):
        header = tk.Frame(self.root, bg="#1e1e2e", pady=20)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="Pesquisa em Árvore Binária (BST Search)", 
                 font=("Helvetica", 22, "bold"), fg="#cdd6f4", bg="#1e1e2e").pack()

        self.status_label = tk.Label(header, text="Introduza um valor e clique em Pesquisar", 
                                     font=("Helvetica", 13, "italic"), fg="#94e2d5", bg="#1e1e2e")
        self.status_label.pack(pady=5)

        self.canvas = tk.Canvas(self.root, bg="#181825", highlightthickness=0)
        self.canvas.pack(expand=True, fill=tk.BOTH, padx=40, pady=10)

        controls = tk.Frame(self.root, bg="#1e1e2e", pady=20)
        controls.pack(fill=tk.X)

        tk.Label(controls, text="Valor a pesquisar:", fg="#cdd6f4", bg="#1e1e2e", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=(40, 10))
        
        self.entry_search = tk.Entry(controls, font=("Helvetica", 14), width=10, bg="#313244", fg="#cdd6f4", insertbackground="white")
        self.entry_search.pack(side=tk.LEFT, padx=10)
        self.entry_search.bind("<Return>", lambda e: self.start_search())

        self.btn_search = tk.Button(controls, text="Pesquisar", command=self.start_search,
                                    bg="#89b4fa", fg="#11111b", font=("Helvetica", 12, "bold"),
                                    activebackground="#b4befe", relief=tk.FLAT, padx=20)
        self.btn_search.pack(side=tk.LEFT, padx=10)

        self.btn_reset = tk.Button(controls, text="Limpar", command=self.reset_visualization,
                                   bg="#f38ba8", fg="#11111b", font=("Helvetica", 12, "bold"),
                                   activebackground="#eba0ac", relief=tk.FLAT, padx=20)
        self.btn_reset.pack(side=tk.LEFT, padx=10)

        # Passo Contador
        self.counter_frame = tk.Frame(controls, bg="#313244", padx=15, pady=5)
        self.counter_frame.pack(side=tk.RIGHT, padx=40)
        
        tk.Label(self.counter_frame, text="PASSOS:", fg="#bac2de", bg="#313244", font=("Helvetica", 10, "bold")).pack()
        self.counter_val_label = tk.Label(self.counter_frame, text="0", fg="#a6e3a1", bg="#313244", font=("Helvetica", 20, "bold"))
        self.counter_val_label.pack()

    def draw_tree(self):
        self.canvas.delete("all")
        if not self.tree.root: return
        self._set_positions(self.tree.root, 500, 50, 250)
        self._draw_node_recursive(self.tree.root)

    def _set_positions(self, node, x, y, dx):
        if not node: return
        node.x, node.y = x, y
        if node.left: self._set_positions(node.left, x - dx, y + 80, dx / 1.8)
        if node.right: self._set_positions(node.right, x + dx, y + 80, dx / 1.8)

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

    def highlight_node(self, node, color):
        self.canvas.itemconfig(node.canvas_id, fill=color, outline="#11111b")
        self.canvas.itemconfig(node.text_id, fill="#11111b")
        self.root.update()

    def search_anim(self, node, target):
        self.iteration_count += 1
        self.counter_val_label.config(text=str(self.iteration_count))
        
        if not node:
            self.status_label.config(text=f"[Iteração {self.iteration_count}] Chegou a NULL. Valor {target} NÃO ENCONTRADO.", fg="#f38ba8")
            return False

        # Highlight current node being compared
        self.highlight_node(node, "#f9e2af") # Yellow for comparison
        self.status_label.config(text=f"[Iteração {self.iteration_count}] Comparando {target} com {node.value}...", fg="#f9e2af")
        time.sleep(self.animation_speed)

        if target == node.value:
            self.highlight_node(node, "#a6e3a1") # Green for found
            self.status_label.config(text=f"[Iteração {self.iteration_count}] SUCESSO! Valor {target} encontrado!", fg="#a6e3a1")
            return True
        
        if target < node.value:
            self.status_label.config(text=f"[Iteração {self.iteration_count}] {target} < {node.value}. Indo para a ESQUERDA.", fg="#89b4fa")
            time.sleep(self.animation_speed)
            self.highlight_node(node, "#45475a") # Gray out after path taken
            return self.search_anim(node.left, target)
        else:
            self.status_label.config(text=f"[Iteração {self.iteration_count}] {target} > {node.value}. Indo para a DIREITA.", fg="#fab387")
            time.sleep(self.animation_speed)
            self.highlight_node(node, "#45475a") # Gray out after path taken
            return self.search_anim(node.right, target)

    def start_search(self):
        if self.is_searching: return
        
        try:
            target = int(self.entry_search.get())
        except ValueError:
            self.status_label.config(text="Por favor, introduza um número válido.", fg="#f38ba8")
            return

        self.is_searching = True
        self.iteration_count = 0
        self.draw_tree() # Reset colors
        
        def run():
            self.search_anim(self.tree.root, target)
            self.is_searching = False

        threading.Thread(target=run, daemon=True).start()

    def reset_visualization(self):
        self.draw_tree()
        self.entry_search.delete(0, tk.END)
        self.iteration_count = 0
        self.counter_val_label.config(text="0", fg="#a6e3a1")
        self.status_label.config(text="Introduza um valor e clique em Pesquisar", fg="#94e2d5")

if __name__ == "__main__":
    root = tk.Tk()
    app = SearchVisualizer(root)
    root.mainloop()
