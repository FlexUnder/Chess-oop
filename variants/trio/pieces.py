from base import WHITE, BLACK, RED


class Piece:
    def __init__(self, color):
        self.symbol = 'E'
        self.color = color
        self.sliding = True
        self.has_moved = False

    def __repr__(self):
        return self.symbol


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♙'
        self.sliding = False
        # WHITE идёт вверх (y-), BLACK вниз (y+), RED вправо (x+)
        if color == WHITE:
            self.direction = (0, -1)
        elif color == BLACK:
            self.direction = (0, 1)
        else:  # RED
            self.direction = (1, 0)


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♞'
        self.sliding = False
        self.directions = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♝'
        self.directions = [(1,1),(1,-1),(-1,1),(-1,-1)]


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♜'
        self.directions = [(1,0),(-1,0),(0,1),(0,-1)]


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♛'
        self.directions = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♚'
        self.sliding = False
        self.directions = [(-1,1),(0,1),(1,1),(-1,0),(1,0),(-1,-1),(0,-1),(1,-1)]