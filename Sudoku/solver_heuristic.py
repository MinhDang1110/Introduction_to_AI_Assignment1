import time
import tracemalloc
import copy
import os

NODE_COUNT = 0
STEP = 0
VISUALIZE = False
ANIMATE = False

# Print Board 
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

# get_neighbors
def get_neighbors():
    neighbors = {}
    for r in range(9):
        for c in range(9):
            nbs = set()
            for i in range(9):
                nbs.add((r, i))
                nbs.add((i, c))
            sr, sc = 3*(r//3), 3*(c//3)
            for i in range(sr, sr+3):
                for j in range(sc, sc+3):
                    nbs.add((i, j))
            nbs.remove((r, c))
            neighbors[(r, c)] = nbs
    return neighbors

NEIGHBORS = get_neighbors()

# CẢI TIẾN 1: Kiểm tra tính hợp lệ của đề bài ban đầu
def is_initial_valid(board):
    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val != 0:
                for (nr, nc) in NEIGHBORS[(r, c)]:
                    if board[nr][nc] == val:
                        return False
    return True

# CẢI TIẾN 2: Phát hiện sớm ô trống không thể điền số nào
def init_domains(board):
    domains = {}
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                possible = set(range(1, 10))
                for (nr, nc) in NEIGHBORS[(r, c)]:
                    possible.discard(board[nr][nc])
                
                # Nếu có ô trống mà tập domain bằng rỗng -> Chắc chắn vô nghiệm
                if len(possible) == 0:
                    return None 
                
                domains[(r, c)] = possible
    return domains

def select_mrv(domains):
    return min(domains.items(), key=lambda x: len(x[1]))

def lcv_order(var, domains):
    def impact(val):
        return sum(1 for nb in NEIGHBORS[var] 
                   if nb in domains and val in domains[nb])
    return sorted(domains[var], key=impact)


# Forward Checking
def forward_check(var, val, domains, removed):
    for nb in NEIGHBORS[var]:
        if nb in domains and val in domains[nb]:
            domains[nb].remove(val)
            removed.append((nb, val))
            if not domains[nb]:
                return False
    return True

# Undo
def undo(domains, removed):
    for var, val in removed:
        domains[var].add(val)

# Solve
def solve(board, domains):
    global NODE_COUNT, STEP

    if not domains:  
        return True

    var, _ = select_mrv(domains)
    r, c = var

    for val in lcv_order(var, domains):

        NODE_COUNT += 1
        board[r][c] = val
        STEP += 1

        # --- VISUALIZATION / ANIMATION ---
        if VISUALIZE:
            if ANIMATE:
                os.system('cls' if os.name == 'nt' else 'clear')

            print(f"\n--- STEP {STEP}: Fill (r={r}, c={c}) = {val} ---")
            print_board(board)
            
            if ANIMATE:
                time.sleep(0.2)
        # ---------------------------------

        removed = []
        saved = domains.pop(var)

        if forward_check(var, val, domains, removed):
            if solve(board, domains):
                return True

        domains[var] = saved
        undo(domains, removed)
        board[r][c] = 0
    return False

def run_heuristic(board, visualize=False, animate=False):
    global NODE_COUNT, VISUALIZE, STEP, ANIMATE

    NODE_COUNT = 0
    STEP = 0
    VISUALIZE = visualize
    ANIMATE = animate

    b = copy.deepcopy(board)
    
    tracemalloc.start()
    start = time.perf_counter()

    success = False
    
    # CẢI TIẾN: Chỉ bắt đầu giải nếu đề bài hợp lệ và có thể khởi tạo tập giá trị
    if is_initial_valid(b):
        domains = init_domains(b)
        if domains is not None:
            success = solve(b, domains)

    end = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if not success:
        print("\n[!]BẢNG SUDOKU VÔ NGHIỆM (Vi phạm ràng buộc hoặc không thể giải)!")

    return b, end-start, peak/1024, NODE_COUNT
