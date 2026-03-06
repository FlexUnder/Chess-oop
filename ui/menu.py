import base

from ui import console


def get_variant():
    print('\n' * 4)
    console.print_center('Выберите вид игры:')
    console.print_center('1.♟️ Классические шахматы')
    console.print_center('2.🐝 Гексагональные шахматы')
    console.print_center('3.🛠️ Шахматы с модификациями')
    console.print_center('4.🧨 Шашки\n')
    variant = input('\t' * 4 + '  > ')
    return variant


def get_mode():
    print('\n' * 4)
    console.print_center('Выберите режим:')
    console.print_center(' 1.🌐 Онлайн')
    console.print_center(' 2.🖥️ Локально')
    console.print_center(' 3.🔙 Назад\n')
    mode = input('\t' * 4 + '  > ')
    return mode


def get_network_type():
    print('\n' * 4)
    console.print_center('Онлайн игра:')
    console.print_center(' 1.🛜 Создать сервер')
    console.print_center(' 2.🔌 Присоединиться')
    console.print_center(' 3.🔙 Назад\n')
    network_type = input('\t' * 4 + '  > ')
    return network_type


def get_connection_ip():
    print('\n' * 4)
    console.print_center('🔌 Присоединение')
    console.print_center('   q - выход')
    ip = input('\t' * 4 + '   Введите ip сервера > ')
    return ip


def selection_loop(choose_function, converter, is_valid):
    while True:
        console.clear_console()
        console.print_logo()
        game_option = choose_function()
        print('valid not None')
        if is_valid(game_option):
            print('Некорректный ввод. Введите Enter')
            input()
            continue
        else:
            if game_option in converter.keys():
                return converter[game_option]
            else:
                return game_option
        # else:
        #     if game_option in converter.keys():
        #         return converter[game_option]
        #     else:
        #         return game_option



def start():
    network_type = ''
    network_config = None
    while True:
        console.clear_console()
        console.print_logo()
        variant = selection_loop(get_variant, base.numbers_to_str_variants, lambda x: x in list(map(str, range(1, 5))))
        console.clear_console()
        console.print_logo()
        mode = selection_loop(get_mode, base.numbers_to_str_modes, lambda x: x in list(map(str, range(1, 4))))
        if mode == 'online':
            network_type = selection_loop(get_network_type, base.network_menu, lambda x: x in list(map(str, range(1, 4))))
            if network_type == 'client':
                network_config = network_type, selection_loop(get_connection_ip, base.connection_menu, )
            if network_type == 'server':
                network_config = network_type, None

        if mode != 'back' and network_type != 'back':
            break
    print(variant, mode, network_config)
    return variant, mode, network_config
