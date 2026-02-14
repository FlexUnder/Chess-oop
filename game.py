import importlib


class Game:
    def __init__(self, variant_name: str, mode_name: str):
        variant = self.load_variant(variant_name)
        board = variant.setup.create_board()
        rules = variant.rules.Rules()
        render = variant.render.Render()
        self.mode = self.create_mode(mode_name, board, rules, render)

    def load_variant(self, variant_name):
        return importlib.import_module(f"variants.{variant_name}")

    def create_mode(self, mode_name, board, rules, render):
        module = importlib.import_module(f"modes.{mode_name}")
        return module.Mode(board, rules, render)

    def run(self):
        self.mode.run()