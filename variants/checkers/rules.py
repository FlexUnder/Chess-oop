import copy
from variants.classic import pieces
from variants.classic.board import Board


class Rules:
    def get_legal_moves(self, board: Board, x, y, player_color):
        """Получение всех легальных ходов для фигуры"""
        piece = board.get_piece(x, y)

        if not piece or piece.color != player_color:
            return []

        # Сначала проверяем, есть ли обязательные ходы с взятием
        capture_moves = self.get_all_capture_moves(board, player_color)

        # Если есть ходы с взятием, другие ходы недоступны
        if capture_moves:
            # Возвращаем только ходы с взятием для этой фигуры
            piece_captures = [move for move in capture_moves if move[:2] == (x, y)]
            return piece_captures

        # Если нет ходов с взятием, возвращаем обычные ходы
        return self.generate_regular_moves(board, x, y, player_color)

    def generate_regular_moves(self, board, x, y, player_color):
        """Генерация обычных ходов (без взятия)"""
        piece = board.get_piece(x, y)
        moves = []

        # Определяем направления в зависимости от типа фигуры
        if piece.is_king:
            # Дамка может ходить во все стороны
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            # Обычная шашка ходит только вперед
            if piece.color == 'black':
                directions = [(1, -1), (1, 1)]  # Черные вниз
            else:
                directions = [(-1, -1), (-1, 1)]  # Белые вверх

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy

            if not board.is_position_in_bounds(new_x, new_y):
                continue

            target = board.get_piece(new_x, new_y)

            # Клетка должна быть пустой
            if target is None:
                moves.append((new_x, new_y))

        return moves

    def get_all_capture_moves(self, board, player_color):
        """Получение всех возможных ходов с взятием для игрока"""
        capture_moves = []

        for y in range(8):
            for x in range(8):
                piece = board.get_piece(x, y)
                if piece and piece.color == player_color:
                    captures = self.generate_capture_moves(board, x, y, player_color)
                    capture_moves.extend(captures)

        return capture_moves

    def generate_capture_moves(self, board, x, y, player_color, is_continuation=False):
        """Генерация ходов с взятием (включая множественные взятия)"""
        piece = board.get_piece(x, y)
        capture_moves = []

        # Определяем все возможные направления для взятия
        if piece.is_king:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            if piece.color == 'black':
                directions = [(1, -1), (1, 1)]  # Черные могут бить вперед
            else:
                directions = [(-1, -1), (-1, 1)]  # Белые могут бить вперед

        for dx, dy in directions:
            # Проверяем клетку с врагом
            enemy_x, enemy_y = x + dx, y + dy
            if not board.is_position_in_bounds(enemy_x, enemy_y):
                continue

            enemy = board.get_piece(enemy_x, enemy_y)

            # Проверяем, есть ли враг
            if enemy and enemy.color != player_color:
                # Проверяем клетку за врагом
                landing_x, landing_y = enemy_x + dx, enemy_y + dy

                if not board.is_position_in_bounds(landing_x, landing_y):
                    continue

                landing = board.get_piece(landing_x, landing_y)

                # Клетка за врагом должна быть пустой
                if landing is None:
                    # Для дамки нужно проверить, что между начальной и конечной позицией нет других фигур
                    if piece.is_king:
                        # Проверяем, что нет других фигур на пути кроме врага
                        if not self.has_obstacles_between(board, x, y, landing_x, landing_y, enemy_x, enemy_y):
                            # Создаем временную доску для проверки множественных взятий
                            temp_board = copy.deepcopy(board)
                            temp_board.apply_move(x, y, landing_x, landing_y, capture=True)

                            # Проверяем, может ли фигура бить дальше
                            further_captures = self.generate_capture_moves(
                                temp_board, landing_x, landing_y, player_color, is_continuation=True
                            )

                            if further_captures:
                                # Добавляем все комбинации с множественными взятиями
                                for capture_sequence in further_captures:
                                    capture_moves.append((x, y, landing_x, landing_y, *capture_sequence[2:]))
                            else:
                                capture_moves.append((x, y, landing_x, landing_y))
                    else:
                        # Для обычной шашки
                        temp_board = copy.deepcopy(board)
                        temp_board.apply_move(x, y, landing_x, landing_y, capture=True)

                        # Проверяем, может ли шашка бить дальше
                        further_captures = self.generate_capture_moves(
                            temp_board, landing_x, landing_y, player_color, is_continuation=True
                        )

                        if further_captures:
                            for capture_sequence in further_captures:
                                capture_moves.append((x, y, landing_x, landing_y, *capture_sequence[2:]))
                        else:
                            capture_moves.append((x, y, landing_x, landing_y))

        return capture_moves

    def has_obstacles_between(self, board, x1, y1, x2, y2, enemy_x, enemy_y):
        """Проверка наличия препятствий между клетками для дамки"""
        dx = 1 if x2 > x1 else -1
        dy = 1 if y2 > y1 else -1

        x, y = x1 + dx, y1 + dy
        while (x, y) != (x2, y2):
            if (x, y) != (enemy_x, enemy_y):  # Пропускаем врага
                if board.get_piece(x, y) is not None:
                    return True
            x += dx
            y += dy

        return False

    def is_legal_move(self, board, x1, y1, x2, y2, player_color):
        """Проверка, является ли ход легальным"""
        legal_moves = self.get_legal_moves(board, x1, y1, player_color)

        for move in legal_moves:
            if len(move) == 2 and move == (x2, y2):
                return True
            elif len(move) >= 4 and move[0] == x1 and move[1] == y1 and move[2] == x2 and move[3] == y2:
                return True

        return False

    def can_promote(self, board, x, y):
        """Проверка, может ли шашка стать дамкой"""
        piece = board.get_piece(x, y)
        if piece and not piece.is_king:
            # Черные шашки становятся дамками на последней линии (7)
            if piece.color == 'black' and y == 7:
                return True
            # Белые шашки становятся дамками на последней линии (0)
            if piece.color == 'white' and y == 0:
                return True
        return False

    def has_mandatory_captures(self, board, player_color):
        """Проверка наличия обязательных взятий"""
        capture_moves = self.get_all_capture_moves(board, player_color)
        return len(capture_moves) > 0

    def is_game_over(self, board, player_color):
        """Проверка окончания игры"""
        # Проверяем, есть ли у игрока ходы
        has_moves = False

        for y in range(8):
            for x in range(8):
                piece = board.get_piece(x, y)
                if piece and piece.color == player_color:
                    if self.get_legal_moves(board, x, y, player_color):
                        has_moves = True
                        break
            if has_moves:
                break

        return not has_moves

    def get_winner(self, board):
        """Определение победителя"""
        black_pieces = 0
        white_pieces = 0

        for y in range(8):
            for x in range(8):
                piece = board.get_piece(x, y)
                if piece:
                    if piece.color == 'black':
                        black_pieces += 1
                    else:
                        white_pieces += 1

        if black_pieces == 0:
            return 'white'
        elif white_pieces == 0:
            return 'black'
        else:
            return None