from variants.checkers import pieces
from base import WHITE, BLACK
from variants.checkers.board import Board

def create_board():
    """Создание стандартной доски для шашек (международные шашки)"""
    board = Board(rows=8, cols=8)

    # В шашках фигуры ставятся только на темные клетки
    # В шахматной нотации, если (x + y) % 2 == 1 - это темная клетка
    # (при условии, что a1 (0,0) - светлая)

    # Расстановка белых шашек (верхняя часть доски) - ряды 0, 1, 2
    # В международных шашках белые обычно сверху
    for y in range(3):  # y = 0, 1, 2
        for x in range(8):
            # Только на темных клетках
            if (x + y) % 2 == 1:
                board.field[y][x] = pieces.Checker(WHITE)

    # Расстановка черных шашек (нижняя часть доски) - ряды 5, 6, 7
    for y in range(5, 8):  # y = 5, 6, 7
        for x in range(8):
            if (x + y) % 2 == 1:
                board.field[y][x] = pieces.Checker(BLACK)

    return board


def create_russian_checkers_board():
    """Создание доски для русских шашек (белые снизу)"""
    board = Board(rows=8, cols=8)

    # Черные шашки сверху (ряды 0, 1, 2)
    for y in range(3):
        for x in range(8):
            if (x + y) % 2 == 1:
                board.field[y][x] = pieces.Checker(BLACK)

    # Белые шашки снизу (ряды 5, 6, 7)
    for y in range(5, 8):
        for x in range(8):
            if (x + y) % 2 == 1:
                board.field[y][x] = pieces.Checker(WHITE)

    return board


def create_english_checkers_board():
    """Создание доски для английских шашек (используется только 3 ряда с каждой стороны)"""
    board = Board(rows=8, cols=8)

    # В английских шашках используется только половина клеток
    # Черные шашки (ряды 0, 1, 2)
    for y in range(3):
        for x in range(8):
            # Только на темных клетках
            if (x + y) % 2 == 1:
                board.field[y][x] = pieces.Checker(BLACK)

    # Белые шашки (ряды 5, 6, 7)
    for y in range(5, 8):
        for x in range(8):
            if (x + y) % 2 == 1:
                board.field[y][x] = pieces.Checker(WHITE)

    return board


def create_checkers_board_with_kings():
    """Создание доски с дамками для тестирования"""
    board = Board(rows=8, cols=8)

    # Обычные шашки
    for y in range(3):
        for x in range(8):
            if (x + y) % 2 == 1:
                board.field[y][x] = pieces.Checker(WHITE)

    for y in range(5, 8):
        for x in range(8):
            if (x + y) % 2 == 1:
                board.field[y][x] = pieces.Checker(BLACK)

    # Добавляем дамки в центр для тестирования
    board.field[3][3] = pieces.King(WHITE)  # Белая дамка
    board.field[4][4] = pieces.King(BLACK)  # Черная дамка

    return board


def create_custom_checkers_board(config):
    """
    Создание доски с пользовательской конфигурацией

    Пример config:
    {
        'white_checkers': [(x1, y1), (x2, y2), ...],
        'black_checkers': [(x1, y1), (x2, y2), ...],
        'white_kings': [(x1, y1), ...],
        'black_kings': [(x1, y1), ...]
    }
    """
    board = Board(rows=8, cols=8)

    # Расставляем обычные шашки
    for x, y in config.get('white_checkers', []):
        if board.is_position_in_bounds(x, y):
            board.field[y][x] = pieces.Checker(WHITE)

    for x, y in config.get('black_checkers', []):
        if board.is_position_in_bounds(x, y):
            board.field[y][x] = pieces.Checker(BLACK)

    # Расставляем дамки
    for x, y in config.get('white_kings', []):
        if board.is_position_in_bounds(x, y):
            board.field[y][x] = pieces.King(WHITE)

    for x, y in config.get('black_kings', []):
        if board.is_position_in_bounds(x, y):
            board.field[y][x] = pieces.King(BLACK)

    return board


def print_board(board):
    """Вспомогательная функция для отображения доски"""
    print("  a b c d e f g h")
    for y in range(7, -1, -1):
        print(y + 1, end=" ")
        for x in range(8):
            piece = board.field[y][x]
            if piece:
                print(piece.symbol, end=" ")
            else:
                # Пустые клетки
                if (x + y) % 2 == 0:
                    print("□", end=" ")  # Светлая клетка
                else:
                    print("■", end=" ")  # Темная клетка
        print(y + 1)
    print("  a b c d e f g h")


# Самая простая версия, которая вам скорее всего нужна:
def create_standard_checkers_board():
    """Стандартная доска для шашек (белые сверху, черные снизу)"""
    board = Board(rows=8, cols=8)

    # Белые шашки (верхние 3 ряда)
    for y in range(3):
        for x in range(8):
            if (x + y) % 2 == 1:  # темные клетки
                board.field[y][x] = pieces.Checker(WHITE)

    # Черные шашки (нижние 3 ряда)
    for y in range(5, 8):
        for x in range(8):
            if (x + y) % 2 == 1:  # темные клетки
                board.field[y][x] = pieces.Checker(BLACK)

    return board