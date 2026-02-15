from base import WHITE
from ui import utils as ui_utils
from ui import console
from modes import base


class Mode(base.GameMode):
    def __init__(self, board, rules, render):
        super().__init__(board, rules, render)

    def run(self):
        turn = WHITE
        while True:
            ui_utils.clear_console()
            ui_utils.print_logo()
            self.render.print_board(self.board)

            raw_input = console.get_player_input(turn)
            parsed = self.normalize_input(raw_input)
            if not parsed:
                print('\n' * 3 + '\t' * 4 + 'Неверный формат! Примеры: e2 e4, e2e4, а2 а4')
                input('\n' + '\t' * 4 + 'Нажмите Enter чтобы продолжить...')
                continue

            move = self.get_move()

            if not self.rules.is_valid_move(self.board, move):
                continue

            self.board.apply_move(move)

            if self.rules.is_checkmate(self.board, self.current_player):
                print("Checkmate!")
                break

            if self.rules.is_stalemate(self.board, self.current_player):
                print("Stalemate!")
                break

            self.switch_player()
