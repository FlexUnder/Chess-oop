import base

from ui import utils


def get_variant():
    print('\t' * 6 + 'Выберите вид игры')
    print('\t' * 6 + ' 1.♟️ Классические шахматы')
    print('\t' * 6 + ' 2.🐝 Гексагональные шахматы')
    print('\t' * 6 + ' 3.🛠️ Шахматы с модификациями')
    print('\t' * 6 + ' 4.🧨 Шашки\n')
    variant = input('\t' * 6 + '  > ')
    return variant


def get_mode():
    print('\t' * 6 + 'Выберите режим')
    print('\t' * 6 + ' 1.🌐 Онлайн')
    print('\t' * 6 + ' 2.🖥️ Локально')
    print('\t' * 6 + ' 3.🔙 Назад\n')
    mode = input('\t' * 6 + '  > ')
    return mode


def selection_loop(choose_function, valid_values, converter):
    while True:
        utils.clear_console()
        utils.print_logo()
        game_option = choose_function()
        if not game_option.isdigit():
            print('Некорректный ввод. Введите Enter')
            input()
            continue
        if int(game_option) in valid_values:
            return converter[int(game_option)]
        else:
            print('Некорректный ввод. Введите Enter')
            input()
            continue


def start():
    while True:
        utils.clear_console()
        utils.print_logo()
        variant = selection_loop(get_variant, range(1, 5), base.numbers_to_str_variants)
        utils.clear_console()
        utils.print_logo()
        mode = selection_loop(get_mode, range(1, 4), base.numbers_to_str_modes)
        if mode != 'back':
            break
    return variant, mode
