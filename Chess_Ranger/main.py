# main.py
import copy
import random

from chessRanger_DFS import giai as dfs_solve
from chessRanger_Heuristic import solve as astar_solve
from board_generator import generate_playable_board
from input_parser import load_board_from_file
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
LEVEL_CONFIG = {
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    11: 11
}

def menu():
    print("\n===== CHESS RANGER SOLVER =====")
    print("1. DFS")
    print("2. A* Heuristic")
    print("3. Thoát")
def choose_input():
    print("\n=== CHỌN INPUT ===")
    print("1. Nhập tay")
    print("2. Đọc từ file")
    print("3. Random theo level (Chess Ranger 4 → 11)")

    choice = input("Chọn: ")

    if choice == "1":
        return {
            (3, 2): "B",
            (5, 2): "P",
            (3, 3): "N",
            (4, 4): "R",
        }

    elif choice == "2":
        filename = input("Nhập tên file: ")
        return load_board_from_file(filename)

    elif choice == "3":
        level = int(input("Chọn level (4 → 11): "))

        if level < 4 or level > 11:
            print("Level không hợp lệ!")
            return choose_input()

        board = generate_playable_board(level)

        print(f"\nGenerated board (level {level}):")
        return board

    else:
        print("Lựa chọn sai!")
        return choose_input()

def main():
    # =========================
    # CONFIG BÀN CỜ TẠI ĐÂY
    # =========================
    initial_board = choose_input()

    while True:
        menu()
        choice = input("Chọn thuật toán: ")

        if choice == "1":
            print("\n--- CHẠY DFS ---")
            dfs_solve(copy.deepcopy(initial_board))

        elif choice == "2":
            print("\n--- CHẠY A* HEURISTIC ---")
            astar_solve(copy.deepcopy(initial_board))

        elif choice == "3":
            print("Thoát chương trình.")
            break

        else:
            print("Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    main()