from base import WHITE


class Piece:
    def __init__(self, color):
        self.symbol = 'E'
        self.color = color
        self.sliding = False

    def __repr__(self):
        return self.symbol


class Man(Piece):
    """Обычная шашка"""
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '●'
        self.sliding = False
        self.direction = -1 if color == WHITE else 1


class King(Piece):
    """Дамка — ходит по диагонали на любое расстояние"""
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♔'
        self.sliding = True
        self.directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
