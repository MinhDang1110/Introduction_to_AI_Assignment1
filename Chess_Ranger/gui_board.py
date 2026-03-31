import tkinter as tk
from PIL import Image, ImageTk
import os
from gui_theme import THEME

class ChessBoard(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=THEME["bg_main"], highlightthickness=0, **kwargs)
        self.sq_size = 60
        self.images = {}
        self.pieces_on_board = {}
        self.current_logic_board = {}
        
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.join(self.base_dir, "assets")
        
        self.load_assets()
        self.bind("<Configure>", self.on_resize)
        
        self._drag_data = {"item": None, "x": 0, "y": 0, "start_pos": None}
        self.tag_bind("piece", "<ButtonPress-1>", self.on_start_drag)
        self.tag_bind("piece", "<B1-Motion>", self.on_drag)
        self.tag_bind("piece", "<ButtonRelease-1>", self.on_stop_drag)

    def load_assets(self):
        for p in ["K", "Q", "R", "B", "N", "P"]:
            path = os.path.join(self.assets_dir, f"{p}.png")
            if os.path.exists(path):
                self.images[p] = Image.open(path)

    def on_resize(self, event):
        side = min(event.width, event.height) - 40
        if side > 100:
            self.sq_size = side // 8
            self.draw_board_grid()
            if self.current_logic_board:
                self.update_board(self.current_logic_board)

    def draw_board_grid(self):
        self.delete("grid")
        offset = 20
        total_size = self.sq_size * 8
        # Vẽ viền cho bàn cờ
        self.create_rectangle(offset-2, offset-2, offset+total_size+2, offset+total_size+2, outline="#BDC3C7", width=2, tags="grid")
        
        for r in range(8):
            for c in range(8):
                color = THEME["board_light"] if (r + c) % 2 == 0 else THEME["board_dark"]
                x1, y1 = c * self.sq_size + offset, r * self.sq_size + offset
                x2, y2 = x1 + self.sq_size, y1 + self.sq_size
                self.create_rectangle(x1, y1, x2, y2, fill=color, outline="", tags="grid")

    def update_board(self, board_dict):
        self.current_logic_board = board_dict.copy()
        self.delete("piece")
        self.pieces_on_board.clear()
        offset = 20
        for (r, c), p_type in board_dict.items():
            x = c * self.sq_size + self.sq_size // 2 + offset
            y = r * self.sq_size + self.sq_size // 2 + offset
            if p_type in self.images:
                img = self.images[p_type].resize((int(self.sq_size*0.85), int(self.sq_size*0.85)), Image.LANCZOS)
                tk_img = ImageTk.PhotoImage(img)
                if not hasattr(self, '_tk_imgs'): self._tk_imgs = {}
                self._tk_imgs[f"{r}_{c}"] = tk_img
                item = self.create_image(x, y, image=tk_img, tags=("piece", p_type))
                self.pieces_on_board[(r, c)] = item
            else:
                item = self.create_text(x, y, text=p_type, font=("Arial", 22, "bold"), fill="#2C3E50", tags=("piece", p_type))
                self.pieces_on_board[(r, c)] = item

    def on_start_drag(self, event):
        item = self.find_closest(event.x, event.y)[0]
        if "piece" in self.gettags(item):
            offset = 20
            r, c = (event.y - offset) // self.sq_size, (event.x - offset) // self.sq_size
            self._drag_data.update({"item": item, "x": event.x, "y": event.y, "start_pos": (r, c)})
            self.tag_raise(item)

    def on_drag(self, event):
        if self._drag_data["item"]:
            dx, dy = event.x - self._drag_data["x"], event.y - self._drag_data["y"]
            self.move(self._drag_data["item"], dx, dy)
            self._drag_data.update({"x": event.x, "y": event.y})

    def on_stop_drag(self, event):
        item = self._drag_data["item"]
        if not item: return
        offset = 20
        old_r, old_c = self._drag_data["start_pos"]
        new_r, new_c = (event.y - offset) // self.sq_size, (event.x - offset) // self.sq_size
        if hasattr(self, 'on_move_callback'):
            if not self.on_move_callback(old_r, old_c, new_r, new_c, event.x_root, event.y_root):
                self.coords(item, old_c * self.sq_size + self.sq_size // 2 + offset, old_r * self.sq_size + self.sq_size // 2 + offset)
        self._drag_data["item"] = None

    def animate_move(self, start, end, callback):
        r1, c1 = start
        r2, c2 = end
        item = self.pieces_on_board.get((r1, c1))
        if not item: 
            callback()
            return
        offset = 20
        tx, ty = c2*self.sq_size + self.sq_size//2 + offset, r2*self.sq_size + self.sq_size//2 + offset
        curr = self.coords(item)
        steps = 12
        dx, dy = (tx - curr[0])/steps, (ty - curr[1])/steps
        def step(i):
            if i < steps:
                self.move(item, dx, dy); self.after(15, lambda: step(i+1))
            else:
                self.coords(item, tx, ty); callback()
        step(0)