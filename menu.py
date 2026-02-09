from ui import utils


def choose_variant():
    print('\t' * 6 + 'Выберите вид игры')
    print('\t' * 6 + ' 1. Классические шахматы')
    print('\t' * 6 + ' 2. Гексагональные шахматы\n')
    print('\t' * 6 + ' 3. Шахматы с модификациями\n')
    print('\t' * 6 + ' 4. Шашки\n')
    variant = '\t' * 6 + '  > '
    return variant


def choose_mode():
    print('\t' * 6 + 'Выберите режим')
    print('\t' * 6 + ' 1. Онлайн')
    print('\t' * 6 + ' 2. Локально\n')
    variant = input('\t' * 6 + '  > ')
    return


def start(logo):
    variants = {1: 'classic', 2: 'hex', 3: 'mods', 4: 'checkers'}
    while True:
        utils.clear_console()
        print(logo)
        print('\n')
        game_variant = choose_variant()
        if not game_variant.isdigit():
            print('Некорректный ввод. Введите Enter')
            input()
            continue
        if int(game_variant) in range(1, 5):
            return variants[int(game_variant)]
        else:
            print('Некорректный ввод. Введите Enter')
            input()
            continue