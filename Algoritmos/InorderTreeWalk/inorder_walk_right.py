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

class RightSkewedBST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if not self.root:
            self.root = Node(value)
        else:
            # Forçar inserção apenas à direita para este exemplo
            curr = self.root
            while curr.right:
                curr = curr.right
            curr.right = Node(value)

class TreeVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Inorder Walk - Right Skewed Tree")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e2e")

        self.tree = RightSkewedBST()
        # Inserindo valores crescentes para criar a expansão à direita
        for val in [6,5,7,2,5,8]:
            self.tree.insert(val)

        self.animation_speed = 0.5
        self.is_animating = False
        self.stop_animation = False
        self.iteration_count = 0

        self._setup_ui()
        self.draw_tree()

    def _setup_ui(self):
        header = tk.Frame(self.root, bg="#1e1e2e", pady=20)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="Inorder Walk: Árvore Degenerada (Direita)", 
                 font=("Helvetica", 20, "bold"), fg="#cdd6f4", bg="#1e1e2e").pack()

        self.status_label = tk.Label(header, text="Pronto para começar", 
                                     font=("Helvetica", 12, "italic"), fg="#94e2d5", bg="#1e1e2e")
        self.status_label.pack(pady=5)

        self.canvas = tk.Canvas(self.root, bg="#181825", highlightthickness=0)
        self.canvas.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)

        controls = tk.Frame(self.root, bg="#1e1e2e", pady=20)
        controls.pack(fill=tk.X)

        self.btn_start = tk.Button(controls, text="Começar Inorder Walk", command=self.start_walk,
                                   bg="#a6e3a1", fg="#11111b", font=("Helvetica", 12, "bold"),
                                   activebackground="#94e2d5", relief=tk.FLAT, padx=20)
        self.btn_start.pack(side=tk.LEFT, padx=20)

        self.btn_reset = tk.Button(controls, text="Reiniciar", command=self.reset_tree,
                                   bg="#f38ba8", fg="#11111b", font=("Helvetica", 12, "bold"),
                                   activebackground="#eba0ac", relief=tk.FLAT, padx=20)
        self.btn_reset.pack(side=tk.LEFT, padx=10)

        self.output_label = tk.Label(self.root, text="Resultado: ", font=("Consolas", 14), 
                                     fg="#fab387", bg="#1e1e2e", pady=10)
        self.output_label.pack()

    def draw_tree(self):
        self.canvas.delete("all")
        if not self.tree.root:
            return
        
        # Posicionamento diagonal para árvore à direita
        self._set_positions(self.tree.root, 100, 100)
        self._draw_node_recursive(self.tree.root)

    def _set_positions(self, node, x, y):
        if not node: return
        node.x = x
        node.y = y
        # Só expande para a direita e para baixo
        if node.right:
            self._set_positions(node.right, x + 80, y + 60)

    def _draw_node_recursive(self, node):
        if not node: return
        if node.right:
            self.canvas.create_line(node.x, node.y, node.right.x, node.right.y, fill="#585b70", width=2)
            self._draw_node_recursive(node.right)

        r = 20
        node.canvas_id = self.canvas.create_oval(node.x-r, node.y-r, node.x+r, node.y+r, 
                                               fill="#313244", outline="#cdd6f4", width=2)
        node.text_id = self.canvas.create_text(node.x, node.y, text=str(node.value), 
                                              fill="#cdd6f4", font=("Helvetica", 10, "bold"))

    def highlight_node(self, node, color="#f9e2af"):
        self.canvas.itemconfig(node.canvas_id, fill=color, outline="#11111b")
        self.canvas.itemconfig(node.text_id, fill="#11111b")
        self.root.update()

    def visit_node(self, node):
        self.canvas.itemconfig(node.canvas_id, fill="#a6e3a1", outline="#11111b")
        self.canvas.itemconfig(node.text_id, fill="#11111b")
        current_text = self.output_label.cget("text")
        self.output_label.config(text=current_text + str(node.value) + " ")
        self.root.update()

    def inorder_walk_anim(self, node):
        self.iteration_count += 1
        
        if not node or self.stop_animation:
            if not self.stop_animation:
                print(f"Chamada #{self.iteration_count}: Nó é None")
                self.status_label.config(text=f"[Iteração #{self.iteration_count}] Argumento: None", fg="#f38ba8")
                time.sleep(self.animation_speed/2)
            return

        # 1. Esquerda (Vazia nesta árvore)
        print(f"--> Chamada #{self.iteration_count} | Nó: {node.value}")
        self.status_label.config(text=f"[Iteração #{self.iteration_count}] Nó({node.value}) -> Esquerda", fg="#89b4fa")
        self.highlight_node(node, "#89b4fa")
        time.sleep(self.animation_speed)
        
        # 2. Visita
        self.status_label.config(text=f"Nó({node.value}) -> VISITANDO", fg="#f9e2af")
        self.highlight_node(node, "#f9e2af")
        time.sleep(self.animation_speed)
        self.visit_node(node)
        time.sleep(self.animation_speed)

        # 3. Direita
        self.status_label.config(text=f"Nó({node.value}) -> Indo para DIREITA", fg="#fab387")
        self.inorder_walk_anim(node.right)
        
        self.status_label.config(text=f"Nó({node.value}) -> Finalizado", fg="#a6e3a1")

    def start_walk(self):
        if self.is_animating: return
        self.is_animating = True
        self.stop_animation = False
        self.iteration_count = 0
        self.output_label.config(text="Resultado: ")
        self.draw_tree()
        threading.Thread(target=lambda: (self.inorder_walk_anim(self.tree.root), 
                                          setattr(self, 'is_animating', False)), daemon=True).start()

    def reset_tree(self):
        self.stop_animation = True
        self.draw_tree()
        self.output_label.config(text="Resultado: ")
        self.status_label.config(text="Pronto para começar", fg="#94e2d5")
        self.is_animating = False

if __name__ == "__main__":
    root = tk.Tk()
    app = TreeVisualizer(root)
    root.mainloop()
