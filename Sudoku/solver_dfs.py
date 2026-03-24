import time
import tracemalloc
import copy
import os

def print_board(board):
    for r in range(9):
        if r % 3 == 0 and r != 0:
            print("-" * 21)
        for c in range(9):
            if c % 3 == 0 and c != 0:
                print("|", end=" ")
            val = board[r][c]
            if val == 0:
                print(".", end=" ")
            else:
                print(val, end=" ")
        print()

class SudokuSolverDFS:
    def __init__(self, board, visual=False, animate=False):
        self.board = board
        self.visual = visual
        self.animate = animate
        self.nodes = 0

    def is_valid(self, r, c, v):
        for i in range(9):
            if self.board[r][i] == v or self.board[i][c] == v:
                return False

        sr, sc = 3*(r//3), 3*(c//3)
        for i in range(sr, sr+3):
            for j in range(sc, sc+3):
                if self.board[i][j] == v:
                    return False
        return True

    # CẢI TIẾN: Kiểm tra bảng đề bài có hợp lệ ngay từ đầu không
    def check_initial_valid(self):
        for r in range(9):
            for c in range(9):
                v = self.board[r][c]
                if v != 0:
                    # Tạm xóa số hiện tại để dùng lại hàm is_valid
                    self.board[r][c] = 0
                    is_val = self.is_valid(r, c, v)
                    self.board[r][c] = v # Trả lại giá trị cũ
                    if not is_val:
                        return False
        return True

    def find_empty(self):
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    return r, c
        return None

    def solve(self):
        empty = self.find_empty()
        if not empty:
            return True

        r, c = empty

        for v in range(1, 10):
            self.nodes += 1
            if self.is_valid(r, c, v):
                self.board[r][c] = v
                
                # --- VISUALIZATION / ANIMATION ---
                if self.visual:
                    if self.animate:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        
                    print(f"\n--- DFS STEP {self.nodes}: Fill (r={r}, c={c}) = {v} ---")
                    print_board(self.board)
                    
                    if self.animate:
                        time.sleep(0.2)
                # ---------------------------------

                if self.solve():
                    return True
                self.board[r][c] = 0

        return False


def run_dfs(board, visualize=False, animate=False):
    b = copy.deepcopy(board)

    tracemalloc.start()
    start = time.perf_counter()

    solver = SudokuSolverDFS(b, visual=visualize, animate=animate)
    
    # CẢI TIẾN: Bắt vô nghiệm ngay từ đề bài hoặc sau khi duyệt
    success = False
    if solver.check_initial_valid():
        success = solver.solve()

    end = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if not success:
        print("\n[!]BẢNG SUDOKU VÔ NGHIỆM (Vi phạm ràng buộc hoặc không thể giải)!")

    return b, end-start, peak/1024, solver.nodes
