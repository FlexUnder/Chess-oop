import importlib
pieces = importlib.import_module('variants.checkers.pieces')


class Move:
    def __init__(self, from_x, from_y, to_x, to_y):
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y


class Board:
    def __init__(self, rows=8, cols=8):
        self.field = [[None for _ in range(rows)] for _ in range(cols)]
        self.width = rows
        self.length = cols
        self._rules = None  # устанавливается через setup.link_rules()

    def get_piece(self, x, y):
        return self.field[y][x]

    def set_piece(self, x, y, piece):
        if self.field[y][x] is None:
            self.field[y][x] = piece
        else:
            raise Exception("Клетка уже занята. Непутевый ты программист!"
                            " Для передвижения фигур используй apply_move(), а не set()")

    def apply_move(self, fx, fy, tx, ty) -> Move:
        """
        Применяет ход. Если в rules._capture_map есть цепочка взятий для этого хода —
        применяет все шаги цепочки последовательно. Иначе — обычный ход.
        """
        if self._rules is not None:
            chain = self._rules._capture_map.get((fx, fy, tx, ty))
            if chain:
                # Применяем каждый шаг цепочки
                cx, cy = fx, fy
                for cap_x, cap_y, land_x, land_y in chain:
                    self.apply_move_simple(cx, cy, land_x, land_y, cap_x, cap_y)
                    self.promote_if_needed(land_x, land_y)
                    cx, cy = land_x, land_y
                return Move(fx, fy, tx, ty)

        # Обычный ход (без взятия)
        self.field[ty][tx] = self.field[fy][fx]
        self.field[fy][fx] = None
        self.promote_if_needed(tx, ty)
        return Move(fx, fy, tx, ty)

    def apply_move_simple(self, fx, fy, tx, ty, cap_x=None, cap_y=None):
        """Внутренний метод: перемещает шашку и убирает съеденную."""
        self.field[ty][tx] = self.field[fy][fx]
        self.field[fy][fx] = None
        if cap_x is not None and cap_y is not None:
            self.field[cap_y][cap_x] = None

    def is_position_in_bounds(self, x, y) -> bool:
        return 0 <= y < self.width and 0 <= x < self.length

    def is_empty(self, x, y) -> bool:
        if not self.is_position_in_bounds(x, y):
            return False
        return self.field[y][x] is None

    def is_enemy(self, x, y, player_color) -> bool:
        if not self.is_position_in_bounds(x, y):
            return False
        piece = self.field[y][x]
        return piece is not None and piece.color != player_color

    def promote_if_needed(self, x, y):
        piece = self.field[y][x]
        if piece is None:
            return
        from base import WHITE, BLACK
        if isinstance(piece, pieces.Man):
            if (piece.color == WHITE and y == 0) or (piece.color == BLACK and y == 7):
                self.field[y][x] = pieces.King(piece.color)