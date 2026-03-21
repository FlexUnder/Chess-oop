import importlib
pieces = importlib.import_module('variants.hex.pieces')

BOARD_SIZE = 5

ORTHO = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
DIAG  = [(2, -1), (1, -2), (-1, -1), (-2, 1), (-1, 2), (1, 1)]

KNIGHT_MOVES = []
for dq, dr in ORTHO:
    mid_q, mid_r = dq * 2, dr * 2
    for sdq, sdr in ORTHO:
        if (sdq, sdr) != (dq, dr) and (sdq, sdr) != (-dq, -dr):
            KNIGHT_MOVES.append((mid_q + sdq, mid_r + sdr))


def _valid_hexes():
    valid = set()
    for q in range(-BOARD_SIZE, BOARD_SIZE + 1):
        r1 = max(-BOARD_SIZE, -q - BOARD_SIZE)
        r2 = min(BOARD_SIZE, -q + BOARD_SIZE)
        for r in range(r1, r2 + 1):
            valid.add((q, r))
    return valid

VALID_HEXES = _valid_hexes()


class Move:
    def __init__(self, fq, fr, tq, tr):
        self.from_x = fq
        self.from_y = fr
        self.to_x   = tq
        self.to_y   = tr


class Board:
    def __init__(self):
        self.field  = {}
        self.history = []

    def get_piece(self, q, r):
        return self.field.get((q, r))

    def set_piece(self, q, r, piece):
        if (q, r) in self.field:
            raise Exception(f"Клетка ({q},{r}) уже занята!")
        self.field[(q, r)] = piece

    def apply_move(self, fq, fr, tq, tr) -> Move:
        piece = self.field.pop((fq, fr))
        self.field[(tq, tr)] = piece
        piece.has_moved = True
        return Move(fq, fr, tq, tr)

    def is_position_in_bounds(self, q, r) -> bool:
        return (q, r) in VALID_HEXES

    def is_empty(self, q, r) -> bool:
        return (q, r) in VALID_HEXES and (q, r) not in self.field

    def is_enemy(self, q, r, player_color) -> bool:
        piece = self.field.get((q, r))
        return piece is not None and piece.color != player_color

    def get_king_position(self, color):
        for (q, r), piece in self.field.items():
            if isinstance(piece, pieces.King) and piece.color == color:
                return q, r
        return None
