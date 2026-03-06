import os
import platform

from base import WHITE


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
    else:
        player_input = input('\t' * 4 + ' Ход черных > ')
    return player_input


def print_center(text, offset=0, padding_left=4):
    print('\t' * (padding_left + offset) + ('\n' + '\t' * (padding_left + offset)).join(text.split('\n')))
