class GameMode:
    def __init__(self, board, rules):
        self.board = board
        self.rules = rules
        self.current_player = "white"

    def run(self):
        raise NotImplementedError