class GameMode:
    # def __init__(self, board_factory, engine, ui, network=None):
    def __init__(self, board_factory):
        self.board = board_factory()
