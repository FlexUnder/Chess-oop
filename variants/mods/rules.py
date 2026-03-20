import copy
import base

from variants.mods import pieces
from variants.mods.board import Board


class Rules:
    def get_legal_moves(self, board: Board, x, y, player_color):
        moves = self.get_piece_moves(board, x, y, player_color)
        legal_moves = []
        for move in moves:
            supposed_board = copy.deepcopy(board)
            supposed_board.apply_move(x, y, move[0], move[1])

            if not self.is_in_check(supposed_board, player_color):
                legal_moves.append(move)

        return legal_moves


    def get_piece_moves(self, board: Board, x, y, player_color, for_attack=False):
        piece = board.get_piece(x, y)

        if isinstance(piece, pieces.Pawn):
            return self.generate_pawn_moves(board, x, y)
        elif isinstance(piece, pieces.King):
            moves = self.generate_moves(board, x, y, player_color)
            if not for_attack:
                moves += self.generate_castling_moves(board, x, y, player_color)
            return moves
        else:
            return self.generate_moves(board, x, y, player_color)


    def generate_moves(self, board, x, y, player_color):
        piece = board.get_piece(x, y)

        if not piece or piece.color != player_color:
            return []

        moves = []

        for dx, dy in piece.directions:

            max_steps = 7 if piece.sliding else 1
            for step in range(1, max_steps + 1):

                x_new = x + dx * step
                y_new = y + dy * step

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
        return True


    def generate_pawn_moves(self, board: Board, x, y):
        piece = board.get_piece(x, y)
        moves = []
        direction = piece.direction

        if board.is_empty(x, y + direction):
            moves.append((x, y + direction))

            if self.is_pawn_starting_rank(y):
                if board.is_empty(x, y + 2 * direction):
                    moves.append((x, y + 2 * direction))

        for dc in [-1, 1]:
            x_new = x + dc
            y_new = y + direction

            if board.is_enemy(x_new, y_new, piece.color):
                moves.append((x_new, y_new))

        last_move = board.last_move

        if last_move:
            moved_piece = board.get_piece(last_move.to_x, last_move.to_y)

            if isinstance(moved_piece, pieces.Pawn):
                if abs(last_move.from_y - last_move.to_y) == 2:
                    if last_move.to_y == y and abs(last_move.to_x - x) == 1:
                        moves.append((last_move.to_x, y + direction))

        return moves

    def generate_castling_moves(self, board, x, y, color):
        piece = board.get_piece(x, y)

        if piece.has_moved:
            return []

        if self.is_in_check(board, color):
            return []

        moves = []

        # короткая рокировка
        rook = board.get_piece(7, y)
        if isinstance(rook, pieces.Rook) and not rook.has_moved:
            if board.is_empty(5, y) and board.is_empty(6, y):
                if not self.is_square_attacked(board, 5, y, color) and \
                        not self.is_square_attacked(board, 6, y, color):
                    moves.append((6, y))

        # длинная рокировка
        rook = board.get_piece(0, y)
        if isinstance(rook, pieces.Rook) and not rook.has_moved:
            if board.is_empty(1, y) and board.is_empty(2, y) and board.is_empty(3, y):
                if not self.is_square_attacked(board, 2, y, color) and \
                        not self.is_square_attacked(board, 3, y, color):
                    moves.append((2, y))

        return moves


    def is_square_attacked(self, board, x, y, color):
        opponent = base.BLACK if color == base.WHITE else base.WHITE

        for yy in range(8):
            for xx in range(8):
                piece = board.get_piece(xx, yy)
                if piece and piece.color == opponent:
                    moves = self.get_piece_moves(board, xx, yy, opponent)
                    if (x, y) in moves:
                        return True
        return False


    def is_pawn_starting_rank(self, y):
        return True if y == 1 or y == 6 else False


    def get_game_finish_message(self, board, color):
        if self.is_checkmate(board, color):
            return f'Игра окончена. Шах и мат! Победа {base.color_converter[color]}'
        if self.is_stalemate(board, color):
            return 'Игра окончена. Пат!'
        return False


    def is_in_check(self, board, color):
        king_position = board.get_king_position(color)
        if not king_position:
            return False

        opponent_color = base.BLACK if color == base.WHITE else base.WHITE

        for y in range(8):
            for x in range(8):
                piece = board.get_piece(x, y)
                if piece and piece.color == opponent_color:
                    if king_position in self.get_piece_moves(board, x, y, opponent_color, for_attack=True):
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

    def get_threatened_pieces(self, board, player_color):
        opponent_color = base.WHITE if player_color == base.BLACK else base.BLACK

        attacked_squares = set()

        for y in range(board.width):
            for x in range(board.length):
                piece = board.get_piece(x, y)

                if piece and piece.color == opponent_color:
                    moves = self.get_piece_moves(board, x, y, opponent_color, for_attack=True)

                    for move in moves:
                        attacked_squares.add(move)

        threatened = []
        king_in_check = False

        for y in range(board.width):
            for x in range(board.length):
                piece = board.get_piece(x, y)

                if piece and piece.color == player_color:
                    if (x, y) in attacked_squares:
                        threatened.append((x, y))

                        if piece.__class__.__name__ == "King":
                            king_in_check = True

        return threatened, king_in_check