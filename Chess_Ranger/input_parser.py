def parse_position(pos):
    col_map = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
    col = col_map[pos[0]]
    row = 8 - int(pos[1])
    return (row, col)


def load_board_from_file(filename):
    board = {}

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            piece, pos = line.split()
            board[parse_position(pos)] = piece

    return board