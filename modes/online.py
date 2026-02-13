from modes import base


class Mode(base.GameMode):

    def __init__(self, board, rules):
        super().__init__(board, rules)
        self.connection = self.init_connection()

    def run(self):
        while True:
            if self.my_turn():
                move = self.get_input()
                self.send_move(move)
            else:
                move = self.receive_move()

            self.board.apply_move(move)

            # Проверка конца игры
            if self.rules.is_checkmate(self.board, self.current_player):
                print("Game over")
                break

            self.switch_player()