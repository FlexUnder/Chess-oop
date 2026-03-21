from base import WHITE, WHITE_PIECE_COLOR, BLACK_PIECE_COLOR
from variants.hex.board import VALID_HEXES

RESET = '\x1b[0m'
COLS  = 'abcdefghijk'


class Render:

    def render_board(self, board, highlights=None, threats=None):
        if highlights is None: highlights = []
        if threats is None:    threats = []
        highlights = set(highlights)
        threats    = set(threats)

        indent = '\t' * 3 + '  '

        rows_data = []
        for r in range(-5, 6):
            row_hexes = []
            for q in range(-5, 6):
                if (q, r) in VALID_HEXES:
                    row_hexes.append(q)
            if row_hexes:
                rows_data.append((r, row_hexes))

        for r, row_qs in rows_data:
            offset = abs(r) * 2
            row_num = 6 - r
            piece_line = indent + " " * offset
            label_line = indent + " " * offset

            for q in row_qs:
                col_l = COLS[q + 5]
                label = f"{col_l}{row_num}"
                piece = board.get_piece(q, r)

                if (q, r) in highlights:
                    piece_line += "  * "
                elif (q, r) in threats:
                    piece_line += "  ! "
                elif piece:
                    fg = WHITE_PIECE_COLOR if piece.color == WHITE else BLACK_PIECE_COLOR
                    piece_line += f"  {fg}{piece}{RESET} "
                else:
                    piece_line += "  · "

                label_line += f" {label:<3}"

            print(piece_line)
            print(label_line)

        print()
