from ui import menu
from game import Game


def main():
    logo = ''.join(open('assets/logo.txt').readlines())
    variant_module_name, mode_module_name = menu.start(logo)
    game = Game(variant_module_name, mode_module_name)
    game.run()


if __name__ == "__main__":
    main()