import copy
import base

from variants.trio.pieces import Pawn, King, Rook


SIZE = 12


def _opponents(color):
    """Возвращает список цветов противников."""
    return [c for c in [base.WHITE, base.BLACK, base.RED] if c != color]


class Rules:

    # ------------------------------------------------------------------ #
    #  Публичный интерфейс                                                 #
    # ------------------------------------------------------------------ #

    def get_legal_moves(self, board, x, y, player_color):
        moves = self.get_piece_moves(board, x, y, player_color)
        legal = []
        for tx, ty in moves:
            b2 = copy.deepcopy(board)
            b2.apply_move(x, y, tx, ty)
            if not self.is_in_check(b2, player_color):
                legal.append((tx, ty))
        return legal

    def get_piece_moves(self, board, x, y, player_color, for_attack=False):
        piece = board.get_piece(x, y)
        if not piece or piece.color != player_color:
            return []

        if isinstance(piece, Pawn):
            return self._pawn_moves(board, x, y, piece)
        elif isinstance(piece, King):
            moves = self._sliding_or_step(board, x, y, player_color)
            if not for_attack:
                moves += self._castling_moves(board, x, y, player_color)
            return moves
        else:
            return self._sliding_or_step(board, x, y, player_color)

    # ------------------------------------------------------------------ #
    #  Генерация ходов                                                     #
    # ------------------------------------------------------------------ #

    def _sliding_or_step(self, board, x, y, player_color):
        piece = board.get_piece(x, y)
        moves = []
        max_steps = SIZE if piece.sliding else 1

        for dx, dy in piece.directions:
            for step in range(1, max_steps + 1):
                nx, ny = x + dx * step, y + dy * step
                if not board.is_position_in_bounds(nx, ny):
                    break
                target = board.get_piece(nx, ny)
                if target:
                    if target.color != player_color:
                        moves.append((nx, ny))
                    break
                moves.append((nx, ny))

        return moves

    def _pawn_moves(self, board, x, y, piece):
        moves = []
        dx, dy = piece.direction

        # Ход вперёд
        nx, ny = x + dx, y + dy
        if board.is_position_in_bounds(nx, ny) and board.get_piece(nx, ny) is None:
            moves.append((nx, ny))
            # Двойной ход с начальной позиции
            if not piece.has_moved:
                nx2, ny2 = x + 2*dx, y + 2*dy
                if board.is_position_in_bounds(nx2, ny2) and board.get_piece(nx2, ny2) is None:
                    moves.append((nx2, ny2))

        # Взятие по диагоналям
        if dx == 0:  # WHITE или BLACK — ходят вертикально, бьют по диагонали
            captures = [(x-1, y+dy), (x+1, y+dy)]
        else:        # RED — ходит горизонтально, бьёт по диагонали
            captures = [(x+dx, y-1), (x+dx, y+1)]

        for cx, cy in captures:
            if board.is_position_in_bounds(cx, cy):
                target = board.get_piece(cx, cy)
                if target and target.color != piece.color:
                    moves.append((cx, cy))

        return moves

    def _castling_moves(self, board, x, y, color):
        piece = board.get_piece(x, y)
        if piece.has_moved or self.is_in_check(board, color):
            return []

        moves = []

        # Рокировка зависит от цвета — у каждого своя сторона
        if color == base.WHITE or color == base.BLACK:
            # Короткая (вправо)
            rook = board.get_piece(9, y)
            if isinstance(rook, Rook) and not rook.has_moved:
                if all(board.get_piece(i, y) is None for i in range(x+1, 9)):
                    if not any(self.is_square_attacked(board, i, y, color) for i in range(x+1, x+3)):
                        moves.append((x+2, y))
            # Длинная (влево)
            rook = board.get_piece(2, y)
            if isinstance(rook, Rook) and not rook.has_moved:
                if all(board.get_piece(i, y) is None for i in range(3, x)):
                    if not any(self.is_square_attacked(board, i, y, color) for i in range(x-2, x)):
                        moves.append((x-2, y))
        else:  # RED ходит вертикально
            rook = board.get_piece(x, 9)
            if isinstance(rook, Rook) and not rook.has_moved:
                if all(board.get_piece(x, i) is None for i in range(y+1, 9)):
                    moves.append((x, y+2))
            rook = board.get_piece(x, 2)
            if isinstance(rook, Rook) and not rook.has_moved:
                if all(board.get_piece(x, i) is None for i in range(3, y)):
                    moves.append((x, y-2))

        return moves

    # ------------------------------------------------------------------ #
    #  Шах, мат, пат                                                      #
    # ------------------------------------------------------------------ #

    def is_in_check(self, board, color):
        king = board.get_king_position(color)
        if not king:
            return False
        kx, ky = king

        for ox, oy, piece in board.iter_pieces():
            if piece.color == color:
                continue
            if (kx, ky) in self.get_piece_moves(board, ox, oy, piece.color, for_attack=True):
                return True
        return False

    def is_checkmate(self, board, color):
        if not self.is_in_check(board, color):
            return False
        return self._no_legal_moves(board, color)

    def is_stalemate(self, board, color):
        if self.is_in_check(board, color):
            return False
        return self._no_legal_moves(board, color)

    def _no_legal_moves(self, board, color):
        for x, y, piece in board.iter_pieces():
            if piece.color == color:
                if self.get_legal_moves(board, x, y, color):
                    return False
        return True

    def is_square_attacked(self, board, x, y, color):
        for ox, oy, piece in board.iter_pieces():
            if piece.color == color:
                continue
            if (x, y) in self.get_piece_moves(board, ox, oy, piece.color, for_attack=True):
                return True
        return False

    def get_game_finish_message(self, board, color):
        if self.is_checkmate(board, color):
            return f'Игра окончена. Шах и мат! {base.color_converter[color]} выбывает!'
        if self.is_stalemate(board, color):
            return f'Игра окончена. Пат! {base.color_converter[color]} выбывает!'
        return False

    def get_threatened_pieces(self, board, player_color):
        attacked = set()
        for ox, oy, piece in board.iter_pieces():
            if piece.color == player_color:
                continue
            for move in self.get_piece_moves(board, ox, oy, piece.color, for_attack=True):
                attacked.add(move)

        threatened = []
        king_in_check = False
        for x, y, piece in board.iter_pieces():
            if piece.color == player_color and (x, y) in attacked:
                threatened.append((x, y))
                if isinstance(piece, King):
                    king_in_check = True

        return threatened, king_in_check