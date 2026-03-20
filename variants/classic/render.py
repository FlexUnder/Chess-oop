from variants.classic.board import Board
from base import WHITE, WHITE_SQUARE, BLACK_SQUARE, BLACK_PIECE_COLOR, WHITE_PIECE_COLOR, LIGHT_GREEN, DARK_GREEN, LIGHT_RED, DARK_RED


class Render:

    def render_board(self, board: Board, highlights=None, threats=None):
        reset_all_colors = '\x1b[0m'
        indent = '\t' * 4 + '   '

        letters = '  a b c d e f g h'

        if highlights is None:
            highlights = []

        if threats is None:
            threats = []

        highlights = set(highlights)
        threats = set(threats)

        print(indent + '\033[38;5;102m' + letters)

        for y in range(board.width):
            print(indent, end='')

            row_number = board.width - y
            print(f'\033[38;5;102m{row_number} ' + reset_all_colors, end='')

            for x in range(board.length):
                is_light = (x + y) % 2 == 0

                if (x, y) in threats:
                    back_ground_color = LIGHT_RED if is_light else DARK_RED

                elif (x, y) in highlights:
                    back_ground_color = LIGHT_GREEN if is_light else DARK_GREEN

                else:
                    back_ground_color = WHITE_SQUARE if is_light else BLACK_SQUARE

                piece = board.get_piece(x, y)

                if piece:
                    font_color = WHITE_PIECE_COLOR if piece.color == WHITE else BLACK_PIECE_COLOR
                    print(f'{back_ground_color}{font_color}{piece} {reset_all_colors}', end='')
                else:
                    print(f'{back_ground_color}  {reset_all_colors}', end='')

            print()

        print()