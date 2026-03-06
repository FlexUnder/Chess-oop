from base import WHITE, BLACK

class Piece:
    def __init__(self, color):
        self.symbol = 'E'
        self.color = color
        self.sliding = True
        self.is_king = False

    def __repr__(self):
        return self.symbol

class Checker(Piece):
    """Обычная шашка"""
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'B' if color == BLACK else 'W'  # B для Black, W для White
        self.sliding = False
        self.is_king = False
        self.directions = [(1 if color == BLACK else -1, -1), 
                          (1 if color == BLACK else -1, 1)]

class CheckerKing(Piece):
    """Дамка (наследуется от Piece)"""
    def __init__(self, color):
        super().__init__(color)
        self.symbol = 'KB' if color == BLACK else 'KW'  # KB для Black King, KW для White King
        self.sliding = True
        self.is_king = True
        self.directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]