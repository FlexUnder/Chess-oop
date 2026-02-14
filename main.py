from ui import menu
from game import Game


def main():
    variant_module_name, mode_module_name = menu.start()
    game = Game(variant_module_name, mode_module_name)
    game.run()


if __name__ == "__main__":
    main()