import copy
import importlib
import base

pieces = importlib.import_module('variants.checkers.pieces')


class Rules:

    def __init__(self):
        self._capture_map: dict = {}

    def get_legal_moves(self, board, x, y, player_color):
        piece = board.get_piece(x, y)
        if not piece or piece.color != player_color:
            return []

        self._capture_map = {}

        if self._player_has_capture(board, player_color):
            chains = self._build_capture_chains(board, x, y, player_color)
            best: dict = {}
            for chain in chains:
                tx, ty = chain[-1][2], chain[-1][3]
                if (tx, ty) not in best or len(chain) > len(best[(tx, ty)]):
                    best[(tx, ty)] = chain
            moves = []
            for (tx, ty), chain in best.items():
                self._capture_map[(x, y, tx, ty)] = chain
                moves.append((tx, ty))
            return moves
        else:
            raw = self._get_quiet_moves(board, x, y, player_color)
            moves = []
            for tx, ty, _, _ in raw:
                self._capture_map[(x, y, tx, ty)] = None
                moves.append((tx, ty))
            return moves

    def get_game_finish_message(self, board, color):
        if self._is_loss(board, color):
            opponent = base.BLACK if color == base.WHITE else base.WHITE
            winner = base.color_converter(opponent)
            return f'Игра окончена. Победа {winner}!'
        return False

    def is_checkmate(self, board, color):
        return self._is_loss(board, color)

    def is_stalemate(self, board, color):
        return False

    def _is_loss(self, board, color):
        for y in range(8):
            for x in range(8):
                piece = board.get_piece(x, y)
                if piece and piece.color == color:
                    if self.get_legal_moves(board, x, y, color):
                        return False
        return True

    def _build_capture_chains(self, board, x, y, player_color):

        piece = board.get_piece(x, y)
        if isinstance(piece, pieces.King):
            single_captures = self._king_captures(board, x, y, player_color, set())
        else:
            single_captures = self._man_captures(board, x, y, player_color, set())

        if not single_captures:
            return []

        result = []
        for lx, ly, ex, ey in single_captures:
            step = (ex, ey, lx, ly)
            board_copy = copy.deepcopy(board)
            board_copy.apply_move_simple(x, y, lx, ly, ex, ey)
            board_copy.promote_if_needed(lx, ly)

            further = self._build_capture_chains(board_copy, lx, ly, player_color)
            if further:
                for chain in further:
                    result.append([step] + chain)
            else:
                result.append([step])

        return result

    def _get_quiet_moves(self, board, x, y, player_color):
        piece = board.get_piece(x, y)
        if isinstance(piece, pieces.King):
            return self._king_quiet_moves(board, x, y)
        return self._man_quiet_moves(board, x, y, piece)

    def _man_quiet_moves(self, board, x, y, piece):
        moves = []
        for dx in [-1, 1]:
            nx, ny = x + dx, y + piece.direction
            if board.is_empty(nx, ny):
                moves.append((nx, ny, None, None))
        return moves

    def _king_quiet_moves(self, board, x, y):
        moves = []
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            step = 1
            while True:
                nx, ny = x + dx * step, y + dy * step
                if not board.is_position_in_bounds(nx, ny):
                    break
                if board.is_empty(nx, ny):
                    moves.append((nx, ny, None, None))
                    step += 1
                else:
                    break
        return moves

    def _player_has_capture(self, board, player_color):
        for y in range(8):
            for x in range(8):
                piece = board.get_piece(x, y)
                if piece and piece.color == player_color:
                    if self._get_capture_moves(board, x, y, player_color):
                        return True
        return False

    def _get_capture_moves(self, board, x, y, player_color):
        piece = board.get_piece(x, y)
        if not piece or piece.color != player_color:
            return []
        if isinstance(piece, pieces.King):
            return self._king_captures(board, x, y, player_color, set())
        return self._man_captures(board, x, y, player_color, set())

    def _man_captures(self, board, x, y, player_color, visited: set):
        moves = []
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            ex, ey = x + dx, y + dy
            lx, ly = x + 2 * dx, y + 2 * dy
            if not board.is_position_in_bounds(lx, ly):
                continue
            if not board.is_enemy(ex, ey, player_color):
                continue
            if not board.is_empty(lx, ly):
                continue
            if (ex, ey) in visited:
                continue
            moves.append((lx, ly, ex, ey))
        return moves

    def _king_captures(self, board, x, y, player_color, visited: set):
        moves = []
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            step = 1
            enemy_pos = None
            while True:
                nx, ny = x + dx * step, y + dy * step
                if not board.is_position_in_bounds(nx, ny):
                    break
                cell = board.get_piece(nx, ny)
                if cell is None:
                    if enemy_pos and enemy_pos not in visited:
                        moves.append((nx, ny, enemy_pos[0], enemy_pos[1]))
                elif cell.color != player_color:
                    if enemy_pos:
                        break
                    enemy_pos = (nx, ny)
                else:
                    break
                step += 1
        return moves