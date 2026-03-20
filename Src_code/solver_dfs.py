import time
import tracemalloc
import copy

class SudokuSolverDFS:
    def __init__(self, board, visual=False):
        self.board = board
        self.visual = visual
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
                if self.solve():
                    return True
                self.board[r][c] = 0

        return False


def run_dfs(board):
    b = copy.deepcopy(board)

    tracemalloc.start()
    start = time.perf_counter()

    solver = SudokuSolverDFS(b)
    solver.solve()

    end = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return b, end-start, peak/1024, solver.nodes