from base import WHITE, BLACK
from variants.mods import pieces
from variants.mods.board import Board


def create_board():
    board = Board()

    for i in range(8):
        board.set_piece(i, 6, pieces.Pawn(WHITE))
        board.set_piece(i, 1, pieces.Pawn(BLACK))

    board.set_piece(0, 7, pieces.Sun(WHITE))
    board.set_piece(1, 7, pieces.Smile(WHITE))
    board.set_piece(2, 7, pieces.Sigma(WHITE))
    board.set_piece(3, 7, pieces.Queen(WHITE))
    board.set_piece(4, 7, pieces.King(WHITE))
    board.set_piece(5, 7, pieces.Sigma(WHITE))
    board.set_piece(6, 7, pieces.Smile(WHITE))
    board.set_piece(7, 7, pieces.Sun(WHITE))

    board.set_piece(0, 0, pieces.Sun(BLACK))
    board.set_piece(1, 0, pieces.Smile(BLACK))
    board.set_piece(2, 0, pieces.Sigma(BLACK))
    board.set_piece(3, 0, pieces.Queen(BLACK))
    board.set_piece(4, 0, pieces.King(BLACK))
    board.set_piece(5, 0, pieces.Sigma(BLACK))
    board.set_piece(6, 0, pieces.Smile(BLACK))
    board.set_piece(7, 0, pieces.Sun(BLACK))

    return board