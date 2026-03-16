from base import WHITE, BLACK
from variants.checkers import pieces
from variants.checkers.board import Board


def create_board():
    board = Board()

    # BLACK — верхние 3 ряда (y = 0, 1, 2), на тёмных клетках
    for y in range(3):
        for x in range(8):
            if (x + y) % 2 != 0:
                board.set_piece(x, y, pieces.Man(BLACK))

    # WHITE — нижние 3 ряда (y = 5, 6, 7), на тёмных клетках
    for y in range(5, 8):
        for x in range(8):
            if (x + y) % 2 != 0:
                board.set_piece(x, y, pieces.Man(WHITE))

    return board


def link_rules(board: Board, rules):
    """Связывает доску с rules чтобы apply_move знал о взятиях."""
    board._rules = rules
