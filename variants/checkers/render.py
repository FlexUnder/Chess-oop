from variants.checkers.board import Board
from base import WHITE, BLACK, WHITE_SQUARE, BLACK_SQUARE, BLACK_PIECE_COLOR, WHITE_PIECE_COLOR


class Render:
    def print_board(self, board: Board):
        reset_all_colors = '\x1b[0m'
        indent = '\t' * 4 + '   '

        letters = '  a b c d e f g h'

        print(indent + '\033[38;5;102m' + letters)

        for y in range(board.width):
            print(indent, end='')

            row_number = board.width - y
            print(f'\033[38;5;102m{row_number} ' + reset_all_colors, end='')

            for x in range(board.length):
                back_ground_color = WHITE_SQUARE if (x + y) % 2 == 0 else BLACK_SQUARE
                piece = board.get_piece(x, y)

                if piece:
                    font_color = WHITE_PIECE_COLOR if piece.color == WHITE else BLACK_PIECE_COLOR

                    # Определяем символ для отображения в зависимости от типа фигуры
                    if hasattr(piece, 'is_king') and piece.is_king:
                        # Для дамок используем символ короны
                        symbol = '♛'
                    else:
                        # Для обычных шашек используем кружочки
                        symbol = '●'

                    print(f'{back_ground_color} {font_color}{symbol}{reset_all_colors}', end='')
                else:
                    print(f'{back_ground_color}  {reset_all_colors}', end='')

            print()

        print()

    def print_board_with_coordinates(self, board: Board):
        """Дополнительная функция для отладки - показывает координаты"""
        reset_all_colors = '\x1b[0m'
        indent = '\t' * 4 + '   '

        letters = '  a(0) b(1) c(2) d(3) e(4) f(5) g(6) h(7)'

        print(indent + '\033[38;5;102m' + letters)

        for y in range(board.width):
            print(indent, end='')

            row_number = board.width - y
            print(f'\033[38;5;102m{row_number}({y}) ' + reset_all_colors, end='')

            for x in range(board.length):
                back_ground_color = WHITE_SQUARE if (x + y) % 2 == 0 else BLACK_SQUARE
                piece = board.get_piece(x, y)

                if piece:
                    font_color = WHITE_PIECE_COLOR if piece.color == WHITE else BLACK_PIECE_COLOR

                    if hasattr(piece, 'is_king') and piece.is_king:
                        symbol = '♔' if piece.color == BLACK else '♕'
                    else:
                        symbol = '●' if piece.color == BLACK else '○'

                    print(f'{back_ground_color}{font_color}{symbol} {reset_all_colors}', end='')
                else:
                    print(f'{back_ground_color}  {reset_all_colors}', end='')

            print()

        print()

    def print_board_unicode(self, board: Board):
        """Версия с более красивыми Unicode символами"""
        reset_all_colors = '\x1b[0m'
        indent = '\t' * 4 + '   '

        letters = '  a b c d e f g h'

        print(indent + '\033[38;5;102m' + letters)

        for y in range(board.width):
            print(indent, end='')

            row_number = board.width - y
            print(f'\033[38;5;102m{row_number} ' + reset_all_colors, end='')

            for x in range(board.length):
                back_ground_color = WHITE_SQUARE if (x + y) % 2 == 0 else BLACK_SQUARE
                piece = board.get_piece(x, y)

                if piece:
                    font_color = WHITE_PIECE_COLOR if piece.color == WHITE else BLACK_PIECE_COLOR

                    if hasattr(piece, 'is_king') and piece.is_king:
                        # Более красивые символы для дамок
                        symbol = '♚' if piece.color == BLACK else '♛'
                    else:
                        # Разные символы для обычных шашек
                        if piece.color == BLACK:
                            symbol = '⚫'  # Черный круг
                        else:
                            symbol = '⚪'  # Белый круг

                    print(f'{back_ground_color}{font_color}{symbol} {reset_all_colors}', end='')
                else:
                    # Для пустых клеток используем пробелы или символы
                    if (x + y) % 2 == 0:
                        print(f'{back_ground_color}  {reset_all_colors}', end='')  # Светлая клетка
                    else:
                        print(f'{back_ground_color}  {reset_all_colors}', end='')  # Темная клетка

            print()

        print()

    def print_board_simple(self, board: Board):
        """Простая текстовая версия без цветов"""
        indent = '    '

        print(indent + '  a b c d e f g h')

        for y in range(board.width):
            print(indent, end='')

            row_number = board.width - y
            print(f'{row_number} ', end='')

            for x in range(board.length):
                piece = board.get_piece(x, y)

                if piece:
                    if hasattr(piece, 'is_king') and piece.is_king:
                        symbol = 'K' if piece.color == BLACK else 'Q'
                    else:
                        symbol = 'B' if piece.color == BLACK else 'W'
                    print(f'{symbol} ', end='')
                else:
                    if (x + y) % 2 == 0:
                        print('. ', end='')  # Светлая клетка
                    else:
                        print('  ', end='')  # Темная клетка (пустая)

            print()

        print()


# Альтернативный вариант с использованием emoji
class EmojiRender:
    def print_board(self, board: Board):
        indent = '\t' * 4 + '   '

        letters = '  a b c d e f g h'
        print(indent + letters)

        for y in range(board.width):
            print(indent, end='')

            row_number = board.width - y
            print(f'{row_number} ', end='')

            for x in range(board.length):
                piece = board.get_piece(x, y)

                if piece:
                    if hasattr(piece, 'is_king') and piece.is_king:
                        # Дамки
                        if piece.color == BLACK:
                            print('👑 ', end='')  # Черная дамка
                        else:
                            print('👸 ', end='')  # Белая дамка
                    else:
                        # Обычные шашки
                        if piece.color == BLACK:
                            print('⚫ ', end='')  # Черная шашка
                        else:
                            print('⚪ ', end='')  # Белая шашка
                else:
                    if (x + y) % 2 == 0:
                        print('⬜ ', end='')  # Светлая клетка
                    else:
                        print('⬛ ', end='')  # Темная клетка

            print()

        print()