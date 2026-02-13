import importlib


class Game:
    def __init__(self, variant_name: str, mode_name: str):
        self.variant = self.load_variant(variant_name)
        self.board = self.variant.setup.create_board()
        self.rules = self.variant.rules.Rules()
        self.mode = self.create_mode(mode_name)

    def load_variant(self, variant_name):
        return importlib.import_module(f"variants.{variant_name}")

    def create_mode(self, mode_name):
        module = importlib.import_module(f"modes.{mode_name}")
        return module.Mode(self.board, self.rules)

    def run(self):
        self.mode.run()