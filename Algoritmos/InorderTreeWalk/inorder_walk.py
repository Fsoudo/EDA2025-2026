import tkinter as tk
from tkinter import ttk
import time
import threading

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        # Position for visualization
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

class TreeVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Inorder Tree Walk Visualization")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e2e")

        self.tree = BST()
        # Default values for a balanced-ish tree
        for val in [50, 30, 70, 20, 45, 60, 80, 15, 25, 35, 45, 55, 65, 75, 85]:
            self.tree.insert(val)

        self.animation_speed = 0.5
        self.is_animating = False
        self.stop_animation = False

        self._setup_ui()
        self.draw_tree()

    def _setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#1e1e2e", pady=20)
        header.pack(fill=tk.X)
        
        title = tk.Label(header, text="Inorder Tree Walk (L → Root → R)", 
                         font=("Helvetica", 24, "bold"), fg="#cdd6f4", bg="#1e1e2e")
        title.pack()

        # Canvas for Tree
        self.canvas = tk.Canvas(self.root, bg="#181825", highlightthickness=0)
        self.canvas.pack(expand=True, fill=tk.BOTH, padx=40, pady=20)

        # Controls
        controls = tk.Frame(self.root, bg="#1e1e2e", pady=20)
        controls.pack(fill=tk.X)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton", font=("Helvetica", 12), padding=10)

        self.btn_start = tk.Button(controls, text="Começar Inorder Walk", command=self.start_walk,
                                   bg="#a6e3a1", fg="#11111b", font=("Helvetica", 12, "bold"),
                                   activebackground="#94e2d5", relief=tk.FLAT, padx=20)
        self.btn_start.pack(side=tk.LEFT, padx=20)

        self.btn_reset = tk.Button(controls, text="Reiniciar", command=self.reset_tree,
                                   bg="#f38ba8", fg="#11111b", font=("Helvetica", 12, "bold"),
                                   activebackground="#eba0ac", relief=tk.FLAT, padx=20)
        self.btn_reset.pack(side=tk.LEFT, padx=10)

        # Speed Slider
        tk.Label(controls, text="Velocidade:", fg="#cdd6f4", bg="#1e1e2e", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=(50, 10))
        self.speed_slider = tk.Scale(controls, from_=0.1, to=2.0, resolution=0.1, orient=tk.HORIZONTAL,
                                     bg="#1e1e2e", fg="#cdd6f4", highlightthickness=0, 
                                     command=self.update_speed, troughcolor="#45475a")
        self.speed_slider.set(0.5)
        self.speed_slider.pack(side=tk.LEFT)

        # Output List
        self.output_label = tk.Label(self.root, text="Resultado: ", font=("Consolas", 14), 
                                     fg="#fab387", bg="#1e1e2e", pady=10)
        self.output_label.pack()

    def update_speed(self, val):
        self.animation_speed = float(val)

    def draw_tree(self):
        self.canvas.delete("all")
        if not self.tree.root:
            return
        
        # Calculate positions
        self._set_positions(self.tree.root, 500, 50, 250)
        self._draw_node_recursive(self.tree.root)

    def _set_positions(self, node, x, y, dx):
        if not node:
            return
        node.x = x
        node.y = y
        if node.left:
            self._set_positions(node.left, x - dx, y + 80, dx / 1.8)
        if node.right:
            self._set_positions(node.right, x + dx, y + 80, dx / 1.8)

    def _draw_node_recursive(self, node):
        if not node:
            return
        
        # Draw edges first (so they are behind nodes)
        if node.left:
            self.canvas.create_line(node.x, node.y, node.left.x, node.left.y, fill="#585b70", width=2)
            self._draw_node_recursive(node.left)
        if node.right:
            self.canvas.create_line(node.x, node.y, node.right.x, node.right.y, fill="#585b70", width=2)
            self._draw_node_recursive(node.right)

        # Draw Node
        r = 20
        node.canvas_id = self.canvas.create_oval(node.x-r, node.y-r, node.x+r, node.y+r, 
                                               fill="#313244", outline="#cdd6f4", width=2)
        node.text_id = self.canvas.create_text(node.x, node.y, text=str(node.value), 
                                              fill="#cdd6f4", font=("Helvetica", 10, "bold"))

    def highlight_node(self, node, color="#f9e2af"):
        self.canvas.itemconfig(node.canvas_id, fill=color, outline="#11111b")
        self.canvas.itemconfig(node.text_id, fill="#11111b")
        self.root.update()

    def reset_node_color(self, node):
        self.canvas.itemconfig(node.canvas_id, fill="#313244", outline="#cdd6f4")
        self.canvas.itemconfig(node.text_id, fill="#cdd6f4")
        self.root.update()

    def visit_node(self, node):
        self.canvas.itemconfig(node.canvas_id, fill="#a6e3a1", outline="#11111b")
        self.canvas.itemconfig(node.text_id, fill="#11111b")
        current_text = self.output_label.cget("text")
        self.output_label.config(text=current_text + str(node.value) + " ")
        self.root.update()

    def inorder_walk_anim(self, node):
        if not node or self.stop_animation:
            return

        # 1. Highlight Left
        self.highlight_node(node, "#89b4fa") # Blue for searching
        time.sleep(self.animation_speed)
        
        self.inorder_walk_anim(node.left)
        
        if self.stop_animation: return

        # 2. Visit Root
        self.highlight_node(node, "#f9e2af") # Yellow for current
        time.sleep(self.animation_speed)
        self.visit_node(node)
        time.sleep(self.animation_speed)

        # 3. Highlight Right
        self.inorder_walk_anim(node.right)

    def start_walk(self):
        if self.is_animating:
            return
        
        self.is_animating = True
        self.stop_animation = False
        self.btn_start.config(state=tk.DISABLED)
        self.output_label.config(text="Resultado: ")
        
        # Reset colors first
        self.draw_tree()
        
        def run():
            self.inorder_walk_anim(self.tree.root)
            self.is_animating = False
            self.btn_start.config(state=tk.NORMAL)

        threading.Thread(target=run, daemon=True).start()

    def reset_tree(self):
        self.stop_animation = True
        time.sleep(0.1) # Wait for thread to notice
        self.draw_tree()
        self.output_label.config(text="Resultado: ")
        self.btn_start.config(state=tk.NORMAL)
        self.is_animating = False

if __name__ == "__main__":
    root = tk.Tk()
    app = TreeVisualizer(root)
    root.mainloop()
