import heapq
import time
import tracemalloc
import os



def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
BOARD_SIZE = 8

heur_cache = {}
PIECE_SYMBOLS = {
    "K": "♔",
    "Q": "♕",
    "R": "♖",
    "B": "♗",
    "N": "♘",
    "P": "♙"
}
# Movement rules

def knight_move(a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return (dx, dy) in [(1, 2), (2, 1)]

def king_move(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1])) == 1

def pawn_move(a, b):
    dr = b[0] - a[0]
    dc = abs(b[1] - a[1])
    return dr == -1 and dc == 1

def rook_move(a, b, board):

    if a[0] != b[0] and a[1] != b[1]:
        return False

    if a[0] == b[0]:
        step = 1 if b[1] > a[1] else -1
        for c in range(a[1] + step, b[1], step):
            if (a[0], c) in board:
                return False
    else:
        step = 1 if b[0] > a[0] else -1
        for r in range(a[0] + step, b[0], step):
            if (r, a[1]) in board:
                return False

    return True

def bishop_move(a, b, board):

    if abs(a[0] - b[0]) != abs(a[1] - b[1]):
        return False

    step_r = 1 if b[0] > a[0] else -1
    step_c = 1 if b[1] > a[1] else -1

    r = a[0] + step_r
    c = a[1] + step_c

    while (r, c) != b:

        if (r, c) in board:
            return False

        r += step_r
        c += step_c

    return True

def queen_move(a, b, board):
    return rook_move(a, b, board) or bishop_move(a, b, board)


# Capture rule

def valid_capture(piece, a, b, board):

    if piece == "N":
        return knight_move(a, b)

    if piece == "K":
        return king_move(a, b)

    if piece == "P":
        return pawn_move(a, b)

    if piece == "R":
        if a[0] != b[0] and a[1] != b[1]:
            return False
        return rook_move(a, b, board)

    if piece == "B":
        if abs(a[0] - b[0]) != abs(a[1] - b[1]):
            return False
        return bishop_move(a, b, board)

    if piece == "Q":
        return queen_move(a, b, board)

    return False


# Check if board has capture

def has_capture(board):

    pieces = list(board.items())

    for posA, typeA in pieces:
        for posB, typeB in pieces:

            if posA == posB:
                continue

            if valid_capture(typeA, posA, posB, board):
                return True

    return False


# Heuristic

def heuristic(board):

    key = frozenset(board.items())
    if key in heur_cache:
        return heur_cache[key]

    pieces = list(board.items())
    n = len(pieces)

    if n <= 1:
        return 0

    # Build capture graph

    graph = {i: set() for i in range(n)}

    for i, (posA, typeA) in enumerate(pieces):
        for j, (posB, typeB) in enumerate(pieces):

            if i == j:
                continue

            if valid_capture(typeA, posA, posB, board):
                graph[i].add(j)
                graph[j].add(i)

    # Count components

    visited = set()
    components = 0

    for i in range(n):

        if i in visited:
            continue

        components += 1

        stack = [i]

        while stack:

            node = stack.pop()

            if node in visited:
                continue

            visited.add(node)

            for nei in graph[node]:
                stack.append(nei)

     # Distance

    dist = 0

    for i in range(n):
        for j in range(i + 1, n):

            a = pieces[i][0]
            b = pieces[j][0]

            dist += abs(a[0] - b[0]) + abs(a[1] - b[1])

    dist = dist / (n*(n-1)/2)

    # Final heuristic

    h = components*5 + dist*3

    heur_cache[key] = max(h, 0)

    return heur_cache[key]


# Successor generation

priority = {
    "Q":0,
    "R":1,
    "B":2,
    "N":3,
    "K":4,
    "P":5
}

def generate_successors(board):

    states = []
    pieces = list(board.items())

    for posA, typeA in pieces:

        for posB, typeB in pieces:

            if posA == posB:
                continue

            if valid_capture(typeA, posA, posB, board):

                new_board = board.copy()

                del new_board[posA]
                del new_board[posB]

                new_board[posB] = typeA

                future = 0

                for p1, t1 in new_board.items():
                    for p2, t2 in new_board.items():

                        if p1 == p2:
                            continue

                        if valid_capture(t1, p1, p2, new_board):
                            future += 1

                score = priority[typeB] - future

                states.append((score, posA, posB, new_board))

    states.sort()

    return [(a,b,c) for _,a,b,c in states]


# A* search

def astar(initial_board):

    open_list = []
    visited = set()
    counter = 0

    h0 = heuristic(initial_board)

    heapq.heappush(open_list, (h0, counter, initial_board, []))

    expanded_nodes = 0

    while open_list:

        f, _, board, path = heapq.heappop(open_list)

        state_key = frozenset(board.items())

        if state_key in visited:
            continue

        visited.add(state_key)

        expanded_nodes += 1

        if len(board) == 1:
            return path, board, expanded_nodes

        if not has_capture(board) and len(board) > 1:
            continue

        for posA, posB, new_board in generate_successors(board):

            key = frozenset(new_board.items())

            if key in visited:
                continue

            g_new = len(path) + 1
            h = heuristic(new_board)
            f_new = g_new + h
            counter += 1

            # heapq.heappush(
            #     open_list,
            #     (g_new + h, counter, new_board, path + [(posA, posB)])
            # )
            f_new = g_new + h

            heapq.heappush(
                open_list,
                (f_new, counter, new_board, path + [(posA, posB, g_new, h, f_new)])
            )

    return None, None, expanded_nodes


# Visualization

def print_board(pieces):
    grid = [["." for _ in range(8)] for _ in range(8)]

    for (r, c), p in pieces.items():
        grid[r][c] = PIECE_SYMBOLS.get(p, p)

    print("  a b c d e f g h")

    for i in range(8):
        row_label = 8 - i
        print(row_label, end=" ")

        for j in range(8):
            print(grid[i][j], end=" ")

        print()

    print()



def to_chess_pos(row, col):
    return f"{chr(ord('a') + col)}{8 - row}"

# Hàm in ra toàn bộ không có animation
# def replay_solution(initial_board, path):

#     board = initial_board.copy()

#     print("\nInitial board:\n")
#     print_board(board)

#     for step, (a, b, g, h, f) in enumerate(path):

#         piece = board[a]

#         del board[a]
#         del board[b]
#         board[b] = piece

#         print(
#             f"Step {step + 1}: {PIECE_SYMBOLS.get(piece, piece)} "
#             f"{to_chess_pos(a[0], a[1])} "
#             f"captures {to_chess_pos(b[0], b[1])} "
#             f"| g = {g} | h = {h} | f = {f}"
#         )

#         print_board(board)

def replay_solution(initial_board, path, delay=0.7):

    board = initial_board.copy()

    clear_screen()
    print("Initial board:\n")
    print_board(board)
    time.sleep(0.5)

    for step, (a, b, g, h, f) in enumerate(path):

        piece = board[a]

        del board[a]
        del board[b]
        board[b] = piece

        clear_screen()

        print(
            f"Step {step + 1}: {PIECE_SYMBOLS.get(piece, piece)} "
            f"{to_chess_pos(a[0], a[1])} "
            f"captures {to_chess_pos(b[0], b[1])} "
            f"| g={g} | h={h} | f={f}\n"
        )

        print_board(board)

        time.sleep(delay)
def solve(initial_board):

    tracemalloc.start()
    start = time.perf_counter()

    path, final_board, nodes = astar(initial_board)

    end = time.perf_counter()
    memory = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    if path:
        replay_solution(initial_board, path)
        print("Final piece:", final_board)
    else:
        print("No solution found")

    print(f"\nNode mở rộng: {nodes}")
    print(f"Thời gian: {end - start:.5f} s")
    print(f"Memory: {round(memory / 1024, 2)} KB")
