class Piece:
    def __init__(self, color):
        self.symbol = 'E'
        self.color = color

    def __repr__(self):
        return self.symbol


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♙' if color == 'white' else '♟'
        self.direction = -1 if color == 'white' else 1  # Белые идут вверх (x уменьшается)

    def get_moves(self, board, x, y):
        moves = []

        # Вперед
        nx = x + self.direction
        if 0 <= nx < 8 and board[nx][y] is None:
            moves.append((nx, y))

            # Двойной ход
            start_row = 6 if self.color == 'white' else 1
            if x == start_row:
                nx2 = x + 2 * self.direction
                if 0 <= nx2 < 8 and board[nx2][y] is None:
                    moves.append((nx2, y))

        # Взятие
        for dy in [-1, 1]:
            nx, ny = x + self.direction, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                piece = board[nx][ny]
                if piece and piece.color != self.color:
                    moves.append((nx, ny))

        return moves


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♘' if color == 'white' else '♞'

    def get_moves(self, board, x, y):
        moves = []
        jumps = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]

        for dx, dy in jumps:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                piece = board[nx][ny]
                if not piece or piece.color != self.color:
                    moves.append((nx, ny))

        return moves


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♗' if color == 'white' else '♝'

    def get_moves(self, board, x, y):
        moves = []
        dirs = [(1,1),(1,-1),(-1,1),(-1,-1)]

        for dx, dy in dirs:
            for i in range(1, 8):
                nx, ny = x + dx*i, y + dy*i
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break

                piece = board[nx][ny]
                if not piece:
                    moves.append((nx, ny))
                elif piece.color != self.color:
                    moves.append((nx, ny))
                    break
                else:
                    break

        return moves


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♖' if color == 'white' else '♜'

    def get_moves(self, board, x, y):
        moves = []
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]

        for dx, dy in dirs:
            for i in range(1, 8):
                nx, ny = x + dx*i, y + dy*i
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break

                piece = board[nx][ny]
                if not piece:
                    moves.append((nx, ny))
                elif piece.color != self.color:
                    moves.append((nx, ny))
                    break
                else:
                    break

        return moves


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♕' if color == 'white' else '♛'

    def get_moves(self, board, x, y):
        moves = []
        dirs = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]

        for dx, dy in dirs:
            for i in range(1, 8):
                nx, ny = x + dx*i, y + dy*i
                if not (0 <= nx < 8 and 0 <= ny < 8):
                    break

                piece = board[nx][ny]
                if not piece:
                    moves.append((nx, ny))
                elif piece.color != self.color:
                    moves.append((nx, ny))
                    break
                else:
                    break

        return moves


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = '♔' if color == 'white' else '♚'

    def get_moves(self, board, x, y):
        moves = []

        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx == 0 and dy == 0:
                    continue

                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    piece = board[nx][ny]
                    if not piece or piece.color != self.color:
                        moves.append((nx, ny))

        return moves
