from base import WHITE, BLACK
from variants.checkers import pieces
from variants.checkers.board import Board


def create_board():
    board = Board()

    for y in range(3):
        for x in range(8):
            if (x + y) % 2 != 0:
                board.set_piece(x, y, pieces.Man(BLACK))

    for y in range(5, 8):
        for x in range(8):
            if (x + y) % 2 != 0:
                board.set_piece(x, y, pieces.Man(WHITE))

    return board


def link_rules(board: Board, rules):
    board._rules = rules
