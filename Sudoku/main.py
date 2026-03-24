import random
import copy
import colorama
from colorama import Fore, Style
from solver_dfs import run_dfs
from solver_heuristic import run_heuristic

# Khởi tạo colorama
colorama.init(autoreset=True)

# =========================
# PRINT BOARD
# =========================
def print_board(board, original_board=None):
    for r in range(9):
        if r % 3 == 0 and r != 0:
            print("-" * 21)
        for c in range(9):
            if c % 3 == 0 and c != 0:
                print("|", end=" ")
            
            val = board[r][c]
            # Nếu có bảng gốc, ô ban đầu trống (0) và ô hiện tại có số -> Đây là số mới điền
            if original_board and original_board[r][c] == 0 and val != 0:
                print(f"{Fore.GREEN}{val}{Style.RESET_ALL}", end=" ")
            elif val == 0:
                print(".", end=" ") # In dấu chấm cho ô trống nhìn cho thoáng
            else:
                print(val, end=" ")
        print()


# =========================
# LOAD ALL BOARDS FROM FILE
# =========================
def load_all_boards(filename):
    data = {}
    exec(open(filename).read(), data)

    boards = {}
    for k, v in data.items():
        if isinstance(v, list) and len(v) == 9:
            boards[k] = v

    return boards


# =========================
# GENERATE FULL BOARD
# =========================
def generate_full_board():
    board = [[0]*9 for _ in range(9)]

    def is_valid(b, r, c, v):
        for i in range(9):
            if b[r][i] == v or b[i][c] == v:
                return False
        sr, sc = 3*(r//3), 3*(c//3)
        for i in range(sr, sr+3):
            for j in range(sc, sc+3):
                if b[i][j] == v:
                    return False
        return True

    def fill():
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    nums = list(range(1,10))
                    random.shuffle(nums)
                    for v in nums:
                        if is_valid(board, r, c, v):
                            board[r][c] = v
                            if fill():
                                return True
                            board[r][c] = 0
                    return False
        return True

    fill()
    return board


def count_solutions(board, limit=2):
    count = 0

    def dfs():
        nonlocal count
        if count >= limit:
            return

        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    for v in range(1,10):
                        if valid(board, r, c, v):
                            board[r][c] = v
                            dfs()
                            board[r][c] = 0
                    return
        count += 1

    def valid(b, r, c, v):
        for i in range(9):
            if b[r][i] == v or b[i][c] == v:
                return False
        sr, sc = 3*(r//3), 3*(c//3)
        for i in range(sr, sr+3):
            for j in range(sc, sc+3):
                if b[i][j] == v:
                    return False
        return True

    dfs()
    return count


def generate_sudoku(level):
    clues = {
        "easy": 50,
        "intermediate": 35,
        "advanced": 27,
        "evil": 20
    }

    board = generate_full_board()
    cells = [(r,c) for r in range(9) for c in range(9)]
    random.shuffle(cells)

    remove_count = 81 - clues[level]

    for r,c in cells:
        if remove_count <= 0:
            break

        temp = board[r][c]
        board[r][c] = 0

        copy_board = copy.deepcopy(board)
        if count_solutions(copy_board) != 1:
            board[r][c] = temp
        else:
            remove_count -= 1

    return board


# =========================
# MAIN
# =========================
def main():
    print("Chọn input:")
    print("1. Tạo Sudoku (chuẩn)")
    print("2. Nhập từ file")

    choice = input(">> ")

    # =========================
    # CASE 1: GENERATE
    # =========================
    if choice == "1":
        level = input("Chọn độ khó (easy/intermediate/advanced/evil): ")
        board = generate_sudoku(level)

        print("\n--- INPUT ---")
        print_board(board)

        run_solver(board)

    # =========================
    # CASE 2: LOAD FILE
    # =========================
    else:
        filename = input("Nhập tên file: ")
        boards = load_all_boards(filename)

        print("\nDanh sách board:")
        for name in sorted(boards):
            print("-", name)

        mode = input("\nChạy 1 board hay tất cả? (1/all): ")

        if mode == "1":
            key = input("Nhập tên board: ")
            board = boards[key]

            print("\n--- INPUT ---")
            print_board(board)

            run_solver(board)

        else:

            print("\nChọn giải thuật:")
            print("1. DFS")
            print("2. Heuristic")
            algo = input(">> ")

            print("Chế độ hiển thị:")
            print("1. In tất cả bước")
            print("2. Animation")
            print("3. Không in")

            mode = input(">> ")

            visual = (mode != "3")
            animate = (mode == "2")

            for name, board in sorted(boards.items()):
                print(f"\n====================")
                print(f"BOARD: {name}")
                print(f"====================")

                print("\n--- INPUT ---")
                print_board(board)

                # ĐÃ SỬA: Truyền đủ tham số animate
                run_solver_fixed(board, algo, visual, animate)


# =========================
# SOLVER WRAPPER
# =========================
def run_solver(board):
    print("\nChọn giải thuật:")
    print("1. DFS")
    print("2. Heuristic")

    algo = input(">> ")
    print("Chế độ hiển thị:")
    print("1. In tất cả bước")
    print("2. Animation")
    print("3. Không in")

    mode = input(">> ")

    visual = (mode != "3")
    animate = (mode == "2")
    
    # Lưu lại bảng gốc để tô màu số mới giải
    original_board = copy.deepcopy(board)

    if algo == "1":
        result, t, mem, nodes = run_dfs(board, visualize=visual, animate=animate) 
        name = "DFS"
    else:
        result, t, mem, nodes = run_heuristic(board, visualize=visual, animate=animate)
        name = "Heuristic"

    print(f"\n--- SOLUTION ({name}) ---")
    print_board(result, original_board)

    if not visual:
        print(f"\nTime: {t:.6f}s")
        print(f"Memory: {mem:.2f} KB")
        print(f"Nodes: {nodes}")

def run_solver_fixed(board, algo, visual, animate):
    # Lưu lại bảng gốc để tô màu số mới giải
    original_board = copy.deepcopy(board)
    
    if algo == "1":
        result, t, mem, nodes = run_dfs(board, visualize=visual, animate=animate)
        name = "DFS"
    else:
        result, t, mem, nodes = run_heuristic(board, visualize=visual, animate=animate)
        name = "Heuristic"

    print(f"\n--- SOLUTION ({name}) ---")
    print_board(result, original_board)

    if not visual:
        print(f"\nTime: {t:.6f}s")
        print(f"Memory: {mem:.2f} KB")
        print(f"Nodes: {nodes}")


if __name__ == "__main__":
    main()
