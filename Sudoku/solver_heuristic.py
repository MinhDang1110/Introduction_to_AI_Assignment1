import time
import tracemalloc
import copy

NODE_COUNT = 0
VISUALIZE = False
STEP = 0


# Print Board 
def print_board(board):
    for r in range(9):
        if r % 3 == 0 and r != 0:
            print("-"*21)
        for c in range(9):
            if c % 3 == 0 and c != 0:
                print("|", end=" ")
            print(board[r][c], end=" ")
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

def init_domains(board):
    domains = {}
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                possible = set(range(1, 10))
                for (nr, nc) in NEIGHBORS[(r, c)]:
                    possible.discard(board[nr][nc])
                domains[(r, c)] = possible
    return domains

def select_mrv(domains):
    return min(domains.items(), key=lambda x: len(x[1]))

def lcv_order(var, domains):
    def impact(val): # hàm con để tính toán "độ sát thương" (impact) nếu ta quyết định điền con số val vào ô var.
        return sum(1 for nb in NEIGHBORS[var] #duyệt qua tất cả các ô hàng xóm (nb) của ô hiện tại.
                   if nb in domains and val in domains[nb]) #Chỉ xét những hàng xóm đang là ô trống (chưa được điền).
    return sorted(domains[var], key=impact)
# Cuối cùng, hàm trả về danh sách các con số có thể điền cho ô var, nhưng đã được sắp xếp tăng dần dựa theo độ impact. 
# Số nào có impact nhỏ nhất (ít làm hại hàng xóm nhất) sẽ nằm ở đầu danh sách (vị trí index 0)
# để vòng lặp for trong hàm solve lấy ra thử đầu tiên.

# Forward Checking
def forward_check(var, val, domains, removed):
    for nb in NEIGHBORS[var]: # Duyệt qua tất cả 20 ô hàng xóm (cùng hàng, cột, khối 3x3) của ô var vừa được điền số val
        
        if nb in domains and val in domains[nb]: # Nếu láng giềng nb vẫn là ô trống và xui xẻo thay,trong danh sách các số nó đang định điền lại chứa đúng con số val mà ta vừa chốt.
            domains[nb].remove(val)
            removed.append((nb, val))
            if not domains[nb]: #
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


        # Code để in ra các bước giải
        if VISUALIZE:
            print(f"\n--- STEP {STEP}: Fill (r={r}, c={c}) = {val} ---")
            print_board(board)

        removed = []
        saved = domains.pop(var)

        if forward_check(var, val, domains, removed):
            if solve(board, domains):
                return True

        domains[var] = saved
        undo(domains, removed)
        board[r][c] = 0
    return False

def run_heuristic(board, visualize=False):
    global NODE_COUNT, VISUALIZE, STEP

    NODE_COUNT = 0
    STEP = 0
    VISUALIZE = visualize

    b = copy.deepcopy(board)
    domains = init_domains(b)

    # ❗ nếu visualize → không đo performance
    if VISUALIZE:
        solve(b, domains)
        return b, None, None, NODE_COUNT

    tracemalloc.start()
    start = time.perf_counter()

    solve(b, domains)

    end = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return b, end-start, peak/1024, NODE_COUNT