def setup_board():
    board = [[None for _ in range(8)] for _ in range(8)]

    for i in range(8):
        board[6][i] = Pawn('white')
        board[1][i] = Pawn('black')

    board[7][0] = Rook('white')
    board[7][1] = Knight('white')
    board[7][2] = Bishop('white')
    board[7][3] = Queen('white')
    board[7][4] = King('white')
    board[7][5] = Bishop('white')
    board[7][6] = Knight('white')
    board[7][7] = Rook('white')

    board[0][0] = Rook('black')
    board[0][1] = Knight('black')
    board[0][2] = Bishop('black')
    board[0][3] = Queen('black')
    board[0][4] = King('black')
    board[0][5] = Bishop('black')
    board[0][6] = Knight('black')
    board[0][7] = Rook('black')

    return board