from base import WHITE, BLACK
from ui import console
from modes import base


class Mode(base.GameMode):
    def __init__(self, board, rules, render, network_config):
        super().__init__(board, rules, render)

    def run(self):
        while True:
            console.clear_console()
            console.print_logo()
            self.render.print_board(self.board)

            raw_input = console.get_player_input(self.turn)
            normalized = self.normalize_input(raw_input)
            if not normalized:
                self.handle_input_error('Неверный формат! Примеры: e2 e4, e2e4, а2 а4')
                continue
            x_from, y_from, x_to, y_to = self.parse_input(normalized)
            print(x_from, y_from, x_to, y_to)
            legal_moves = self.rules.get_legal_moves(self.board, x_from, y_from, self.turn)
            print(legal_moves)
            if (x_to, y_to) not in legal_moves:
                self.handle_input_error('Невозможный ход!')
                continue

            self.board.apply_move(x_from, y_from, x_to, y_to)

            self.switch_player()

            if self.rules.is_checkmate(self.board, self.turn):
                print("Шах и мат!")
                break

            # if self.rules.is_stalemate(self.board, self.current_player):
            #     print("Пат!")
            #     break

    def handle_input_error(self, message):
        print('\n' * 3 + '\t' * 4 + message)
        input('\n' + '\t' * 4 + 'Нажмите Enter чтобы продолжить...')

    def switch_player(self):
        self.turn = BLACK if self.turn == WHITE else WHITE


