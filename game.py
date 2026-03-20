import importlib


class Game:
    def __init__(self, variant_name: str, mode_name: str, network_config):
        variant = self.load_variant(variant_name)
        board = variant.setup.create_board()
        rules = variant.rules.Rules()
        render = variant.render.Render()

        if hasattr(variant, 'after_init'):
            variant.after_init(board, rules)

        self.mode = self.create_mode(mode_name, board, rules, render, network_config)

    def load_variant(self, variant_name):
        return importlib.import_module(f"variants.{variant_name}")

    def create_mode(self, mode_name, board, rules, render, network_config):
        module = importlib.import_module(f"modes.{mode_name}")
        return module.Mode(board, rules, render, network_config)

    def run(self):
        self.mode.run()
