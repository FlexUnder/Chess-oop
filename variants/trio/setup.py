# variants/trio/setup.py

from base import WHITE, BLACK, RED

from variants.trio.board import Board
from variants.trio.pieces import (
    Pawn,
    Rook,
    Knight,
    Bishop,
    Queen,
    King
)


def create_board():

    board = Board()

    # ==========================================
    # WHITE (снизу)
    # ==========================================

    white_back = [
        Rook,
        Knight,
        Bishop,
        Queen,
        King,
        Bishop,
        Knight,
        Rook
    ]

    for i, piece_cls in enumerate(white_back):
        board.set_piece(i + 2, 11, piece_cls(WHITE))

    for i in range(8):
        board.set_piece(i + 2, 10, Pawn(WHITE))

    # ==========================================
    # BLACK (сверху)
    # ==========================================

    black_back = [
        Rook,
        Knight,
        Bishop,
        Queen,
        King,
        Bishop,
        Knight,
        Rook
    ]

    for i, piece_cls in enumerate(black_back):
        board.set_piece(i + 2, 0, piece_cls(BLACK))

    for i in range(8):
        board.set_piece(i + 2, 1, Pawn(BLACK))

    # ==========================================
    # RED (слева)
    # ==========================================

    red_back = [
        Rook,
        Knight,
        Bishop,
        Queen,
        King,
        Bishop,
        Knight,
        Rook
    ]

    for i, piece_cls in enumerate(red_back):
        board.set_piece(0, i + 2, piece_cls(RED))

    for i in range(8):
        board.set_piece(1, i + 2, Pawn(RED))

    return board