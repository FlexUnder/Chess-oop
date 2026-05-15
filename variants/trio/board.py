# variants/trio/board.py

from copy import deepcopy

from base import WHITE, BLACK, RED


class Board:

    SIZE = 12

    def __init__(self):
        self.field = {}
        # history хранит снимки field для undo (как в classic/local.py)
        self.history = []

    # ==========================================
    # BASIC
    # ==========================================

    def is_position_in_bounds(self, x, y):
        return 0 <= x < self.SIZE and 0 <= y < self.SIZE

    def get_piece(self, x, y):
        return self.field.get((x, y))

    def set_piece(self, x, y, piece):
        if not self.is_position_in_bounds(x, y):
            raise ValueError(f'Invalid position {(x, y)}')
        self.field[(x, y)] = piece

    def remove_piece(self, x, y):
        if (x, y) in self.field:
            del self.field[(x, y)]

    # ==========================================
    # MOVES
    # ==========================================

    def apply_move(self, from_x, from_y, to_x, to_y):
        piece = self.get_piece(from_x, from_y)

        if piece is None:
            raise ValueError('No piece on source position')

        self.remove_piece(from_x, from_y)
        self.field[(to_x, to_y)] = piece
        piece.has_moved = True

        # last_move нужен для взятия на проходе в rules
        self.last_move = {
            'piece': piece,
            'from': (from_x, from_y),
            'to': (to_x, to_y),
        }

        return self.last_move

    # ==========================================
    # HELPERS
    # ==========================================

    def clone(self):
        return deepcopy(self)

    def clear(self):
        self.field.clear()
        self.history.clear()

    def get_players(self):
        return [WHITE, BLACK, RED]

    def get_king_position(self, color):
        for (x, y), piece in self.field.items():
            if piece.color == color and piece.__class__.__name__ == 'King':
                return x, y
        return None

    def iter_pieces(self):
        for (x, y), piece in list(self.field.items()):
            yield x, y, piece
