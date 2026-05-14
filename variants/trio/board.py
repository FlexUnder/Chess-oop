from copy import deepcopy

from base import WHITE, BLACK, RED


class Board:
    """
    Трёхсторонняя доска.

    Используется обычная координатная сетка 12x12,
    но валидными считаются только клетки трёх секторов.
    """

    SIZE = 12

    def __init__(self):
        self.field = {}
        self.history = []

    # =========================
    # BASIC
    # =========================

    def is_position_in_bounds(self, x, y):
        """
        Проверка существования клетки.

        Геометрия:
        - нижний сектор (white)
        - левый сектор (red)
        - правый сектор (black)
        """

        if not (0 <= x < self.SIZE and 0 <= y < self.SIZE):
            return False

        # Центральная область
        if 3 <= x <= 8 and 3 <= y <= 8:
            return True

        # Белый сектор
        if 2 <= x <= 9 and 8 <= y <= 11:
            return True

        # Красный сектор
        if 0 <= x <= 3 and 2 <= y <= 9:
            return True

        # Чёрный сектор
        if 8 <= x <= 11 and 2 <= y <= 9:
            return True

        return False

    def get_piece(self, x, y):
        return self.field.get((x, y))

    def set_piece(self, x, y, piece):
        if not self.is_position_in_bounds(x, y):
            raise ValueError(f"Invalid position: {(x, y)}")

        self.field[(x, y)] = piece

    def remove_piece(self, x, y):
        if (x, y) in self.field:
            del self.field[(x, y)]

    # =========================
    # MOVES
    # =========================

    def apply_move(self, from_x, from_y, to_x, to_y):
        """
        Выполняет ход.
        """

        piece = self.get_piece(from_x, from_y)

        if piece is None:
            raise ValueError("No piece on source position")

        captured_piece = self.get_piece(to_x, to_y)

        self.remove_piece(from_x, from_y)

        self.field[(to_x, to_y)] = piece

        piece.has_moved = True

        move = {
            'piece': piece,
            'from': (from_x, from_y),
            'to': (to_x, to_y),
            'captured': captured_piece
        }

        self.history.append(move)

        return move

    # =========================
    # KING HELPERS
    # =========================

    def get_king_position(self, color):
        for (x, y), piece in self.field.items():
            if piece.color == color and piece.__class__.__name__ == 'King':
                return x, y

        return None

    def is_king_alive(self, color):
        return self.get_king_position(color) is not None

    def get_players(self):
        return [WHITE, BLACK, RED]

    def get_alive_players(self):
        return [
            color for color in self.get_players()
            if self.is_king_alive(color)
        ]

    # =========================
    # BOARD STATE
    # =========================

    def clone(self):
        return deepcopy(self)

    def clear(self):
        self.field.clear()
        self.history.clear()

    # =========================
    # ITERATORS
    # =========================

    def iter_pieces(self):
        for (x, y), piece in self.field.items():
            yield x, y, piece

    def get_pieces_by_color(self, color):
        result = []

        for (x, y), piece in self.field.items():
            if piece.color == color:
                result.append((x, y, piece))

        return result