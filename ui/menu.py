import base

from ui import utils
from ui.console import print_center


def get_variant():
    print('\n' * 4)
    print_center('Выберите вид игры:')
    print_center('1.♟️ Классические шахматы')
    print_center('2.🐝 Гексагональные шахматы')
    print_center('3.🛠️ Шахматы с модификациями')
    print_center('4.🧨 Шашки\n')
    variant = input('\t' * 4 + '  > ')
    return variant


def get_mode():
    print('\n' * 4)
    print_center('Выберите режим:')
    print_center(' 1.🌐 Онлайн')
    print_center(' 2.🖥️ Локально')
    print_center(' 3.🔙 Назад\n')
    mode = input('\t' * 4 + '  > ')
    return mode


def get_network_type():
    print('\n' * 4)
    print_center('Онлайн игра:')
    print_center(' 1.🛜 Создать сервер')
    print_center(' 2.🔌 Присоединиться')
    print_center(' 3.🔙 Назад\n')
    network_type = input('\t' * 4 + '  > ')
    return network_type


def get_connection_ip():
    print('\n' * 4)
    print_center('🔌 Присоединение')
    print_center('   q - выход')
    ip = input('\t' * 4 + '   Введите ip сервера > ')
    return ip


def selection_loop(choose_function, converter, valid_values=None):
    while True:
        utils.clear_console()
        utils.print_logo()
        game_option = choose_function()
        if valid_values is not None:
            if game_option not in valid_values:
                print('Некорректный ввод. Введите Enter')
                input()
                continue
            else:
                return converter[game_option]
        else:
            if game_option in converter.keys():
                return converter[game_option]
            else:
                return game_option


def start():
    network_type = ''
    network_config = None
    while True:
        utils.clear_console()
        utils.print_logo()
        variant = selection_loop(get_variant, base.numbers_to_str_variants, map(str, range(1, 5)))
        utils.clear_console()
        utils.print_logo()
        mode = selection_loop(get_mode, base.numbers_to_str_modes, map(str, range(1, 4)))
        if mode == 'online':
            network_type = selection_loop(get_network_type, base.network_menu, map(str, range(1, 4)))
            if network_type == 'client':
                network_config = network_type, selection_loop(get_connection_ip, base.connection_menu)
            if network_type == 'server':
                network_config = network_type, None

        if mode != 'back' and network_type != 'back':
            break
    print(variant, mode, network_config)
    return variant, mode, network_config
