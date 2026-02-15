from base import WHITE, BLACK
from variants.classic import pieces


class Rules:
    def is_in_check(self, board, color):
        king_position = board.get_king_position(color)
        if not king_position:
            return False

        opponent_color = BLACK if color == WHITE else WHITE

        for y in range(8):
            for x in range(8):
                piece = board.get_piece(x, y)
                if piece and piece.color == opponent_color:
                    if king_position in piece.get_moves(board, x, y):
                        return True
        return False

    def is_checkmate(self, board, color):
        if not self.is_in_check(board, color):
            return False

        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece and piece.color == color:
                    for move in piece.get_moves(board, i, j):
                        temp = copy.deepcopy(board)
                        temp[move[0]][move[1]] = piece
                        temp[i][j] = None

                        if not self.is_in_check(temp, color):
                            return False
        return True

    def is_stalemate(self, board, color):
        if self.is_in_check(board, color):
            return False

        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece and piece.color == color:
                    for move in piece.get_moves(board, i, j):
                        temp = copy.deepcopy(board)
                        temp[move[0]][move[1]] = piece
                        temp[i][j] = None

                        if not self.is_in_check(temp, color):
                            return False
        return True

    def get_valid_moves(self, board, position, player_color):
        x, y = position
        piece = board.get_piece(x, y)

        if not piece or piece.color != player_color:
            return []

        moves = []
        for dx, dy in dirs:
        for i in range(1, 8):
            x_new, y_new = x + dx * i, y + dy * i
            piece = board.get_piece(x_new, y_new)
            if not piece and piece.color != self.color:
                moves.append((x_new, y_new))
        for direction in piece.directions:
            temp = copy.deepcopy(board)
            temp[move[0]][move[1]] = piece
            temp[x][y] = None

            if not self.is_in_check(temp, player):
                moves.append(move)

        return moves

    def get_pseudo_legal_moves(self, board, row, col):
        piece = board.get_piece(row, col)

        if isinstance(piece, pieces.Pawn):
            return self.generate_pawn_moves(board, row, col, piece)

        if piece.sliding:
            return self.generate_sliding_moves(board, row, col, piece)

        return self.generate_step_moves(board, row, col, piece)

    def generate_pawn_moves(self, board, row, col, piece):
        moves = []
        direction = piece.direction

        # 1. Обычный ход вперёд
        if board.is_empty(row + direction, col):
            moves.append((row + direction, col))

            # 2. Двойной ход
            if self.is_starting_rank(row, piece):
                if board.is_empty(row + 2 * direction, col):
                    moves.append((row + 2 * direction, col))

        # 3. Взятия
        for dc in [-1, 1]:
            new_row = row + direction
            new_col = col + dc

            if board.has_enemy(new_row, new_col, piece.color):
                moves.append((new_row, new_col))

        # 4. En passant
        if self.can_en_passant(...):
            moves.append(...)

        return moves
