import re
import base

from ui import console


def get_variant():
    print('\n' * 4)
    console.print_center('Выберите вид игры:')
    console.print_center('1.♟️ Классические шахматы')
    console.print_center('2.👌 Шахматы на троих')
    console.print_center('3.🛠️ Шахматы с модификациями')
    console.print_center('4.🧨 Шашки')
    console.print_center('5.💠 Гексагональные шахматы\n')
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
        value = choose_function()

        if not is_valid(value):
            print('Некорректный ввод. Введите Enter')
            input()
            continue

        return converter.get(value, value)


def is_ip_valid(input_ip):
    ip_pattern = r'^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$'
    return bool(re.match(ip_pattern, input_ip)) or input_ip == 'q'


def start():
    while True:
        variant = selection_loop(
            get_variant,
            base.numbers_to_str_variants,
            lambda x: x in list(map(str, range(1, 6)))
        )

        while True:
            mode = selection_loop(
                get_mode,
                base.numbers_to_str_modes,
                lambda x: x in list(map(str, range(1, 4)))
            )

            if mode == 'back':
                break

            if mode != 'online':
                return variant, mode, (None, None)

            while True:
                network_type = selection_loop(
                    get_network_type,
                    base.network_menu,
                    lambda x: x in list(map(str, range(1, 4)))
                )

                if network_type == 'back':
                    break

                if network_type == 'server':
                    return variant, mode, (network_type, None)

                if network_type == 'client':
                    ip = selection_loop(
                        get_connection_ip,
                        base.connection_menu,
                        is_ip_valid
                    )

                    if ip == 'back' or ip == 'q':
                        continue

                    return variant, mode, (network_type, ip)