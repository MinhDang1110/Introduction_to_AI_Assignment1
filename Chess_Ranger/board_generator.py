import random
from chessRanger_Heuristic import valid_capture

PIECES = ["K", "Q", "R", "B", "N", "P"]

def generate_random_board(num_pieces):
    board = {}

    while len(board) < num_pieces:
        r = random.randint(0, 7)
        c = random.randint(0, 7)

        if (r, c) in board:
            continue

        piece = random.choice(PIECES)
        board[(r, c)] = piece

    return board


def has_valid_move(board):
    items = list(board.items())

    for (p1, t1) in items:
        for (p2, t2) in items:
            if p1 == p2:
                continue
            if valid_capture(t1, p1, p2, board):
                return True
    return False


def generate_playable_board(num_pieces):
    while True:
        board = generate_random_board(num_pieces)
        if has_valid_move(board):
            return board