import copy
import re
from base import WHITE, BLACK
from ui import console
from modes import base
from variants.hex.board import VALID_HEXES

COLS = 'abcdefghijk'

def _label_to_qr(label: str):
    label = label.strip().lower()
    match = re.match(r'^([a-k])(\d{1,2})$', label)
    if not match:
        return None
    col_l, row_s = match.groups()
    q = COLS.index(col_l) - 5
    r = 6 - int(row_s)
    if (q, r) in VALID_HEXES:
        return q, r
    return None

def _qr_to_label(q, r):
    col_l = COLS[q + 5]
    row_n = 6 - r
    return f'{col_l}{row_n}'


class Mode(base.GameMode):
    def __init__(self, board, rules, render, network_config):
        super().__init__(board, rules, render)

    def run(self):
        highlights_cells = []
        threatened_cells = []

        while True:
            console.clear_console()
            console.print_logo()
            self.render.render_board(self.board,
                                     highlights=highlights_cells,
                                     threats=threatened_cells)

            raw_input = console.get_player_input(self.turn)
            highlights_cells = []
            threatened_cells = []

            raw = raw_input.strip().lower()

            if raw == 'undo':
                if len(self.board.history) > 0:
                    self.board.field = self.board.history[-1]
                    self.board.history.pop(-1)
                    self._switch_player()
                else:
                    self.handle_input_error('История отсутствует. Первый ход')
                continue

            parts = raw.split()
            if len(parts) == 2:
                from_qr = _label_to_qr(parts[0])
                to_qr   = _label_to_qr(parts[1])
                if not from_qr or not to_qr:
                    self.handle_input_error('Неверный формат! Пример: f6 f7')
                    continue
                fq, fr = from_qr
                tq, tr = to_qr

                piece = self.board.get_piece(fq, fr)
                if not piece or piece.color != self.turn:
                    self.handle_input_error('Неверная фигура!')
                    continue

                legal = self.rules.get_legal_moves(self.board, fq, fr, self.turn)
                if (tq, tr) not in legal:
                    self.handle_input_error('Невозможный ход!')
                    continue

                self.board.history.append(copy.deepcopy(self.board.field))
                self.board.apply_move(fq, fr, tq, tr)
                self._switch_player()

                finish = self.rules.get_game_finish_message(self.board, self.turn)
                if finish:
                    console.clear_console()
                    console.print_logo()
                    self.render.render_board(self.board)
                    print(finish)
                    input('\n' + '\t' * 4 + 'Нажмите Enter чтобы выйти...')
                    break

            elif len(parts) == 1:
                qr = _label_to_qr(parts[0])
                if not qr:
                    match = re.match(r'^([a-k]\d{1,2})([a-k]\d{1,2})$', raw)
                    if match:
                        from_qr = _label_to_qr(match.group(1))
                        to_qr   = _label_to_qr(match.group(2))
                        if from_qr and to_qr:
                            fq, fr = from_qr
                            tq, tr = to_qr
                            piece = self.board.get_piece(fq, fr)
                            if not piece or piece.color != self.turn:
                                self.handle_input_error('Неверная фигура!')
                                continue
                            legal = self.rules.get_legal_moves(self.board, fq, fr, self.turn)
                            if (tq, tr) not in legal:
                                self.handle_input_error('Невозможный ход!')
                                continue
                            self.board.history.append(copy.deepcopy(self.board.field))
                            self.board.apply_move(fq, fr, tq, tr)
                            self._switch_player()
                            finish = self.rules.get_game_finish_message(self.board, self.turn)
                            if finish:
                                console.clear_console()
                                console.print_logo()
                                self.render.render_board(self.board)
                                print(finish)
                                input('\n' + '\t' * 4 + 'Нажмите Enter чтобы выйти...')
                                break
                            continue
                    self.handle_input_error('Неверный формат! Пример: f6 f7')
                    continue
                q, r = qr
                piece = self.board.get_piece(q, r)
                if not piece or piece.color != self.turn:
                    self.handle_input_error('Неверная фигура!')
                    continue
                highlights_cells = self.rules.get_legal_moves(self.board, q, r, self.turn)
            else:
                self.handle_input_error('Неверный формат! Пример: f6 f7')

    def handle_input_error(self, message):
        print('\n' * 3 + '\t' * 4 + message)
        input('\n' + '\t' * 4 + 'Нажмите Enter чтобы продолжить...')

    def _switch_player(self):
        self.turn = BLACK if self.turn == WHITE else WHITE