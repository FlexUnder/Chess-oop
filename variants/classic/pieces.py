from base import WHITE


class Piece:
    def __init__(self, color):
        self.symbol = 'E'
        self.color = color
        self.sliding = True

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
        self.sliding = False
        self.moves = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♝'
        self.moves = [(1,1),(1,-1),(-1,1),(-1,-1)]

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♜'
        self.moves = [(1,0),(-1,0),(0,1),(0,-1)]

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♛'
        self.moves = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♚'
        self.moves = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
