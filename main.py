from ui import menu
from game import Game


def main():
    variant_module_name, mode_module_name, network_config = menu.start()
    game = Game(variant_module_name, mode_module_name, network_config)
    game.run()


if __name__ == "__main__":
    main()