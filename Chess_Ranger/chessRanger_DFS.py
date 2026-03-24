import time
import tracemalloc
import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
SIZE = 8

PIECE_SYMBOLS = {
    "K": "♔",
    "Q": "♕",
    "R": "♖",
    "B": "♗",
    "N": "♘",
    "P": "♙"
}

# =========================
# MOVE RULES
# =========================
def di_ma(vt1, vt2):
    dh = abs(vt1[0] - vt2[0])
    dc = abs(vt1[1] - vt2[1])
    return (dh, dc) in [(1, 2), (2, 1)]

def di_vua(vt1, vt2):
    return max(abs(vt1[0] - vt2[0]), abs(vt1[1] - vt2[1])) == 1

def di_tot(vt1, vt2):
    dh = vt2[0] - vt1[0]
    dc = abs(vt2[1] - vt1[1])
    return dh == -1 and dc == 1

def di_xe(vt1, vt2, bc):
    if vt1[0] != vt2[0] and vt1[1] != vt2[1]:
        return False

    if vt1[0] == vt2[0]:
        buoc = 1 if vt2[1] > vt1[1] else -1
        for c in range(vt1[1] + buoc, vt2[1], buoc):
            if (vt1[0], c) in bc:
                return False
    else:
        buoc = 1 if vt2[0] > vt1[0] else -1
        for h in range(vt1[0] + buoc, vt2[0], buoc):
            if (h, vt1[1]) in bc:
                return False
    return True

def di_tuong(vt1, vt2, bc):
    if abs(vt1[0] - vt2[0]) != abs(vt1[1] - vt2[1]):
        return False

    b_hang = 1 if vt2[0] > vt1[0] else -1
    b_cot = 1 if vt2[1] > vt1[1] else -1

    h = vt1[0] + b_hang
    c = vt1[1] + b_cot

    while (h, c) != vt2:
        if (h, c) in bc:
            return False
        h += b_hang
        c += b_cot

    return True

def di_hau(vt1, vt2, bc):
    return di_xe(vt1, vt2, bc) or di_tuong(vt1, vt2, bc)

def an_duoc(quan, vt1, vt2, bc):
    if quan == "N": return di_ma(vt1, vt2)
    if quan == "K": return di_vua(vt1, vt2)
    if quan == "P": return di_tot(vt1, vt2)
    if quan == "R": return di_xe(vt1, vt2, bc)
    if quan == "B": return di_tuong(vt1, vt2, bc)
    if quan == "Q": return di_hau(vt1, vt2, bc)
    return False

# =========================
# GENERATE STATES
# =========================
def sinh_the(bc):
    ds_moi = []
    ds_quan = list(bc.items())

    for vt1, q1 in ds_quan:
        for vt2, q2 in ds_quan:
            if vt1 == vt2:
                continue

            if an_duoc(q1, vt1, vt2, bc):
                bc_moi = bc.copy()
                del bc_moi[vt1]
                del bc_moi[vt2]
                bc_moi[vt2] = q1
                ds_moi.append((vt1, vt2, bc_moi))

    return ds_moi

# =========================
# DFS
# =========================
def dfs(bc_goc):
    stack = [(bc_goc, [])]
    da_tham = set()
    so_node = 0

    while stack:
        bc_ht, duong = stack.pop()
        so_node += 1

        key = tuple(sorted(bc_ht.items()))
        if key in da_tham:
            continue
        da_tham.add(key)

        if len(bc_ht) == 1:
            return duong, bc_ht, so_node

        for vt1, vt2, bc_moi in sinh_the(bc_ht):
            duong_moi = duong + [(vt1, vt2)]
            stack.append((bc_moi, duong_moi))

    return None, None, so_node

# =========================
# DISPLAY
# =========================
def in_bc(ds_quan):
    bang = [["." for _ in range(8)] for _ in range(8)]

    for (h, c), quan in ds_quan.items():
        bang[h][c] = PIECE_SYMBOLS.get(quan, quan)

    print("  a b c d e f g h")

    for i in range(8):
        print(8 - i, end=" ")
        for j in range(8):
            print(bang[i][j], end=" ")
        print()
    print()





def to_chess_pos(row, col):
    return f"{chr(ord('a') + col)}{8 - row}"

# =========================
# REPLAY SOLUTION
# =========================

# Hàm in ra toàn bộ không có animation
# def chieu_lai(bc_goc, kq):
#     bc_ht = bc_goc.copy()

#     print("\nInitial board:\n")
#     in_bc(bc_ht)

#     for i, (vt1, vt2) in enumerate(kq):
#         quan = bc_ht[vt1]

#         del bc_ht[vt1]
#         del bc_ht[vt2]
#         bc_ht[vt2] = quan

#         print(
#             f"Step {i+1}: {PIECE_SYMBOLS.get(quan, quan)} "
#             f"{to_chess_pos(vt1[0], vt1[1])} "
#             f"captures {to_chess_pos(vt2[0], vt2[1])}"
#         )

#         in_bc(bc_ht)



def chieu_lai(bc_goc, kq, delay=0.7):
    bc_ht = bc_goc.copy()

    clear_screen()
    print("Initial board:\n")
    in_bc(bc_ht)
    time.sleep(0.5)

    for i, (vt1, vt2) in enumerate(kq):
        quan = bc_ht[vt1]

        del bc_ht[vt1]
        del bc_ht[vt2]
        bc_ht[vt2] = quan

        clear_screen()

        print(
            f"Step {i+1}: {PIECE_SYMBOLS.get(quan, quan)} "
            f"{to_chess_pos(vt1[0], vt1[1])} "
            f"captures {to_chess_pos(vt2[0], vt2[1])}\n"
        )

        in_bc(bc_ht)

        time.sleep(delay)
# =========================
# SOLVER ENTRY
# =========================
def giai(bc_dau):
    tracemalloc.start()
    t1 = time.perf_counter()

    kq, bc_cuoi, so_node = dfs(bc_dau)

    t2 = time.perf_counter()
    ram = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    if kq:
        chieu_lai(bc_dau, kq)
        print("Final piece:", {
            to_chess_pos(r, c): PIECE_SYMBOLS.get(q, q)
            for (r, c), q in bc_cuoi.items()
        })
    else:
        print("No solution found")

    print(f"\nNode mở rộng: {so_node}")
    print(f"Thời gian: {round(t2 - t1, 6)} seconds")
    print(f"Memory: {round(ram / 1024, 2)} KB")