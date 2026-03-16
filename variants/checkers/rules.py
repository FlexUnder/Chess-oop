import importlib
import base

pieces = importlib.import_module('variants.checkers.pieces')


class Rules:
    """
    Возвращает ходы в формате [(x, y), ...] — совместимо с modes/local.py и online.py.
    Информация о взятии хранится в self._capture_map: {(fx,fy,tx,ty): (cap_x,cap_y)}.
    board.apply_move() вызывается из mode с теми же аргументами что и в шахматах,
    но Board.apply_move() у шашек дополнительно удаляет съеденную шашку через этот словарь.
    """

    def __init__(self):
        # Словарь взятий: ключ (fx, fy, tx, ty) -> (cap_x, cap_y) или None
        self._capture_map: dict = {}

    # ------------------------------------------------------------------ #
    #  Публичный интерфейс (совместимый с шахматным mode)                 #
    # ------------------------------------------------------------------ #

    def get_legal_moves(self, board, x, y, player_color):
        """
        Возвращает [(tx, ty), ...].
        Побочно заполняет self._capture_map для текущей шашки.
        Обязательное взятие: если хоть у одной шашки игрока есть бой —
        разрешены только бьющие ходы.
        """
        piece = board.get_piece(x, y)
        if not piece or piece.color != player_color:
            return []

        any_capture = self._player_has_capture(board, player_color)

        if any_capture:
            raw = self._get_capture_moves(board, x, y, player_color)
        else:
            raw = self._get_quiet_moves(board, x, y, player_color)

        moves = []
        for tx, ty, cap_x, cap_y in raw:
            self._capture_map[(x, y, tx, ty)] = (cap_x, cap_y) if cap_x is not None else None
            moves.append((tx, ty))

        return moves

    def get_game_finish_message(self, board, color):
        if self._is_loss(board, color):
            opponent = base.BLACK if color == base.WHITE else base.WHITE
            winner = base.color_converter(opponent)
            return f'Игра окончена. Победа {winner}!'
        return False

    def is_checkmate(self, board, color):
        """Заглушка для совместимости с modes/local.py — в шашках нет шаха."""
        return self._is_loss(board, color)

    def is_stalemate(self, board, color):
        """Заглушка для совместимости с modes/local.py — в шашках пат = проигрыш."""
        return False

    # ------------------------------------------------------------------ #
    #  Применение хода — вызывается из Board, знает о взятии              #
    # ------------------------------------------------------------------ #

    def prepare_move(self, board, fx, fy, tx, ty):
        """
        Вызывается из mode перед board.apply_move().
        Возвращает (cap_x, cap_y) если ход — взятие, иначе (None, None).
        Также превращает шашку в дамку после хода.
        """
        cap = self._capture_map.get((fx, fy, tx, ty))
        cap_x, cap_y = cap if cap else (None, None)
        return cap_x, cap_y

    def after_move(self, board, tx, ty):
        """Вызывается после board.apply_move() — превращает шашку в дамку."""
        board.promote_if_needed(tx, ty)

    # ------------------------------------------------------------------ #
    #  Конец игры                                                         #
    # ------------------------------------------------------------------ #

    def _is_loss(self, board, color):
        for y in range(8):
            for x in range(8):
                piece = board.get_piece(x, y)
                if piece and piece.color == color:
                    if self.get_legal_moves(board, x, y, color):
                        return False
        return True

    # ------------------------------------------------------------------ #
    #  Тихие ходы                                                         #
    # ------------------------------------------------------------------ #

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

    # ------------------------------------------------------------------ #
    #  Бьющие ходы                                                        #
    # ------------------------------------------------------------------ #

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