import copy
import base
import importlib

pieces = importlib.import_module('variants.hex.pieces')
board_mod = importlib.import_module('variants.hex.board')

ORTHO  = board_mod.ORTHO
DIAG   = board_mod.DIAG
KNIGHT_MOVES = board_mod.KNIGHT_MOVES


class Rules:

    def get_legal_moves(self, board, q, r, player_color):
        raw = self._get_piece_moves(board, q, r, player_color)
        legal = []
        for tq, tr in raw:
            b2 = copy.deepcopy(board)
            b2.apply_move(q, r, tq, tr)
            if not self.is_in_check(b2, player_color):
                legal.append((tq, tr))
        return legal

    def _get_piece_moves(self, board, q, r, player_color):
        piece = board.get_piece(q, r)
        if not piece or piece.color != player_color:
            return []

        if isinstance(piece, pieces.Pawn):
            return self._pawn_moves(board, q, r, piece)
        if isinstance(piece, pieces.Knight):
            return self._step_moves(board, q, r, KNIGHT_MOVES, player_color)
        if isinstance(piece, pieces.Bishop):
            return self._sliding_moves(board, q, r, DIAG, player_color)
        if isinstance(piece, pieces.Rook):
            return self._sliding_moves(board, q, r, ORTHO, player_color)
        if isinstance(piece, pieces.Queen):
            return self._sliding_moves(board, q, r, ORTHO + DIAG, player_color)
        if isinstance(piece, pieces.King):
            return self._step_moves(board, q, r, ORTHO + DIAG, player_color)
        return []

    def _sliding_moves(self, board, q, r, dirs, player_color):
        moves = []
        for dq, dr in dirs:
            for step in range(1, 11):
                nq, nr = q + dq * step, r + dr * step
                if not board.is_position_in_bounds(nq, nr):
                    break
                target = board.get_piece(nq, nr)
                if target:
                    if target.color != player_color:
                        moves.append((nq, nr))
                    break
                moves.append((nq, nr))
        return moves

    def _step_moves(self, board, q, r, dirs, player_color):
        moves = []
        for dq, dr in dirs:
            nq, nr = q + dq, r + dr
            if not board.is_position_in_bounds(nq, nr):
                continue
            target = board.get_piece(nq, nr)
            if target is None or target.color != player_color:
                moves.append((nq, nr))
        return moves

    def _pawn_moves(self, board, q, r, piece):
        moves = []
        d = piece.direction

        nq, nr = q, r + d
        if board.is_position_in_bounds(nq, nr) and board.is_empty(nq, nr):
            moves.append((nq, nr))
            if not piece.has_moved:
                nq2, nr2 = q, r + 2 * d
                if board.is_position_in_bounds(nq2, nr2) and board.is_empty(nq2, nr2):
                    moves.append((nq2, nr2))

        diag = [(1, -1), (-1, 0)] if piece.color == base.WHITE else [(1, 0), (-1, 1)]
        for dq, dr in diag:
            cq, cr = q + dq, r + dr
            if board.is_position_in_bounds(cq, cr):
                target = board.get_piece(cq, cr)
                if target and target.color != piece.color:
                    moves.append((cq, cr))

        return moves

    def is_in_check(self, board, color):
        king = board.get_king_position(color)
        if not king:
            return False
        opponent = base.BLACK if color == base.WHITE else base.WHITE
        for (q, r), piece in board.field.items():
            if piece.color == opponent:
                if king in self._get_piece_moves(board, q, r, opponent):
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
        for (q, r), piece in board.field.items():
            if piece.color == color:
                if self.get_legal_moves(board, q, r, color):
                    return False
        return True

    def get_game_finish_message(self, board, color):
        if self.is_checkmate(board, color):
            winner = base.color_converter(
                base.BLACK if color == base.WHITE else base.WHITE
            )
            return f'Игра окончена. Шах и мат! Победа {winner}'
        if self.is_stalemate(board, color):
            return 'Игра окончена. Пат!'
        return False
