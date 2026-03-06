from variants.checkers import pieces


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

    def get_piece(self, x, y):
        return self.field[y][x]

    def set_piece(self, x, y, piece):
        if self.field[y][x] is None:
            self.field[y][x] = piece
        else:
            raise Exception("Клетка уже занята. Непутевый ты программист!"
                            " Для передвижения фигур используй apply_move(), а не set()")

    def apply_move(self, fx, fy, tx, ty) -> Move:
        move = Move(fx, fy, tx, ty)
        self.field[fy][fx], self.field[ty][tx] = None, self.field[fy][fx]
        return move

    def is_position_in_bounds(self, x, y) -> bool:
        return 0 <= y < self.width and 0 <= x < self.length

    def get_king_position(self, color):
        for y in range(self.width):
            for x in range(self.length):
                piece = self.field[y][x]
                if isinstance(piece, pieces.King) and piece.color == color:
                    return x, y
        return None

    def is_empty(self, x, y) -> bool:
        if not self.is_position_in_bounds(x, y):
            return False
        return True if self.field[y][x] is None else False

    def is_enemy(self, x, y, player_color) -> bool:
        if not self.is_position_in_bounds(x, y):
            return False
        return True if self.field[y][x] and self.field[y][x].color != player_color else False
