import copy

from base import WHITE, BLACK
from variants.classic import pieces
from variants.classic.board import Board


class Rules:
    def get_legal_moves(self, board: Board, x, y, player_color):
        piece = board.get_piece(x, y)

        if isinstance(piece, pieces.Pawn):
            return self.generate_pawn_moves(board, x, y)

        return self.generate_moves(board, x, y, player_color)

    def generate_moves(self, board, x, y, player_color):
        piece = board.get_piece(x, y)

        if not piece or piece.color != player_color:
            return []

        moves = []

        for dx, dy in piece.directions:

            max_steps = 7 if piece.sliding else 1
            print(piece.sliding)
            for step in range(1, max_steps + 1):

                x_new = x + dx * step
                y_new = y + dy * step

                print(x_new, y_new)
                if not board.is_position_in_bounds(x_new, y_new):
                    continue

                target_square = board.get_piece(x_new, y_new)

                if not self._is_legal_target(board, x, y, x_new, y_new, player_color):
                    break

                moves.append((x_new, y_new))

                if target_square:
                    break

        return moves


    def _is_legal_target(self, board, x, y, x_new, y_new, player_color):
        target_square = board.get_piece(x_new, y_new)

        if target_square and target_square.color == player_color:
            return False

        supposed_board = copy.deepcopy(board)
        supposed_board.apply_move(x, y, x_new, y_new)

        return not self.is_in_check(supposed_board, player_color)


    def generate_pawn_moves(self, board: Board, x, y):
        piece = board.get_piece(x, y)
        moves = []
        direction = piece.direction

        # 1. Обычный ход вперёд
        if board.is_empty(x + direction, y):
            moves.append((x + direction, y))

            # 2. Двойной ход
            if self.is_pawn_starting_rank(y):
                if board.is_empty(x + 2 * direction, y):
                    moves.append((x + 2 * direction, y))

        # 3. Взятия
        for dc in [-1, 1]:
            new_row = x + direction
            new_col = y + dc

            if board.is_enemy(new_row, new_col, piece.color):
                moves.append((new_row, new_col))

        # 4. En passant
        # if self.can_en_passant(...):
        #     moves.append(...)

        return moves


    def is_pawn_starting_rank(self, y):
        return True if y == 1 or y == 6 else False


    def is_in_check(self, board, color):
        king_position = board.get_king_position(color)
        if not king_position:
            return False

        opponent_color = BLACK if color == WHITE else WHITE

        for y in range(8):
            for x in range(8):
                piece = board.get_piece(x, y)
                if piece and piece.color == opponent_color:
                    if king_position in self.get_legal_moves(board, x, y, color):
                        return True
        return False

    def is_checkmate(self, board, color):
        if not self.is_in_check(board, color):
            return False

        for y in range(8):
            for x in range(8):
                piece = board.get_piece(x, y)
                if piece and piece.color == color:
                    for x_new, y_new in self.get_legal_moves(board, x, y, color):
                        supposed_board = copy.deepcopy(board)
                        supposed_board.apply_move(x, y, x_new, y_new)

                        if not self.is_in_check(supposed_board, color):
                            return False
        return True

    def is_stalemate(self, board, color):
        if self.is_in_check(board, color):
            return False

        for y in range(8):
            for x in range(8):
                piece = board.get_piece(x, y)
                if piece and piece.color == color:
                    for x_new, y_new in self.get_legal_moves(board, x, y, color):
                        supposed_board = copy.deepcopy(board)
                        supposed_board.apply_move(x, y, x_new, y_new)

                        if not self.is_in_check(supposed_board, color):
                            return False
        return True
