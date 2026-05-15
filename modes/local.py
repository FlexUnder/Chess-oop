import copy

from base import WHITE, BLACK
from ui import console
from modes import base


class Mode(base.GameMode):
    def __init__(self, board, rules, render, config, network_config):
        super().__init__(board, rules, render, config)
        # Список игроков из конфига (по умолчанию два)
        self.players = self.params.get('players', [WHITE, BLACK])
        self.player_index = 0
        self.turn = self.players[0]
        # Выбывшие игроки
        self.eliminated = set()

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
            parsed = self.parse_input(normalized)
            if parsed is None:
                self.handle_input_error('Неверные координаты!')
                continue
            if parsed == 'danger':
                threatened_cells, is_check = self.rules.get_threatened_pieces(self.board, self.turn)
                if is_check:
                    self.handle_input_error('ШАХ')
                continue
            if parsed == 'undo':
                if len(self.board.history) > 0:
                    self.board.field = self.board.history[-1]
                    self.board.history.pop(-1)
                    self.prev_player()
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
                self.next_player()

                # Проверяем конец игры для следующего игрока
                finish = self.rules.get_game_finish_message(self.board, self.turn)
                if finish:
                    print('\n' + '\t' * 4 + finish)
                    self.eliminated.add(self.turn)
                    # Остался один — победитель
                    active = [p for p in self.players if p not in self.eliminated]
                    if len(active) == 1:
                        from base import color_converter
                        input('\n' + '\t' * 4 + f'Победа {color_converter[active[0]]}! Нажмите Enter...')
                        break
                    # Иначе выбывший пропускает ходы — просто переходим дальше
                    self.next_player()

    def next_player(self):
        while True:
            self.player_index = (self.player_index + 1) % len(self.players)
            self.turn = self.players[self.player_index]
            if self.turn not in self.eliminated:
                break

    def prev_player(self):
        while True:
            self.player_index = (self.player_index - 1) % len(self.players)
            self.turn = self.players[self.player_index]
            if self.turn not in self.eliminated:
                break

    def handle_input_error(self, message):
        print('\n' * 3 + '\t' * 4 + message)
        input('\n' + '\t' * 4 + 'Нажмите Enter чтобы продолжить...')

    def switch_player(self):
        self.next_player()