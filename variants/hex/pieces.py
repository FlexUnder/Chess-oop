from base import WHITE, BLACK


class Piece:
    def __init__(self, color):
        self.color = color
        self.symbol = '?'
        self.has_moved = False

    def __repr__(self):
        return self.symbol


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♙'
        self.direction = -1 if color == WHITE else 1


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♞'


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♝'


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♜'


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♛'


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♚'
