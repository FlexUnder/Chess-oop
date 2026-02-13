def is_in_check(board, color):
    king_pos = find_king(board, color)
    if not king_pos:
        return False

    opponent = 'black' if color == 'white' else 'white'

    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece and piece.color == opponent:
                if king_pos in piece.get_moves(board, i, j):
                    return True
    return False


def is_checkmate(board, color):
    if not is_in_check(board, color):
        return False

    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece and piece.color == color:
                for move in piece.get_moves(board, i, j):
                    temp = copy.deepcopy(board)
                    temp[move[0]][move[1]] = piece
                    temp[i][j] = None

                    if not is_in_check(temp, color):
                        return False
    return True


def is_stalemate(board, color):
    if is_in_check(board, color):
        return False

    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece and piece.color == color:
                for move in piece.get_moves(board, i, j):
                    temp = copy.deepcopy(board)
                    temp[move[0]][move[1]] = piece
                    temp[i][j] = None

                    if not is_in_check(temp, color):
                        return False
    return True


def get_valid_moves(board, from_pos, player):
    x, y = from_pos
    piece = board[x][y]

    if not piece or piece.color != player:
        return []

    moves = []
    for move in piece.get_moves(board, x, y):
        temp = copy.deepcopy(board)
        temp[move[0]][move[1]] = piece
        temp[x][y] = None

        if not is_in_check(temp, player):
            moves.append(move)

    return moves