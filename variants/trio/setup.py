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


def place_back_rank_horizontal(board, y, color):
    """
    Горизонтальная линия фигур.
    """

    pieces = [
        Rook,
        Knight,
        Bishop,
        Queen,
        King,
        Bishop,
        Knight,
        Rook
    ]

    start_x = 2

    for i, piece_cls in enumerate(pieces):
        board.set_piece(start_x + i, y, piece_cls(color))


def place_pawns_horizontal(board, y, color):
    for x in range(2, 10):
        board.set_piece(x, y, Pawn(color))


def place_back_rank_vertical(board, x, color, king_top=True):
    """
    Вертикальная линия фигур.
    """

    pieces = [
        Rook,
        Knight,
        Bishop,
        Queen if king_top else King,
        King if king_top else Queen,
        Bishop,
        Knight,
        Rook
    ]

    start_y = 2

    for i, piece_cls in enumerate(pieces):
        board.set_piece(x, start_y + i, piece_cls(color))


def place_pawns_vertical(board, x, color):
    for y in range(2, 10):
        board.set_piece(x, y, Pawn(color))


def create_board():
    board = Board()

    # ==========================================
    # WHITE (снизу)
    # ==========================================

    place_back_rank_horizontal(board, 11, WHITE)
    place_pawns_horizontal(board, 10, WHITE)

    # ==========================================
    # BLACK (справа)
    # ==========================================

    place_back_rank_vertical(board, 11, BLACK, king_top=True)
    place_pawns_vertical(board, 10, BLACK)

    # ==========================================
    # RED (слева)
    # ==========================================

    place_back_rank_vertical(board, 0, RED, king_top=False)
    place_pawns_vertical(board, 1, RED)

    return board