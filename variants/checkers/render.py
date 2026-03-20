from base import WHITE, WHITE_SQUARE, BLACK_SQUARE, BLACK_PIECE_COLOR, WHITE_PIECE_COLOR


class Render:

    def render_board(self, board, highlights=None, threats=None):
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
                    print(f'{back_ground_color}{font_color}{piece} {reset_all_colors}', end='')
                else:
                    print(f'{back_ground_color}  {reset_all_colors}', end='')

            print()

        print()
