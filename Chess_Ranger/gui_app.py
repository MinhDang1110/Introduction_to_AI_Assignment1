import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import os
import copy
from gui_theme import THEME
from gui_board import ChessBoard
import chessRanger_DFS as dfs_logic
import chessRanger_Heuristic as astar_logic
import input_parser

class ModernButton(tk.Button):
    def __init__(self, master, **kwargs):
        kwargs.setdefault("relief", "flat")
        kwargs.setdefault("font", THEME["font_bold"])
        kwargs.setdefault("fg", "#1C1E21")
        kwargs.setdefault("cursor", "hand2")
        kwargs.setdefault("pady", 10)
        super().__init__(master, **kwargs)
        self.default_bg = kwargs.get("bg", THEME["btn_secondary"])
        self.bind("<Enter>", lambda e: self.config(bg="#D8DADE" if self.default_bg == THEME["btn_secondary"] else "#27AE60"))
        self.bind("<Leave>", lambda e: self.config(bg=self.default_bg))

class ChessRangerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chess Ranger Pro - Light Studio")
        self.geometry("1200x850")
        self.configure(bg=THEME["bg_main"])
        
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.join(self.base_dir, "assets")
        self.current_board, self.solution_path, self.current_step, self.history_states = {}, [], 0, []
        self.ghost_window = None

        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # LEFT PANEL
        self.left_panel = tk.Frame(self, bg=THEME["bg_panel"], padx=15, pady=20, highlightbackground="#DCDFE3", highlightthickness=1)
        self.left_panel.grid(row=0, column=0, sticky="nsew")
        tk.Label(self.left_panel, text="KHO QUÂN CỜ", bg=THEME["bg_panel"], fg=THEME["text_secondary"], font=THEME["font_bold"]).pack(pady=(0, 20))
        
        self.piece_icons = {}
        for p in ["K", "Q", "R", "B", "N", "P"]:
            path = os.path.join(self.assets_dir, f"{p}.png")
            if os.path.exists(path):
                img = Image.open(path).resize((50, 50), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                lbl = tk.Label(self.left_panel, image=photo, bg=THEME["bg_panel"], cursor="fleur")
                lbl.image = photo
                lbl.pack(pady=8)
                lbl.bind("<ButtonPress-1>", lambda e, pt=p: self.start_external_drag(e, pt))
                lbl.bind("<B1-Motion>", self.do_external_drag)
                lbl.bind("<ButtonRelease-1>", self.stop_external_drag)
                self.piece_icons[p] = lbl

        self.trash_label = tk.Label(self.left_panel, text="🗑 KÉO VÀO ĐÂY ĐỂ XÓA", bg="#FEEFF0", fg=THEME["btn_danger"], font=THEME["font_bold"], pady=20)
        self.trash_label.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # CENTER PANEL
        self.center_panel = tk.Frame(self, bg=THEME["bg_main"])
        self.center_panel.grid(row=0, column=1, sticky="nsew")
        self.status_label = tk.Label(self.center_panel, text="SẴN SÀNG GIẢI ĐỐ", bg=THEME["bg_main"], fg="#2C3E50", font=THEME["font_title"])
        self.status_label.pack(pady=(20, 5))
        self.step_label = tk.Label(self.center_panel, text="Quân trên bàn: 0", bg=THEME["bg_main"], fg=THEME["text_secondary"], font=THEME["font_main"])
        self.step_label.pack(pady=(0, 10))
        self.board_ui = ChessBoard(self.center_panel); self.board_ui.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.board_ui.on_move_callback = self.handle_manual_move

        # RIGHT PANEL
        self.right_panel = tk.Frame(self, bg=THEME["bg_panel"], padx=20, pady=30, highlightbackground="#DCDFE3", highlightthickness=1)
        self.right_panel.grid(row=0, column=2, sticky="nsew")
        tk.Label(self.right_panel, text="ĐIỀU KHIỂN", bg=THEME["bg_panel"], fg=THEME["text_secondary"], font=THEME["font_bold"]).pack(pady=(0, 20))
        self.btn_load = ModernButton(self.right_panel, text="📁 Nhập từ File", command=self.load_file); self.btn_load.pack(fill=tk.X, pady=5)
        tk.Frame(self.right_panel, height=1, bg="#DCDFE3").pack(fill=tk.X, pady=20)
        ModernButton(self.right_panel, text="Giải bằng DFS", command=lambda: self.solve("DFS")).pack(fill=tk.X, pady=5)
        ModernButton(self.right_panel, text="Giải bằng A*", command=lambda: self.solve("ASTAR")).pack(fill=tk.X, pady=5)
        self.btn_solve_auto = ModernButton(self.right_panel, text="GIẢI TỰ ĐỘNG", bg=THEME["btn_primary"], fg="white", command=self.auto_solve); self.btn_solve_auto.pack(fill=tk.X, pady=(20, 5))
        nav_frame = tk.Frame(self.right_panel, bg=THEME["bg_panel"]); nav_frame.pack(fill=tk.X, pady=10)
        self.btn_back = ModernButton(nav_frame, text="◁ LÙI", width=8, command=self.prev_step, state=tk.DISABLED); self.btn_back.pack(side=tk.LEFT, expand=True, padx=2)
        self.btn_next = ModernButton(nav_frame, text="TIẾP ▷", width=8, command=self.next_step, state=tk.DISABLED); self.btn_next.pack(side=tk.LEFT, expand=True, padx=2)
        ModernButton(self.right_panel, text="LÀM MỚI BÀN CỜ", bg=THEME["btn_danger"], fg="white", command=self.clear_board).pack(side=tk.BOTTOM, fill=tk.X)

    def update_step_display(self):
        total = len(self.solution_path)
        self.step_label.config(text=f"Tiến trình: Bước {self.current_step} / {total}" if total > 0 else f"Quân trên bàn: {len(self.current_board)}")

    def handle_manual_move(self, r1, c1, r2, c2, x_root, y_root):
        tx, ty, tw, th = self.trash_label.winfo_rootx(), self.trash_label.winfo_rooty(), self.trash_label.winfo_width(), self.trash_label.winfo_height()
        if tx <= x_root <= tx + tw and ty <= y_root <= ty + th:
            if (r1, c1) in self.current_board: del self.current_board[(r1, c1)]; self.board_ui.update_board(self.current_board); self.update_step_display(); return True
        if astar_logic.valid_capture(self.current_board.get((r1, c1)), (r1, c1), (r2, c2), self.current_board):
            piece = self.current_board.pop((r1, c1)); self.current_board[(r2, c2)] = piece; self.history_states.append(self.current_board.copy()); self.board_ui.update_board(self.current_board); self.btn_load.config(state=tk.DISABLED); return True
        return False

    def start_external_drag(self, event, p_type):
        self.dragged_type = p_type; self.ghost_window = tk.Toplevel(self); self.ghost_window.overrideredirect(True); self.ghost_window.attributes("-topmost", True); self.ghost_window.config(bg="white")
        tk.Label(self.ghost_window, image=self.piece_icons[p_type].image, bg="white").pack(); self.do_external_drag(event)

    def do_external_drag(self, event):
        if self.ghost_window: self.ghost_window.geometry(f"+{event.x_root-25}+{event.y_root-25}")

    def stop_external_drag(self, event):
        if not self.ghost_window: return
        bx, by = event.x_root - self.board_ui.winfo_rootx(), event.y_root - self.board_ui.winfo_rooty()
        offset = 20
        if 0 <= bx - offset < self.board_ui.sq_size * 8 and 0 <= by - offset < self.board_ui.sq_size * 8:
            r, c = (by - offset) // self.board_ui.sq_size, (bx - offset) // self.board_ui.sq_size
            if (r, c) not in self.current_board: self.current_board[(r, c)] = self.dragged_type; self.board_ui.update_board(self.current_board); self.history_states = [self.current_board.copy()]; self.btn_load.config(state=tk.DISABLED)
        self.ghost_window.destroy(); self.ghost_window = None; self.update_step_display()

    def solve(self, algo):
        if len(self.current_board) < 2: return
        self.status_label.config(text="ĐANG TÍNH TOÁN...", fg="#E67E22"); self.update()
        path = dfs_logic.dfs(self.current_board)[0] if algo == "DFS" else [(p[0], p[1]) for p in astar_logic.astar(self.current_board)[0]] if astar_logic.astar(self.current_board)[0] else None
        if path: self.solution_path, self.current_step = path, 0; self.status_label.config(text="ĐÃ CÓ LỜI GIẢI!", fg="#27AE60"); self.update_step_display(); self.update_buttons()
        else: self.status_label.config(text="VÔ NGHIỆM", fg=THEME["btn_danger"]); messagebox.showwarning("Thông báo", "Không tìm thấy cách giải!")

    def next_step(self):
        if self.current_step < len(self.solution_path):
            start, end = self.solution_path[self.current_step]
            def done(): piece = self.current_board.pop(start); self.current_board[end] = piece; self.history_states.append(self.current_board.copy()); self.current_step += 1; self.board_ui.update_board(self.current_board); self.update_step_display(); self.update_buttons()
            self.board_ui.animate_move(start, end, done)

    def prev_step(self):
        if len(self.history_states) > 1: self.history_states.pop(); self.current_board = self.history_states[-1].copy(); self.current_step -= 1; self.board_ui.update_board(self.current_board); self.update_step_display(); self.update_buttons()

    def auto_solve(self):
        if self.current_step < len(self.solution_path): self.next_step(); self.after(800, self.auto_solve)

    def update_buttons(self):
        self.btn_next.config(state=tk.NORMAL if self.current_step < len(self.solution_path) else tk.DISABLED); self.btn_back.config(state=tk.NORMAL if len(self.history_states) > 1 else tk.DISABLED)

    def load_file(self):
        f = simpledialog.askstring("Mở file", "Tên file:")
        if f:
            try: self.current_board = input_parser.load_board_from_file(f); self.history_states = [self.current_board.copy()]; self.solution_path, self.current_step = [], 0; self.board_ui.update_board(self.current_board); self.update_step_display(); self.status_label.config(text="ĐÃ TẢI DỮ LIỆU", fg="#2980B9")
            except: messagebox.showerror("Lỗi", "Không tìm thấy file!")

    def clear_board(self):
        self.current_board, self.history_states, self.solution_path, self.current_step = {}, [], [], 0; self.board_ui.update_board({}); self.status_label.config(text="SẴN SÀNG GIẢI ĐỐ", fg="#2C3E50"); self.update_step_display(); self.btn_load.config(state=tk.NORMAL); self.update_buttons()

if __name__ == "__main__":
    app = ChessRangerApp(); app.mainloop()