from base import (
    WHITE,
    BLACK,
    RED,
    WHITE_SQUARE,
    BLACK_SQUARE,
    WHITE_PIECE_COLOR,
    BLACK_PIECE_COLOR
)

reset_all_colors = '\033[0m'


class Render:

    def render_board(self, board, highlights=None, threats=None):

        if highlights is None:
            highlights = []

        if threats is None:
            threats = []

        print()

        # буквы сверху
        print('   ', end='')

        for x in range(board.SIZE):
            print(f' {chr(97 + x)} ', end='')

        print('\n')

        for y in range(board.SIZE):

            # номер строки
            print(f'{board.SIZE - y:2} ', end='')

            for x in range(board.SIZE):

                if not board.is_position_in_bounds(x, y):
                    print('   ', end='')
                    continue

                is_light = (x + y) % 2 == 0

                background = WHITE_SQUARE if is_light else BLACK_SQUARE

                piece = board.get_piece(x, y)

                if piece is None:
                    print(f'{background}   {reset_all_colors}', end='')
                    continue

                # цвет фигуры
                if piece.color == WHITE:
                    piece_color = WHITE_PIECE_COLOR

                elif piece.color == BLACK:
                    piece_color = BLACK_PIECE_COLOR

                else:
                    # RED
                    piece_color = '\033[38;5;196m'

                print(
                    f'{background}{piece_color} {piece} {reset_all_colors}',
                    end=''
                )

            print(f' {board.SIZE - y}')

        print()

        # буквы снизу
        print('   ', end='')

        for x in range(board.SIZE):
            print(f' {chr(97 + x)} ', end='')

        print('\n')