import os
import platform

from base import WHITE, BLACK, RED


def clear_console():
    system = platform.system().lower()
    if system == "windows":
        os.system('cls')
    else:
        os.system('clear')


def print_logo():
    print(''.join(open('assets/logo_mini.txt').readlines()))
    print('\n')


def get_player_input(color):
    if color == WHITE:
        player_input = input('\t' * 4 + ' Ход белых > ')
    elif color == BLACK:
        player_input = input('\t' * 4 + ' Ход черных > ')
    elif color == RED:
        player_input = input('\t' * 4 + ' Ход красных > ')
    else:
        player_input = input('\t' * 4 + ' Ход следующего игрока > ')

    return player_input


def print_center(text, offset=0, padding_left=4):
    print('\t' * (padding_left + offset) + ('\n' + '\t' * (padding_left + offset)).join(text.split('\n')))
