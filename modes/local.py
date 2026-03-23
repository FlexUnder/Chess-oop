import copy

from base import WHITE, BLACK
from ui import console
from modes import base


class Mode(base.GameMode):
    def __init__(self, board, rules, render, config, network_config):
        super().__init__(board, rules, render, config)

    def run(self):
        highlights_cells = []
        threatened_cells = []
        while True:
            console.clear_console()
            console.print_logo()
            self.render.render_board(self.board, highlights=highlights_cells, threats=threatened_cells)

            raw_input = console.get_player_input(self.turn)
            highlights_cells = []
            threatened_cells = []
            normalized = self.normalize_input(raw_input)
            if not normalized:
                self.handle_input_error('Неверный формат! Формат хода: пара [a-h][1-8].\nПримеры: e2 e4, e2e4, а2 а4')
                continue
            parsed  = self.parse_input(normalized)
            if parsed == 'danger':
                threatened_cells, is_check = self.rules.get_threatened_pieces(self.board, self.turn)
                if is_check:
                    self.handle_input_error('ШАХ')
                continue
            if parsed == 'undo':
                if len(self.board.history) > 0:
                    self.board.field = self.board.history[-1]
                    self.board.history.pop(-1)
                    self.switch_player()
                    continue
                else:
                    self.handle_input_error('История отсутствует. Первый ход')
                    continue
            if len(parsed) == 2:
                x, y = parsed

                piece = self.board.get_piece(x, y)
                if not piece or piece.color != self.turn:
                    self.handle_input_error('Неверная фигура')
                    continue

                highlights_cells = self.rules.get_legal_moves(self.board, x, y, self.turn)
                continue

            elif len(parsed) == 4:
                x_from, y_from, x_to, y_to = parsed

                piece = self.board.get_piece(x_from, y_from)
                if not piece or piece.color != self.turn:
                    self.handle_input_error('Неверная фигура')
                    continue

                legal_moves = self.rules.get_legal_moves(self.board, x_from, y_from, self.turn)
                if (x_to, y_to) not in legal_moves:
                    self.handle_input_error('Фигура не может сделать ход на эту клетку!')
                    continue

                self.board.history.append(copy.deepcopy(self.board.field))

                self.board.apply_move(x_from, y_from, x_to, y_to)

                self.switch_player()

                finish_message = self.rules.get_game_finish_message(self.board, self.turn)
                if finish_message:
                    print(finish_message)
                    break

    def handle_input_error(self, message):
        print('\n' * 3 + '\t' * 4 + message)
        input('\n' + '\t' * 4 + 'Нажмите Enter чтобы продолжить...')

    def switch_player(self):
        self.turn = BLACK if self.turn == WHITE else WHITE


