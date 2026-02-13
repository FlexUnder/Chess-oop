from modes import base


class Mode(base.GameMode):
    def __init__(self, board, rules):
        super().__init__(board, rules)

    def run(self):
        while True:

            self.print_board()

            move = self.get_move()

            if not self.rules.is_valid_move(self.board, move):
                continue

            self.board.apply_move(move)

            # 🔥 ВАЖНО — проверка после хода
            if self.rules.is_checkmate(self.board, self.current_player):
                print("Checkmate!")
                break

            if self.rules.is_stalemate(self.board, self.current_player):
                print("Stalemate!")
                break

            self.switch_player()
