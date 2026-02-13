class GameMode:
    def __init__(self, board, rules):
        self.board = board
        self.rules = rules

    def run(self):
        raise NotImplementedError